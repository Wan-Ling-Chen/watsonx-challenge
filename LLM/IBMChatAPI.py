from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
import os
from langchain import PromptTemplate, LLMChain
from time import sleep

import requests
import json
from dotenv import load_dotenv
from genai.credentials import Credentials
from genai.model import Model
from genai.schemas import GenerateParams
from genai.credentials import Credentials

load_dotenv()
api_key = os.getenv("GENAI_KEY", None) 
api_url = os.getenv("GENAI_API", None)
creds = Credentials(api_key, api_endpoint=api_url)

class ChatBot():
    def __init__(self) -> None:
        return None
    def chat(self, prompt):
        params = GenerateParams(
            decoding_method="sample",
            max_new_tokens=1536,
            min_new_tokens=10,
            temperature=0.7,
        )
        lan_model = Model("bigscience/bloom", params=params, credentials=creds)
        return lan_model.generate([prompt])



class IBMChat(LLM):
    
    history_data: Optional[List] = []
    chatbot : Optional[ChatBot] = ChatBot()
    conversation : Optional[str] = ""
    cookiepath : Optional[str]
    #### WARNING : for each api call this library will create a new chat on chat.openai.com
    
    
    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        if stop is not None:
            pass
            #raise ValueError("stop kwargs are not permitted.")
        #token is a must check
        if self.chatbot is None:
            if self.cookiepath is None:
                ValueError("Cookie path is required, pls check the documentation on github")
            else: 
                if self.conversation == "":
                    print('Here')
                    self.chatbot = ChatBot()
                else:
                    raise ValueError("Something went wrong")
            
        
        sleep(2)
        data = self.chatbot.chat(prompt=prompt)
        #conversation_list = self.chatbot.get_conversation_list()
        #print(conversation_list)
        
        #add to history
        self.history_data.append({"prompt":prompt,"response":data})    
        return data[0].generated_text

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": "IBM watsonx"}

# llm = IBMChat() #for start new chat

# print(llm("Hello, how are you?"))

# for result in ChatBot().chat('Hello! How are you?':
#     print("\t {}".format(result.generated_text))
