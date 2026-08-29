from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
load_dotenv()


llm3 = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.environ['GROQ_API_KEY3']
    # other params...
)

# llm = HuggingFacePipeline.from_model_id(
#     model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
#     task="text-generation",
#     pipeline_kwargs={
#         "temperature": 0.5,
#         "max_new_tokens": 200
#     }
# )



messages = [
    SystemMessage(content="You are an helpful ai assistant."),
    HumanMessage(content = "Tell me about langchain")
]




class StrOutput(BaseModel):
    report : str = Field(description="a detailed knowledge about provided topic")


parser = PydanticOutputParser(pydantic_object=StrOutput)


template = PromptTemplate(
    template = "You are an helpful AI assistant and provide a report about \n\n{topic}\n\n{format_instruction}",
    input_variables=['topic'],
    partial_variables={
        "format_instruction": parser.get_format_instructions()}
)



result = template | llm3 | parser
resultt = result.invoke({'topic' : 'Langchain'}).report
messages.append(AIMessage(content=resultt))

 
print(messages)


# import torch
# print(torch.__version__)

