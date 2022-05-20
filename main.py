from gc import callbacks
from urllib import response
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from uvicorn.config import LOGGING_CONFIG
import os
from pydantic import BaseModel
from typing import Dict
import chat as chat
from db import saveChat
import json
import random
intents = json.loads(open('intents.json').read())

PORT = int(os.getenv("PORT", 8080)) 
log_config = LOGGING_CONFIG
log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"

app = FastAPI()

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = methods,
    allow_headers = headers    
)


class UserInput(BaseModel):
    message: str

class Response(BaseModel):
    message: str = None
    res:Dict[str,str] = None


@app.put("/chat/")
async def root(message:UserInput):
    text = message.message
    results = chat.chatbot_response(text) #predict
    probRes = float(results['responseClass']['probability'])*100 

    if(probRes < 70):
        list_of_intents = intents['intents']
        output_dict = [x for x in list_of_intents if x['intent'] == 'noanswer']
        filteredIntent = output_dict[0]
        result = random.choice(filteredIntent['responses'])
        results = {
        'response': result,
        'responseClass': {
            'intent': 'noanswer',
            'probability': probRes/100
            }
        }
    await saveChat(text, results)
    return results

@app.get("/")
async def root(): 
    return {"message": "Chat is up!"}

    
if __name__  == "__main__":
	run(app, host="0.0.0.0", port=PORT,log_config=log_config)

 
# to run 
# python -m uvicorn main:app --reload

# docker image build -t <app-name> .
# docker run -p 5000:5000 -d <app-name>