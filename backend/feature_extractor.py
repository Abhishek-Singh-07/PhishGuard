from urllib.parse import urlparse, urljoin
import re

import requests
from bs4 import BeautifulSoup


# ============================================================
# Configuration
# ============================================================

REQUEST_TIMEOUT = 5

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/153.0.0.0 Safari/537.36"
    )
}


# ============================================================
# Helper Functions
# ============================================================

def normalize_url(url):
    """
    Add a scheme if the user did not provide one.
    """

    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    return url


def get_domain(url):
    """
    Extract the hostname/domain from a URL.
    """

    parsed = urlparse(url)

    return parsed.netloc.lower().split(":")[0]


def get_page(url):
    """
    Try to download the webpage.

    Returns:
        response, soup

    If the webpage cannot be downloaded:
        returns None, None
    """

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True
        )

        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        if "text/html" not in content_type:
            return response, None

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        return response, soup

    except requests.RequestException:
        return None, None


def is_external_url(link, base_domain):
    """
    Check whether a link belongs to another domain.
    """

    if not link:
        return False

    link = link.strip()

    if link.startswith((
        "#",
        "javascript:",
        "mailto:",
        "tel:"
    )):
        return False

    try:
        link_domain = urlparse(link).netloc.lower()

        if not link_domain:
            return False

        link_domain = link_domain.split(":")[0]

        return link_domain != base_domain

    except Exception:
        return False


def calculate_external_ratio(links, base_domain):
    """
    Calculate the percentage of links pointing to
    external domains.

    Returns:
        1  -> mostly external
        0  -> mixed/uncertain
       -1  -> mostly same-domain
    """

    valid_links = []

    for link in links:

        if not link:
            continue

        link = link.strip()

        if link.startswith((
            "#",
            "javascript:",
            "mailto:",
            "tel:"
        )):
            continue

        valid_links.append(link)

    if not valid_links:
        return 0

    external_count = 0

    for link in valid_links:

        if is_external_url(
            link,
            base_domain
        ):
            external_count += 1

    external_ratio = external_count / len(valid_links)

    if external_ratio > 0.5:
        return -1

    return 1


# ============================================================
# Feature Extraction
# ============================================================

def extract_features(url):
    """
    Extract the 30 features required by the trained
    Random Forest model.

    IMPORTANT:
    The feature order must remain exactly the same
    as the training dataset.
    """

    # --------------------------------------------------------
    # Normalize URL
    # --------------------------------------------------------

    url = normalize_url(url)

    parsed = urlparse(url)

    domain = get_domain(url)

    full_url = url.lower()


    # --------------------------------------------------------
    # Try to download webpage
    # --------------------------------------------------------

    response, soup = get_page(url)


    # ========================================================
    # 1. having_IP_Address
    # ========================================================

    ip_pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"

    if re.match(ip_pattern, domain):
        having_ip_address = -1
    else:
        having_ip_address = 1


    # ========================================================
    # 2. URL_Length
    # ========================================================

    if len(url) < 54:
        url_length = 1

    elif len(url) <= 75:
        url_length = 0

    else:
        url_length = -1


    # ========================================================
    # 3. Shortining_Service
    # ========================================================

    shortening_services = [
        "bit.ly",
        "tinyurl.com",
        "goo.gl",
        "t.co",
        "ow.ly",
        "is.gd",
        "buff.ly",
        "cutt.ly",
        "tiny.cc",
        "shorturl.at"
    ]

    if any(
        service in domain
        for service in shortening_services
    ):
        shortening_service = 1

    else:
        shortening_service = -1


    # ========================================================
    # 4. having_At_Symbol
    # ========================================================

    if "@" in full_url:
        having_at_symbol = 1
    else:
        having_at_symbol = -1


    # ========================================================
    # 5. double_slash_redirecting
    # ========================================================

    remaining_url = re.sub(
        r"^https?://",
        "",
        full_url
    )

    if "//" in remaining_url:
        double_slash_redirecting = 1
    else:
        double_slash_redirecting = -1


    # ========================================================
    # 6. Prefix_Suffix
    # ========================================================

    if "-" in domain:
        prefix_suffix = -1
    else:
        prefix_suffix = 1


    # ========================================================
    # 7. having_Sub_Domain
    # ========================================================

    domain_parts = domain.split(".")

    if len(domain_parts) <= 2:
        having_sub_domain = 1

    elif len(domain_parts) == 3:
        having_sub_domain = 0

    else:
        having_sub_domain = -1


    # ========================================================
    # 8. SSLfinal_State
    # ========================================================

    if parsed.scheme == "https":
        ssl_final_state = 1
    else:
        ssl_final_state = -1


    # ========================================================
    # 9. Domain_registeration_length
    # ========================================================
    #
    # Requires domain registration information.
    # A URL alone does not provide this information.
    #

    domain_registration_length = -1


    # ========================================================
    # 10. Favicon
    # ========================================================
    #
    # Check whether a favicon exists and whether its
    # source is external.
    #

    favicon = -1

    if soup is not None:

        favicon_tags = soup.find_all(
            "link",
            rel=lambda value: (
                value and
                "icon" in str(value).lower()
            )
        )

        if favicon_tags:

            external_favicon = False

            for tag in favicon_tags:

                icon_url = tag.get("href")

                if not icon_url:
                    continue

                absolute_icon_url = urljoin(
                    url,
                    icon_url
                )

                icon_domain = get_domain(
                    absolute_icon_url
                )

                if (
                    icon_domain and
                    icon_domain != domain
                ):
                    external_favicon = True
                    break

            if external_favicon:
                favicon = -1
            else:
                favicon = 1


    # ========================================================
    # 11. port
    # ========================================================

    try:
        port_number = parsed.port

    except ValueError:
        port_number = None

    if port_number is None:
        port = 1

    elif port_number in (80, 443):
        port = 1

    else:
        port = -1


    # ========================================================
    # 12. HTTPS_token
    # ========================================================

    if "https" in domain.lower():
        https_token = -1
    else:
        https_token = 1


    # ========================================================
    # 13. Request_URL
    # ========================================================
    #
    # Analyze images, audio, video and other resources.
    #

    request_url = -1

    if soup is not None:

        resources = []

        for tag in soup.find_all(
            ["img", "audio", "video", "source"]
        ):

            resource = (
                tag.get("src")
                or tag.get("data-src")
            )

            if resource:
                resources.append(resource)

        request_url = calculate_external_ratio(
            resources,
            domain
        )


    # ========================================================
    # 14. URL_of_Anchor
    # ========================================================
    #
    # Analyze <a> elements.
    #

    url_of_anchor = -1

    if soup is not None:

        anchors = soup.find_all("a")

        if anchors:

            suspicious_count = 0
            valid_count = 0

            for anchor in anchors:

                href = anchor.get("href")

                if not href:
                    continue

                href = href.strip()

                valid_count += 1

                if href in (
                    "#",
                    "#content",
                    "#skip"
                ):
                    suspicious_count += 1
                    continue

                if href.lower().startswith(
                    "javascript:"
                ):
                    suspicious_count += 1
                    continue

                if is_external_url(
                    href,
                    domain
                ):
                    suspicious_count += 1

            if valid_count > 0:

                ratio = (
                    suspicious_count /
                    valid_count
                )

                if ratio > 0.5:
                    url_of_anchor = -1
                else:
                    url_of_anchor = 1


    # ========================================================
    # 15. Links_in_tags
    # ========================================================
    #
    # Analyze <meta>, <script> and <link> tags.
    #

    links_in_tags = -1

    if soup is not None:

        resources = []

        for tag_name in [
            "meta",
            "script",
            "link"
        ]:

            for tag in soup.find_all(tag_name):

                resource = (
                    tag.get("src")
                    or tag.get("href")
                )

                if resource:
                    resources.append(resource)

        links_in_tags = calculate_external_ratio(
            resources,
            domain
        )


    # ========================================================
    # 16. SFH
    # ========================================================
    #
    # Analyze HTML form action.
    #

    sfh = -1

    if soup is not None:

        forms = soup.find_all("form")

        if forms:

            suspicious_form = False

            for form in forms:

                action = form.get("action")

                if not action:
                    suspicious_form = True
                    break

                action = action.strip().lower()

                if action in (
                    "",
                    "about:blank"
                ):
                    suspicious_form = True
                    break

                action_url = urljoin(
                    url,
                    action
                )

                action_domain = get_domain(
                    action_url
                )

                if (
                    action_domain and
                    action_domain != domain
                ):
                    suspicious_form = True
                    break

            if suspicious_form:
                sfh = -1
            else:
                sfh = 1


    # ========================================================
    # 17. Submitting_to_email
    # ========================================================

    submitting_to_email = -1

    if soup is not None:

        page_source = str(soup).lower()

        if (
            "mailto:" in page_source
            or "mail(" in page_source
        ):
            submitting_to_email = 1

        else:
            submitting_to_email = -1


    # ========================================================
    # 18. Abnormal_URL
    # ========================================================

    if domain and domain in full_url:
        abnormal_url = 1
    else:
        abnormal_url = -1


    # ========================================================
    # 19. Redirect
    # ========================================================
    #
    # Use the actual HTTP redirect history when available.
    #

    redirect = 0

    if response is not None:

        redirect_count = len(
            response.history
        )

        if redirect_count == 0:
            redirect = 0

        else:
            redirect = 1


    # ========================================================
    # 20. on_mouseover
    # ========================================================

    on_mouseover = -1

    if soup is not None:

        mouseover_found = False

        for tag in soup.find_all(
            attrs={"onmouseover": True}
        ):

            value = str(
                tag.get("onmouseover")
            ).lower()

            if (
                "window.status" in value
                or "status" in value
            ):
                mouseover_found = True
                break

        if mouseover_found:
            on_mouseover = 1


    # ========================================================
    # 21. RightClick
    # ========================================================

    right_click = -1

    if soup is not None:

        page_source = str(soup).lower()

        if (
            "event.button==2" in page_source
            or "event.button == 2" in page_source
            or "contextmenu" in page_source
        ):
            right_click = 1


    # ========================================================
    # 22. popUpWidnow
    # ========================================================

    popup_window = -1

    if soup is not None:

        page_source = str(soup).lower()

        if (
            "window.open(" in page_source
            or "window.open (" in page_source
        ):
            popup_window = 1


    # ========================================================
    # 23. Iframe
    # ========================================================

    iframe = -1

    if soup is not None:

        iframes = soup.find_all("iframe")

        if iframes:
            iframe = 1


    # ========================================================
    # 24. age_of_domain
    # ========================================================
    #
    # Requires WHOIS/domain registration information.
    #

    age_of_domain = -1


    # ========================================================
    # 25. DNSRecord
    # ========================================================
    #
    # Requires DNS information.
    #

    dns_record = -1


    # ========================================================
    # 26. web_traffic
    # ========================================================
    #
    # Requires external traffic/ranking information.
    #

    web_traffic = -1


    # ========================================================
    # 27. Page_Rank
    # ========================================================
    #
    # Requires external ranking information.
    #

    page_rank = -1


    # ========================================================
    # 28. Google_Index
    # ========================================================
    #
    # Requires search-engine index information.
    #

    google_index = -1


    # ========================================================
    # 29. Links_pointing_to_page
    # ========================================================
    #
    # Requires external backlink information.
    #

    links_pointing_to_page = -1


    # ========================================================
    # 30. Statistical_report
    # ========================================================
    #
    # Requires external phishing/reputation reports.
    #

    statistical_report = -1


    # ========================================================
    # Final 30-feature vector
    # ========================================================

    features = [
        having_ip_address,           # 1
        url_length,                  # 2
        shortening_service,          # 3
        having_at_symbol,            # 4
        double_slash_redirecting,    # 5
        prefix_suffix,               # 6
        having_sub_domain,            # 7
        ssl_final_state,             # 8
        domain_registration_length,  # 9
        favicon,                     # 10
        port,                        # 11
        https_token,                 # 12
        request_url,                 # 13
        url_of_anchor,               # 14
        links_in_tags,               # 15
        sfh,                         # 16
        submitting_to_email,         # 17
        abnormal_url,                # 18
        redirect,                    # 19
        on_mouseover,                # 20
        right_click,                 # 21
        popup_window,                # 22
        iframe,                      # 23
        age_of_domain,               # 24
        dns_record,                  # 25
        web_traffic,                 # 26
        page_rank,                   # 27
        google_index,                # 28
        links_pointing_to_page,      # 29
        statistical_report           # 30
    ]


    return features