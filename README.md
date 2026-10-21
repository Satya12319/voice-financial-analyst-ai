
🎙️ Voice-Driven Financial & Sales Analyst AI

A conversational business intelligence tool that lets users speak directly to Amazon sales data, turning spoken questions into immediate financial insights, KPIs, and summaries without writing a single line of SQL or code.

💡 Why Build This?

Analyzing e-commerce financial records usually means:

Writing repetitive queries for basic questions ("What was last month's top category?").

Navigating complex dashboard filters when all you need is a fast number.

Voice Financial Analyst AI bridges this gap: speak your business question naturally into your microphone, and the application extracts the financial context from the dataset to deliver immediate verbal and visual answers.

✨ Key Features

🗣️ Voice-Activated Queries: Formulate questions naturally in plain speech without writing formulas or filters.

💰 Amazon E-Commerce Financial Metrics: Instantly queries sales volumes, profit margins, category performance, and order statuses from amazon_sales_dataset.csv.

📊 Automated KPI Extraction: Delivers summaries on total revenue, average order value (AOV), and top-selling product segments.

⚡ Streamlined Lightweight App: Built cleanly around an interactive Python web architecture (app.py) for rapid local execution.

🛠️ Tech Stack

Core Language: Python 3.9+

Data Manipulation & Query Engine: Pandas, NumPy

Speech & Audio Processing: SpeechRecognition / Audio transcription utilities

Interface & Visualization: Streamlit / Python interactive UI

Dataset: Amazon Sales & Financial Transaction Dataset (amazon_sales_dataset.csv)

📂 Repository Structure

├── amazon_sales_dataset.csv    # E-commerce sales, order & revenue dataset
├── app.py                      # Main application logic (Audio handling + Analytics)
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation


🚀 Getting Started

1. Clone the Repository

git clone https://github.com/Satya12319/voice-financial-analyst-ai.git
cd voice-financial-analyst-ai


2. Set Up a Virtual Environment (Optional but Recommended)

python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate


3. Install Dependencies

pip install -r requirements.txt


4. Run the Application

# If using Streamlit:
streamlit run app.py

# If running as standard Python script:
python app.py


💡 Sample Questions You Can Ask

"What is our total recorded sales revenue?"

"Which product category generated the highest volume of orders?"

"Show me the monthly revenue trend for this year."

"What is the average transaction value across all fulfilled orders?"

🤝 Connect with the Developer

Satya Prakash Singh

🌐 GitHub: @Satya12319

💼 LinkedIn: Satya Prakash Singh

📧 Email: ssatyasingh598@gmail.com

⭐ If you find this project intriguing, consider leaving a star on this repository!
