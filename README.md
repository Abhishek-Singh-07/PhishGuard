\# 🛡️ PhishGuard — ML-Based Phishing URL Detector



PhishGuard is a full-stack machine learning web application that detects whether a website URL is potentially \*\*Phishing\*\* or \*\*Safe\*\*.



The application extracts \*\*30 URL and webpage-related features\*\*, processes them using a trained \*\*Random Forest Classifier\*\*, and displays the prediction and model score through a simple web interface.



\---



\## 🚀 Features



\* 🔍 Real-time URL analysis

\* 🤖 Random Forest machine learning model

\* 🧠 30-feature URL analysis

\* 🌐 Flask REST API

\* 🎨 Responsive cybersecurity-themed frontend

\* ⚡ Vanilla JavaScript frontend

\* 📊 Phishing and Safe model scores

\* 🔄 Frontend-backend API integration

\* ❌ Input validation and error handling

\* 📈 Model evaluation using Accuracy, Precision, Recall and F1 Score



\---



\## 🏗️ System Architecture



```text

&#x20;               User

&#x20;                 │

&#x20;                 ▼

&#x20;       ┌──────────────────┐

&#x20;       │   Frontend UI    │

&#x20;       │ HTML/CSS/JS      │

&#x20;       └────────┬─────────┘

&#x20;                │

&#x20;                │ POST /predict

&#x20;                ▼

&#x20;       ┌──────────────────┐

&#x20;       │   Flask Backend  │

&#x20;       │    REST API      │

&#x20;       └────────┬─────────┘

&#x20;                │

&#x20;                ▼

&#x20;       ┌──────────────────┐

&#x20;       │ Feature Extractor│

&#x20;       │    30 Features   │

&#x20;       └────────┬─────────┘

&#x20;                │

&#x20;                ▼

&#x20;       ┌──────────────────┐

&#x20;       │ Random Forest ML │

&#x20;       │      Model       │

&#x20;       └────────┬─────────┘

&#x20;                │

&#x20;                ▼

&#x20;       ┌──────────────────┐

&#x20;       │ Prediction +     │

&#x20;       │ Model Scores     │

&#x20;       └────────┬─────────┘

&#x20;                │

&#x20;                ▼

&#x20;       ┌──────────────────┐

&#x20;       │ Frontend Result  │

&#x20;       └──────────────────┘

```



\---



\## 🧠 Machine Learning Model



PhishGuard uses a \*\*Random Forest Classifier\*\* for phishing URL classification.



The model was trained using the \*\*UCI Phishing Websites Dataset\*\*.



\### Dataset



\* Records: \*\*11,055\*\*

\* Input features: \*\*30\*\*

\* Target column: \*\*Result\*\*

\* Classification:



&#x20; \* `-1` → Safe

&#x20; \* `1` → Phishing



The dataset is stored in:



```text

dataset/Training Dataset.arff

```



\---



\## 📊 Model Performance



The dataset was divided into:



\* \*\*80% training data\*\*

\* \*\*20% testing data\*\*

\* Stratified train/test split

\* Random state: `42`



The trained Random Forest model achieved:



| Metric    |      Score |

| --------- | ---------: |

| Accuracy  | \*\*97.42%\*\* |

| Precision | \*\*96.96%\*\* |

| Recall    | \*\*98.46%\*\* |

| F1 Score  | \*\*97.70%\*\* |



\### Confusion Matrix



```text

\[\[942   38]

&#x20;\[ 19 1212]]

```



The model was evaluated on the held-out test set.



\---



\## 🔎 30 Features



PhishGuard extracts 30 features corresponding to the dataset used during training.



\### Address Bar Features



1\. Having IP Address

2\. URL Length

3\. URL Shortening Service

4\. `@` Symbol

5\. Double Slash Redirecting

6\. Prefix/Suffix

7\. Subdomain

8\. SSL/HTTPS State

9\. Domain Registration Length

10\. Favicon

11\. Port

12\. HTTPS Token



\### Abnormal URL Features



13\. Request URL

14\. URL of Anchor

15\. Links in Tags

16\. Server Form Handler (SFH)

17\. Submitting to Email

18\. Abnormal URL



\### HTML / JavaScript Features



19\. Redirect

20\. On MouseOver

21\. Right Click

22\. Pop-up Window

23\. IFrame



\### Domain-Based Features



24\. Age of Domain

25\. DNS Record

26\. Web Traffic

27\. Page Rank

28\. Google Index

29\. Links Pointing to Page

30\. Statistical Report



\---



\## 🛠️ Technologies Used



\### Machine Learning



\* Python

\* NumPy

\* SciPy

\* scikit-learn

\* Random Forest

\* Joblib



\### Backend



\* Python

\* Flask

\* Flask-CORS

\* Requests

\* BeautifulSoup



\### Frontend



\* HTML5

\* CSS3

\* JavaScript

\* Fetch API



\### Dataset



\* UCI Phishing Websites Dataset



\---



\## 📁 Project Structure



```text

PhishGuard/

│

├── backend/

│   ├── app.py

│   ├── feature\_extractor.py

│   ├── load\_data.py

│   ├── test\_prediction.py

│   └── train\_model.py

│

├── dataset/

│   └── Training Dataset.arff

│

├── frontend/

│   └── index.html

│

├── model/

│   └── phishguard\_model.pkl

│

├── .gitignore

├── requirements.txt

└── README.md

```



\---



\# ⚙️ Installation



\## 1. Clone the repository



```bash

git clone https://github.com/Abhishek-Singh-07/PhishGuard.git

```



Navigate into the project:



```bash

cd PhishGuard

```



\---



\## 2. Create a Virtual Environment



\### Windows



```powershell

python -m venv venv

```



Activate it:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



\---



\## 3. Install Dependencies



```powershell

pip install -r requirements.txt

```



\---



\# ▶️ Running the Application



\## Step 1 — Start the Flask Backend



Open PowerShell inside the project:



```powershell

cd backend

```



Run:



```powershell

python app.py

```



The backend will start at:



```text

http://127.0.0.1:5000

```



You should see:



```text

PhishGuard model loaded successfully!

```



\---



\## Step 2 — Open the Frontend



Open another PowerShell window.



Navigate to the project:



```powershell

cd "C:\\Users\\Abhishek Singh\\PhishGuard"

```



Run:



```powershell

start frontend\\index.html

```



The PhishGuard interface will open in your browser.



\---



\# 🔌 API



\## Prediction Endpoint



```text

POST /predict

```



\### Request



```json

{

&#x20; "url": "https://example.com"

}

```



\### Example PowerShell Request



```powershell

Invoke-RestMethod `

&#x20; -Uri "http://127.0.0.1:5000/predict" `

&#x20; -Method POST `

&#x20; -ContentType "application/json" `

&#x20; -Body '{"url":"https://example.com"}'

```



\### Example Response



```json

{

&#x20; "url": "https://example.com",

&#x20; "prediction": "Phishing",

&#x20; "result": 1,

&#x20; "probabilities": {

&#x20;   "safe": 49.0,

&#x20;   "phishing": 51.0

&#x20; }

}

```



The displayed scores come from the Random Forest model's `predict\_proba()` output and should be understood as \*\*model scores\*\*, not guaranteed real-world probabilities.



\---



\# 🔄 How PhishGuard Works



The complete prediction flow is:



```text

1\. User enters a URL

&#x20;         ↓

2\. Frontend sends POST request

&#x20;         ↓

3\. Flask receives the URL

&#x20;         ↓

4\. Feature extractor analyzes the URL/webpage

&#x20;         ↓

5\. 30 features are generated

&#x20;         ↓

6\. Features are converted into model input

&#x20;         ↓

7\. Random Forest performs prediction

&#x20;         ↓

8\. Model generates prediction + scores

&#x20;         ↓

9\. Flask returns JSON response

&#x20;         ↓

10\. Frontend displays the result

```



\---



\# 🧪 Model Training Process



The training process follows:



```text

UCI Dataset

&#x20;    ↓

Load ARFF Dataset

&#x20;    ↓

Convert Feature Values

&#x20;    ↓

Separate X and y

&#x20;    ↓

Train/Test Split

&#x20;    ↓

Random Forest Training

&#x20;    ↓

Generate Predictions

&#x20;    ↓

Evaluate Model

&#x20;    ↓

Save Model

```



The trained model is saved as:



```text

model/phishguard\_model.pkl

```



\---



\# 🧩 Feature Extraction



When a user enters a URL, the backend extracts features such as:



\* URL length

\* Presence of IP address

\* URL shortening

\* `@` symbol

\* HTTPS

\* Subdomains

\* Prefix/suffix

\* Redirect behavior

\* IFrame usage

\* Mouse-over behavior

\* Right-click behavior

\* Popup usage

\* External links

\* Anchor links



Some domain-level features require external information such as WHOIS or additional services. Those features are currently represented using the fallback value used by the implementation when that external information is unavailable.



\---



\# 🛡️ Error Handling



The API handles cases such as:



\### Empty request



```json

{

&#x20; "error": "Request body is required"

}

```



\### Missing URL



```json

{

&#x20; "error": "URL is required"

}

```



\### Invalid/very short input



```json

{

&#x20; "error": "Please enter a valid URL"

}

```



The frontend also displays an appropriate message if the backend is unavailable.



\---



\# ⚠️ Limitations



\* The system is a machine learning classifier and predictions can be incorrect.

\* Some domain-level features require external information that is not currently retrieved through WHOIS or other external APIs.

\* Model scores from `predict\_proba()` should not be interpreted as guaranteed real-world probabilities.

\* The system should be used as a security-assistance tool rather than the sole basis for deciding whether a website is safe.

\* Live website analysis can depend on network availability and website behavior.



\---



\# 🔮 Future Improvements



Possible future improvements include:



\* Real-time WHOIS integration

\* Domain age and registration analysis

\* DNS-based feature extraction

\* Google Safe Browsing integration

\* More advanced phishing datasets

\* Additional machine learning models

\* Model comparison

\* Explainable AI for individual predictions

\* Prediction history

\* User authentication

\* Cloud deployment

\* Automated model retraining



\---



\# 🎯 Project Objective



The main objective of PhishGuard is to demonstrate how \*\*machine learning, backend APIs, feature engineering, and frontend development\*\* can be combined to create a practical cybersecurity application.



\---



\# 👨‍💻 Author



\*\*Abhishek Singh\*\*



B.Tech — Computer Science \& Engineering



PSIT, Kanpur



GitHub:



https://github.com/Abhishek-Singh-07



\---



\# 📌 Disclaimer



PhishGuard is an educational and research project created to demonstrate machine-learning-based phishing URL detection.



It should not be considered a replacement for professional cybersecurity tools or security verification services.



