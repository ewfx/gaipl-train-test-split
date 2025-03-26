from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

import os
import requests
from fastapi import HTTPException
from requests.auth import HTTPBasicAuth
class IncQueryService:
    
    USERNAME = "admin"
    INSTANCE = "https://dev305679.service-now.com/api/now/table"
    PASSWORD = "2jzx/UCkO2I@"
    HEADERS = {"Accept": "application/json"}
        
    def initialise_genai_model(self):
        
        # Read the API key
        f = open("keys/.gemini_api_key.txt")
        key = f.read()
        os.environ["GOOGLE_API_KEY"] = key
        #  Setup chat model
        self.chat_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    # Load the documents from ServiceNow API
    def load_documents(self):
        incidents_response = self.get_incidents()

        if "error" in incidents_response:
            raise Exception(f"Error: {incidents_response['error']}")
        
        self.incident_documents = [Document(page_content=incident.get("short_description") + incident.get("description"), metadata={"source": incident.get("number")}) for incident in incidents_response]
        self.incident_documents.extend([Document(page_content=incident.get("comments"), metadata={"source": incident.get("number")}) for incident in incidents_response])
        self.incident_documents.extend([Document(page_content=incident.get("attachments"), metadata={"source": incident.get("number")}) for incident in incidents_response])
        

    
    def create_embeddings(self):
        self.embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        Chroma.from_documents(self.incident_documents, self.embedding_model, persist_directory="./chroma_db_incidents_")        
    
    def get_incidents(self, incident_number: str = None) -> dict: 
        try:
            incidents_url = f"{self.INSTANCE}/incident"
            incidents_response = requests.get(
                incidents_url,
                auth=HTTPBasicAuth(self.USERNAME, self.PASSWORD),
                params={
                    "sysparm_fields": "sys_id,number,short_description,description",
                    "sysparm_limit": 10000
                },
                headers=self.HEADERS
            )

            if incidents_response.status_code != 200:
                raise HTTPException(
                    status_code=incidents_response.status_code,
                    detail="Failed to fetch incident numbers."
                )

            incidents = incidents_response.json().get("result", [])
            if incident_number:
                incidents = [incident for incident in incidents if incident.get("number") == incident_number]
            incidents = [{**incident, "comments": self.get_all_comments(incident.get("sys_id")), "attachments" : self.get_all_attachments(incident.get("sys_id"))} for incident in incidents]
            return incidents  
            
           

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_all_comments(self, sys_id: str) -> str:
        url = f"{self.INSTANCE}/sys_journal_field?sysparm_query=element_id={sys_id}"
        response = requests.get(
            url,
            auth=HTTPBasicAuth(self.USERNAME, self.PASSWORD),
            headers=self.HEADERS
            )
        response.raise_for_status()

        all_comments = [comment.get("value") for comment in response.json().get("result")]

        all_comments_str = "".join(all_comments)
        return all_comments_str
    
    def get_all_attachments(self, sys_id: str) -> str:
        url = f"https://dev305679.service-now.com/api/now/attachment?sysparm_query=table_sys_id={sys_id}"
        response = requests.get(url, auth=HTTPBasicAuth(self.USERNAME, self.PASSWORD), headers=self.HEADERS)
        response.raise_for_status()
        attachments = response.json().get("result", [])
        download_links = [attachment["download_link"] for attachment in attachments]

        responses = [requests.get(download_link, auth=HTTPBasicAuth(self.USERNAME, self.PASSWORD)) for download_link in download_links]
        [response.raise_for_status() for response in responses]
        response_texts = [response.text for response in responses]
        response_texts_str = "".join(response_texts)
        return response_texts_str
    



if __name__ == "__main__":
        inc_query_service = IncQueryService()
        inc_query_service.initialise_genai_model()
        inc_query_service.load_documents()
        inc_query_service.create_embeddings()
