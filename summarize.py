from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from dotenv import load_dotenv

load_dotenv()

def sum(obj, content):
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")    
    
    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=1000, chunk_overlap=500)
    docs = text_splitter.create_documents([content])
    map_prompt = """Write a concise summary of the following:
    "{text}"
    CONCISE SUMMARY:"""
    
    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text", "objective"])
    
    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type='map_reduce',
        map_prompt=map_prompt_template,
        combine_prompt=map_prompt_template,
        verbose=True,
    )
    
    output = summary_chain.run(input_documents=docs, objective=obj)
    return output
