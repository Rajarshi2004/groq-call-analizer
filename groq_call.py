import streamlit as st
from groq import Groq
import os
import csv
import json
import pandas as pd
API_KEY = st.secrets["groq_api_key"]
client = Groq(api_key=API_KEY)

CSV_FILE = "conversations.csv"

if not os.path.exists(CSV_FILE):
    
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Transcript", "Summary", "Sentiment"])

st.title("📞 Call Transcript Analyzer (Groq API)")

transcript = st.text_area("Paste customer call transcript here:")

if st.button("Analyze"):
    if transcript.strip() == "":
        st.warning("Please enter a transcript first.")
    else:
    
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  
            messages=[
                {"role": "system", "content": "You are a call center transcript analyzer."},
                {"role": "user", "content": f"Transcript:\n{transcript}\n\n1. Summarize in 2–3 sentences.\n2. Extract sentiment as Positive / Neutral / Negative.\nReply in JSON format with keys 'summary' and 'sentiment'."}
            ],
            temperature=0.3,
        )

        output = response.choices[0].message.content.strip()

        
        try:
            result = json.loads(output)
            summary = result.get("summary", "")
            sentiment = result.get("sentiment", "")
        except:
            summary = output
            sentiment = "Unknown"

        
        st.subheader("✅ Analysis Result")
        st.write("**Transcript:**", transcript)
        st.write("**Summary:**", summary)
        st.write("**Sentiment:**", sentiment)

       
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([transcript, summary, sentiment])

        st.success(f"Saved to {CSV_FILE}")
        st.subheader("📂 Download your saved conversations")
        df=pd.read_csv(CSV_FILE)
        st.dataframe(df)  
        
