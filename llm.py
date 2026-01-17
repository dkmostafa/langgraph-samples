from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()






def get_groq_llm():
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0
    )


    return llm
