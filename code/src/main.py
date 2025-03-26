from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, FastAPI
from fastapi import Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from autogen_agents import get_agent_response
from fastapi.responses import (
    HTMLResponse,
    JSONResponse
)
import os, io
import time
from time import perf_counter
import json
from incidentQueryService import IncidentQueryService
# from servicev2 import DocumentQueryServicev2
import requests
from requests.auth import HTTPBasicAuth
from subprocess import Popen, PIPE
import asyncio
import agent  # Add this line to import the agent module
from apscheduler.schedulers.background import BackgroundScheduler
# Generate a unique session ID on each app restart
import uuid
from fastapi import HTTPException
import agent

from service import DocumentQueryService
SESSION_ID = str(uuid.uuid4())


INSTANCE = "dev305679"
USERNAME = "admin"
PASSWORD = "2jzx/UCkO2I@"
HEADERS = {"Accept": "application/json"}

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]

class QueryAPI:

    def __init__(self):
        self.query_Service = IncidentQueryService("chatBot")
        # self.query_Service_v2 = DocumentQueryServicev2()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*', 'http://127.0.0.1:8080'],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

queryAPI = QueryAPI()
app.mount(path="/static", app=StaticFiles(directory="static", html=True),name="static")
# templates = Jinja2Templates(directory="templates")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message text was: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Function to notify clients about incident updates
async def notify_incident_update(update_type: str, incident: dict):
    message = {
        "type": update_type,
        "incident": incident
    }
    await manager.broadcast(json.dumps(message))

@app.get("/session_id")
async def get_session_id():
    return {"session_id": SESSION_ID}    

# @app.get("/", response_class=HTMLResponse)
# async def root(request: Request):
    
#     print(request)
#     return templates.TemplateResponse(request=request, name="index.html")        

@app.post("/v1/query", response_class=JSONResponse)
async def query(request: Request):
    
    logger = {}
    logger["endpoint"] = "/v1/query"
    logger["starting time"] = time.ctime()
    time1 = time.perf_counter()
    requestJson = await request.json()
    print(requestJson);
    response = get_agent_response(requestJson['query'])
    logger["time elapsed"] = time.perf_counter() - time1
    logger["response"] = response
    try:
        return JSONResponse(content={'response':response})
    finally:
        write_to_log(logger)
    
@app.post("/v2/query", response_class=JSONResponse)
async def query(request: Request):
    print("recahed v2");
    logger = {}
    logger["endpoint"] = "/v2/query"
    logger["starting time"] = time.ctime()
    time1 = time.perf_counter()
    requestJson = await request.json()
    response = queryAPI.query_Service_v2.rag_chain.invoke({'query': requestJson['query']})
    logger["time elapsed"] = time.perf_counter() - time1
    # print(response)
    logger["response"] = {'response': response['result'], 'sources': [{'page-content' : i.page_content, 'metadata':i.metadata} for i in response['source_documents']]}
    try:
        return JSONResponse(content={'response': response['result'], 'sources': [{'page-content' : i.page_content, 'metadata':i.metadata} for i in response['source_documents']]})
    finally:
        write_to_log(logger)

@app.post("/incidentResolution/query", response_class=JSONResponse)
async def query(request: Request):
    print("reached resolution")
    logger = {}
    logger["endpoint"] = "/incidentResolution/query"
    logger["starting time"] = time.ctime()
    time1 = time.perf_counter()
    requestJson = await request.json()
    print(requestJson);
    response = queryAPI.query_Service.rag_chain.invoke(requestJson['query']) # make new RAG chain
    print("response is: ", response)
    logger["time elapsed"] = time.perf_counter() - time1
    logger["response"] = response
    try:
        return JSONResponse(content={'response':response})
    finally:
        write_to_log(logger)

@app.get("/incident/{incident_number}", response_class=JSONResponse)
async def get_incident(incident_number: str):
    url = f"https://dev305679.service-now.com/api/now/table/incident?sysparm_query=number={incident_number}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    auth = HTTPBasicAuth("admin", "2jzx/UCkO2I@")  # Use HTTPBasicAuth for authentication
    response = requests.get(url, headers=headers, auth=auth)
    return response.json()

@app.get("/incident/{incident_number}/details", response_class=JSONResponse)
async def get_incident_details(incident_number: str):
    url = f"https://dev305679.service-now.com/api/now/table/incident?sysparm_query=number={incident_number}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    auth = HTTPBasicAuth("admin", "2jzx/UCkO2I@")  # Use HTTPBasicAuth for authentication
    response = requests.get(url, headers=headers, auth=auth)
    return response.json()

@app.post("/run-script", response_class=JSONResponse)
async def run_script(request: Request):
    
    try:
        requestJson = await request.json()
        print("reached server 1")
        script_content = requestJson.get('script', '')
        print("reached server" + script_content)
        # Save the script content to a temporary file
        temp_file_path = os.path.abspath('temp_script.bat')
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(script_content)

        # Execute the script
        process = Popen(['cmd', '/c', temp_file_path], stdout=PIPE, stderr=PIPE)
        print("reached server 2")
        stdout, stderr = process.communicate()  # Set timeout to 30 seconds
        print(stdout.decode())
        print(stderr.decode())

        # Clean up the temporary file
        os.remove(temp_file_path)

        if process.returncode == 0:
            # print(stdout.decode())
            return JSONResponse(content={'message': 'Script ran successfully.'})
        else:
            # print(stderr.decode())
            return JSONResponse(content={'error': 'Failed to run the script.'}, status_code=500)
    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=500)

@app.post("/incident/{incident_id}", response_class=JSONResponse)
async def create_incident(request: Request, incident_id: str):
    # ...existing code to create incident...
    incident = {"id": incident_id, "status": "new"}  # Example incident data
    await notify_incident_update("new", incident)
    return JSONResponse(content=incident)

@app.put("/incident/{incident_id}", response_class=JSONResponse)
async def resolve_incident(incident_id: str):
    # ...existing code to resolve incident...
    incident = {"id": incident_id, "status": "resolved"}  # Example incident data
    await notify_incident_update("resolved", incident)
    return JSONResponse(content=incident)

@app.post("/train-agent/{incident_number}", response_class=JSONResponse)
async def train_agent_endpoint(incident_number: str, request: Request):
    try:
        print("here 0")
        incident_agent = agent.IncidentAgent(INSTANCE, USERNAME, PASSWORD)
        print("here construct")
        sys_id = incident_agent.get_incident_sys_id(incident_number)
        print("here 1")
        comments = incident_agent.get_incident_comments(sys_id)
        print("here 2")
        log_links = incident_agent.get_log_file_links(sys_id)
        print("here 3")
        print("log link", log_links);
        logs = [incident_agent.download_log_file(link) for link in log_links]
        print(comments, logs)
        solution = incident_agent.train_agent(comments, logs)
        return JSONResponse(content={"solution": solution})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))         

@app.get("/api/proxy/incidents", response_class=JSONResponse)
async def proxy_incidents():
    url = "https://dev305679.service-now.com/api/now/table/incident?sysparm_query=state=1^ORstate=2"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    auth = HTTPBasicAuth("admin", "2jzx/UCkO2I@")  # Use HTTPBasicAuth for authentication

    try:
        response = requests.get(url, headers=headers, auth=auth)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

def write_to_log(data_dict):
    fname = "log.json"
    if os.path.isfile(fname):
        # File exists
        with open(fname, 'a+') as outfile:
            # outfile.seek(-1, os.SEEK_END)
            data = list(outfile)
            data.append(data_dict)
            json.dump(data, outfile)
    else: 
        # Create file
        with open(fname, 'w') as outfile:
            array = []
            array.append(data_dict)
            json.dump(array, outfile)

class ChatQuery(BaseModel):
    query: str

@app.post("/chat/query")
async def handle_chat_query(chat_query: ChatQuery):
    try:
        print("chat query", chat_query.query)
        response = get_agent_response(chat_query.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/incident/{incident_number}/related", response_class=JSONResponse)
async def get_related_incidents(incident_number: str):
    try:
        agent_instance = agent.IncidentAgent(agent.INSTANCE, agent.USERNAME, agent.PASSWORD)
        related_incidents = agent_instance.get_related_incidents(incident_number)
        return JSONResponse(content={"related_incidents": related_incidents})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))        
