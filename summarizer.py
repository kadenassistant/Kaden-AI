from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import os

# Use environment variable or Streamlit Secrets to load your key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(temperature=0.3, openai_api_key=OPENAI_API_KEY)

summary_prompt = PromptTemplate(
    input_variables=["email"],
    template="""
You are Kaden, an elite executive assistant. Summarize the following email in 2–3 short sentences.
Highlight key information and action items, if any.

EMAIL:
{email}
"""
)

def summarize_email(email_text):
    prompt = summary_prompt.format(email=email_text)
    response = llm.predict(prompt)
    return response.strip()
