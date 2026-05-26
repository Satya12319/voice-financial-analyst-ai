import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import plotly.express as px
import json
import os  # Security aur .env read karne ke liye
from langchain_google_genai import ChatGoogleGenerativeAI
from streamlit_mic_recorder import speech_to_text

# Page Configuration & Full Screen Layout
st.set_page_config(page_title="Global Finance Analyst AI", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0f1116; color: #ffffff; }
    .stButton>button { background-color: #2563eb; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    .stTextInput>div>div>input { background-color: #1e293b; color: white; border: 1px solid #3b82f6; }
    </style>
""", unsafe_allow_html=True)

# ORIGINAL HEADERS
st.title("📊 Global Autonomous Financial Analyst Agent")
st.caption("Powered by Advanced AI Architecture | Production-Grade Analytics")
st.write("---")

# --- 🔒 SECURITY BACKEND (AUTOMATIC .ENV READING) ---
api_key = os.getenv("GEMINI_API_KEY")

# Sidebar for Settings & File Upload
st.sidebar.header("⚙️ Control Panel")
uploaded_file = st.sidebar.file_uploader("Upload Financial Data (CSV or Excel)", type=["csv", "xlsx"])

df = None
if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
        
    st.sidebar.success("✅ File uploaded successfully!")
    st.sidebar.write("### Data Preview:", df.head(3))

# Main Interface Layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("💬 Chat with Financial AI Team")
    st.write("🎙️ **Tap Microphone to Speak your command:**")
    
    text_from_voice = speech_to_text(language='en', start_prompt="🟢 Start Recording", stop_prompt="🔴 Stop", key='voice_input')
    
    default_text = text_from_voice if text_from_voice else ""
    
    user_query = st.text_input(
        "Ask anything about your data (e.g., 'What is the profit trend?' or 'Give me a risk assessment'):", 
        value=default_text,
        placeholder="Type or record your financial query here..."
    )
    analyze_btn = st.button("Run Multi-Agent Analysis")

with col2:
    # --- INTERACTIVE DATA INSIGHTS SECTION CONFIRMED ---
    st.subheader("📈 Interactive Data Insights")
    chart_placeholder = st.empty()
    chart_placeholder.info("Waiting for dataset upload to generate interactive charts automatically.")

# Core Multi-Agent Logic
if analyze_btn:
    if not api_key:
        st.error("Backend Error: Gemini API Key not found in .env file! Please check step 1.")
    elif df is None:
        st.error("Please upload a financial sheet (CSV/Excel) first!")
    elif not user_query:
        st.error("Please provide a query first!")
    else:
        with st.spinner("🚀 AI Agents are collaborating on your data... Please wait..."):
            try:
                llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)
                
                columns_list = list(df.columns)
                data_summary = f"Columns available: {columns_list}\nData Sample:\n{df.head(10).to_string()}"
                
                system_prompt = f"""
                You are a team of two world-class financial experts working sequentially:
                1. Senior Quantitative Data Scientist: Analyzes the numbers deeply, extracts stats, trends, and prepares charting structures.
                2. Chief Financial Officer (CFO): Converts those numbers into strategic global business advice, risk management, and executive insights.
                
                User Dataset Summary:
                {data_summary}
                
                User Request: {user_query}
                
                You must collaborate and provide your final response in two strict parts separated by a unique delimiter '|||CHART_CONFIG|||'.
                
                Part 1: Detailed Executive Financial Report combining the Quantitative Data Scientist's mathematical findings and the CFO's strategic advice in beautiful Markdown format (in professional Hinglish).
                Part 2: If the user explicitly or implicitly asked for a graph, chart, or visual format, output a valid single-line JSON object specifying how to plot it. If no chart is needed, output 'NONE'.
                
                The JSON structure must be exactly like this:
                {{
                    "type": "bar" or "line" or "scatter",
                    "x": "exact_column_name_for_x",
                    "y": "exact_column_name_for_y",
                    "title": "A professional chart title"
                }}
                
                Separate Part 1 and Part 2 using exactly '|||CHART_CONFIG|||'. Do not wrap Part 2 inside code blocks.
                """
                
                response = llm.invoke(system_prompt).content
                
                if "|||CHART_CONFIG|||" in response:
                    report_part, chart_part = response.split("|||CHART_CONFIG|||")
                else:
                    report_part = response
                    chart_part = "NONE"
                
                with col1:
                    st.success("✨ Analysis Completed by CFO Agent Team!")
                    st.markdown("### 📋 Executive Financial Report")
                    st.write(report_part.strip())
                
                with col2:
                    chart_str = chart_part.strip().replace("```json", "").replace("```", "").strip()
                    
                    if "NONE" not in chart_str and chart_str != "":
                        try:
                            chart_config = json.loads(chart_str)
                            c_type = chart_config.get("type", "line")
                            x_col = chart_config.get("x")
                            y_col = chart_config.get("y")
                            title = chart_config.get("title", "AI Financial Chart")
                            
                            if x_col in df.columns and y_col in df.columns:
                                if c_type == "bar":
                                    df_grouped = df.groupby(x_col, as_index=False)[y_col].sum()
                                    fig = px.bar(
                                        df_grouped, x=x_col, y=y_col, title=title, color=x_col, 
                                        color_discrete_sequence=px.colors.qualitative.Prism, 
                                        template="plotly_dark"
                                    )
                                elif c_type == "scatter":
                                    fig = px.scatter(
                                        df, x=x_col, y=y_col, title=title, color=x_col, 
                                        color_discrete_sequence=px.colors.qualitative.Set1, 
                                        template="plotly_dark"
                                    )
                                else:
                                    fig = px.line(df, x=x_col, y=y_col, title=title, template="plotly_dark")
                                    fig.update_traces(line=dict(color='#00ffcc', width=4))
                                    
                                fig.update_layout(
                                    margin=dict(l=20, r=20, t=40, b=20),
                                    hovermode="x unified",
                                    showlegend=True,
                                    barmode='group'
                                )
                                fig.update_traces(marker=dict(opacity=1.0))
                                chart_placeholder.plotly_chart(fig, use_container_width=True)
                            else:
                                chart_placeholder.warning("AI suggested columns that don't match your dataset. Try re-phrasing.")
                        except Exception as json_err:
                            chart_placeholder.info("No specific graph was plotted for this query.")
                    else:
                        chart_placeholder.info("No specific graph was requested. Showing standard analytical overview.")
                        
            except Exception as e:
                st.error(f"An error occurred during execution: {str(e)}")