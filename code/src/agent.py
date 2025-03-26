import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from requests.auth import HTTPBasicAuth
from typing import List
from incidentQueryService import IncidentQueryService
from incqueryservice import IncQueryService
from langchain_community.vectorstores import Chroma



INSTANCE = "dev305679"
USERNAME = "admin"
PASSWORD = "2jzx/UCkO2I@"
HEADERS = {"Accept": "application/json"}

class QueryAPI:

    def __init__(self):
        self.query_Service = IncidentQueryService("resolution")

class IncidentAgent:
    def __init__(self, instance: str, username: str, password: str):
        self.instance = instance
        self.auth = HTTPBasicAuth(username, password)
        f = open("keys/.gemini_api_key.txt")
        key = f.read()
        os.environ["GOOGLE_API_KEY"] = key
        self.embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.inc_query_service = IncQueryService()

    def get_incident_sys_id(self, incident_number: str) -> str:
        url = f"https://{self.instance}.service-now.com/api/now/table/incident?sysparm_query=number={incident_number}"
        print("url", url)
        response = requests.get(url, auth=self.auth, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        print("data", data)
        if data.get("result"):
            return data["result"][0]["sys_id"]
        else:
            raise HTTPException(status_code=404, detail="Incident not found")
    
        
    
    def get_related_incidents(self, incident_number: str) -> List[str]:
        incident_details = self.inc_query_service.get_incidents(incident_number = incident_number)
        incident_details = incident_details[0]
        db_connection = Chroma(persist_directory="./chroma_db_incidents_", embedding_function=self.embedding_model)
        self.retriever = db_connection.as_retriever(search_kwargs={"k": 3})
        results = self.retriever.invoke(incident_details.get("short_description") + " " + incident_details.get("description"))
        results.extend(self.retriever.invoke(self.inc_query_service.get_all_comments(incident_details.get("sys_id"))))
        results.extend(self.retriever.invoke(self.inc_query_service.get_all_attachments(incident_details.get("sys_id"))))
        return [result.metadata["source"] for result in results if result.metadata["source"] != incident_number]
     
    def get_incident_comments(self, sys_id: str) -> List[dict]:
        url = f"https://{self.instance}.service-now.com/api/now/table/sys_journal_field?sysparm_query=element_id={sys_id}"
        response = requests.get(url, auth=self.auth, headers=HEADERS)
        response.raise_for_status()
        return response.json().get("result", [])

    def get_log_file_links(self, sys_id: str) -> List[str]:
        url = f"https://{self.instance}.service-now.com/api/now/attachment?sysparm_query=table_sys_id={sys_id}"
        response = requests.get(url, auth=self.auth, headers=HEADERS)
        response.raise_for_status()
        attachments = response.json().get("result", [])
        return [attachment["download_link"] for attachment in attachments]

    def download_log_file(self, download_link: str) -> str:
        print("download_link", download_link)
        response = requests.get(download_link, auth=self.auth)
        print("response", response)
        response.raise_for_status()
        return response.text

    def train_agent(self, comments: List[dict], logs: List[str]) -> str:
        # Placeholder for training logic
        # This function should train the agent using comments and logs
        # and return a solution for the incident
        print(comments, logs)
        queryAPI = QueryAPI()
        all_comments = " ".join(comment["value"] for comment in comments)
        all_logs = " ".join(logs)
        input_data = all_comments + " " + all_logs
        response = queryAPI.query_Service.rag_chain.invoke(input_data)
        print("rag-response", response)
        return response

if __name__ == "__main__":
    agent = IncidentAgent(INSTANCE, USERNAME, PASSWORD)
    print(agent.get_related_incidents("INC0000060"))