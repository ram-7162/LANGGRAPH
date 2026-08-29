from dotenv import load_dotenv
import os
load_dotenv()

from langchain_groq import ChatGroq

chatbot = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
    api_key=os.environ["GROQ_API_KEY1"],
    verbose=True,
    # other params...
)

out = chatbot.invoke('What is capital of INDIA ?')
print(out)
