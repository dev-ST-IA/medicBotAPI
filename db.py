from pymongo import MongoClient
from pydantic import BaseModel
from typing import Dict
class Chat(BaseModel):
    sent: str = None
    rec: str = None
    intent: str = None
    prob: str = None

client = MongoClient('mongodb+srv://salman:salman123@cluster0.z9i4w.mongodb.net/?retryWrites=true&w=majority')
async def saveChat(sent, response):
    db = client["MedicChats"]
    msg_collection = db["medChat"]
    chatObj = Chat()
    chatObj.sent = sent
    chatObj.rec = response['response']
    chatObj.intent = response['responseClass']['intent']
    probRes = float(response['responseClass']['probability'])*100
    chatObj.prob = str(probRes)
    dictionary = chatObj.dict()
    prevSent =msg_collection.find_one(({'sent':sent}))
    if(prevSent==None):
        msg_collection.insert_one(dictionary)