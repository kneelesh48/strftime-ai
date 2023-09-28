import os

import streamlit as st

import openai
import google.generativeai as palm
from anthropic import AI_PROMPT, HUMAN_PROMPT, Anthropic

from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="strftime AI", page_icon="🕘")

with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.header("strftime AI")

with st.sidebar:
    provider = st.radio("Choose AI Provider", options=["Anthropic", "Google Palm", "OpenAI"])

text = st.text_input("Enter datetime text eg. 2023-09-28T15:27:58Z")

if text:
    prompt = ("Convert the following datetime string into strftime format, "
    "show the strftime string on top and then breakdown of % symbols: " + text)

    if provider == "Anthropic":
        anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        completion = anthropic.completions.create(
            model="claude-2",
            max_tokens_to_sample=300,
            prompt=f"{HUMAN_PROMPT} {prompt}{AI_PROMPT}",
        )
        st.text(completion.completion)
    elif provider == "Google Palm":
        palm.configure(api_key=os.getenv("PALM_API_KEY"))
        completion = palm.generate_text(
            model="models/text-bison-001",
            prompt=prompt,
            temperature=0,
            max_output_tokens=800,
        )
        st.text(completion.result)
    elif provider == "OpenAI":
        openai.api_key = os.getenv("OPENAI_API_KEY")
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "user", "content": prompt}],
        )
        st.text(chat_completion.choices[0].message.content)
