
from dotenv import load_dotenv
import os
load_dotenv()

from langchain_groq import ChatGroq

llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
    
    # other params...
)

out = llm.invoke('What is capital of INDIA ?')
print(out)
