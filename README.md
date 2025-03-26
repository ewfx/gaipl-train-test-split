# 🚀 Gen AI for Platform Support – Integrated Platform Environment  

## 🏆 Team: train_test_split  

## 📌 Introduction  
The **Generative AI Integrated Platform Support Environment** is designed to make platform support operations more efficient by providing a one-stop solution for managing all tasks.  

### ✨ Key Features  
- **🤖 AI-powered Chatbot** – Assists with issue resolution, troubleshooting, and knowledge retrieval.  
- **📊 Interactive Dashboard** – Displays incidents, change tasks (Ctasks), and updates in a structured manner.  
- **⚡ Real-time Alerts** – Detects anomalies and immediately notifies users for quick decision-making.  

By integrating **AI-driven automation and real-time insights**, this solution aims to **reduce manual workload, speed up incident resolution, and enhance operational efficiency**.  

---

## 🏗️ Solution Overview  
![WhatsApp Image 2025-03-26 at 16 06 23](https://github.com/user-attachments/assets/1a2e9c61-73dd-456b-945f-61c508762984)

Our **Gen AI Integrated Platform Support Environment** combines **real-time monitoring, intelligent automation, and AI-powered assistance**.  

### 🔹 1. Dashboard (Real-time Monitoring & Incident Management)  
The **dashboard** acts as the central hub for platform support personnel, displaying:  
- **🔍 Synthetic Monitoring Panel** – Shows real-time status of application monitors.  
- **📌 Autosys Jobs Panel** – Tracks running, completed, and failed jobs.  
- **🚨 BigPanda Alerts Panel** – Highlights detected anomalies and incidents.  
- **🛠️ Incidents Panel** – Lists open incidents and Major Incident Management (MIM) cases.  
- **📅 Change Management Panel** – Displays scheduled changes and approvals.  
- **🤖 Automation Panel** – Lists available automation scripts and their execution status.  

This dashboard provides a **holistic view of system health** to help engineers respond quickly to critical issues.  

---

### 🔹 2. Chatbot (AI-Powered Virtual Support Assistant)  
The AI-driven chatbot serves as a **virtual support assistant** with **agentic capabilities**, allowing engineers to:  

#### 📌 **Incident Management**  
- Retrieve **incident details** (priority, status, description).  
- Suggest **resolutions** using log analysis and monitoring insights.  
- Execute **predefined automation scripts** for quick fixes.  

#### ⚡ **Automation Execution**  
- Run **diagnostic scripts** for troubleshooting.  
- Launch **health checks** and **remediation tasks**.  

#### 📅 **Change & Task Management**  
- Provide **real-time updates** on change requests and approvals.  
- List **pending tasks** assigned to the user.  

The chatbot **follows an agentic workflow**, where a **Master Agent** understands queries and delegates tasks to specialized **Worker Agents** for execution.  

---

### 🔹 3. Real-Time Monitoring & Alerting (Proactive Issue Detection)  
#### 🛠️ **Overview**  
The **Health Check Module** monitors **system and application metrics**, detects **anomalies using AI**, and provides **real-time health reports**.  

#### 📊 **Key Features**  
1. **System Health Monitoring**  
   - Monitors **CPU, memory, and disk usage** using `psutil`.  
   - Logs real-time performance statistics.  

2. **Application Health Monitoring**  
   - Integrates with **Prometheus** for real-time metric collection.  
   - Tracks **service availability, API response times, and resource utilization**.  

3. **Anomaly Detection**  
   - Uses the **Isolation Forest** ML model to detect anomalies.  
   - Applies **statistical analysis** (e.g., standard deviation thresholds).  
   - Implements a **sliding window approach** for real-time detection.  

4. **Real-Time Alerts & Reporting**  
   - Exposes a **`/check_health` API endpoint** via Flask.  
   - **Notifies support engineers** when critical thresholds are breached.  
   - **Integrates with AI agents** to escalate alerts to external monitoring systems.    

---

## ⚙️ **Design Diagram** 

![image](https://github.com/user-attachments/assets/30bbe01c-5c84-46ae-96bc-a5723e184597)

---

## ⚙️ **Technology Stack**  
| Component            | Technology Used  |
|----------------------|-----------------|
| **Back end**        | Python, FastAPI |
| **Front end**       | React, TypeScript |
| **Embedding Model** | `models/embedding-001` |
| **LLM Model**       | Gemini-1.5-Flash |
| **Database**        | ChromaDB |
| **Monitoring**      | Prometheus |
| **Containerization**| Docker |
| **Agent Framework** | AutoGen |

---

## 🛠️ **Implementation Details**  

### 🖥️ **Dashboard**  
- **UI generated using [Lovable.dev](https://lovable.dev) AI tool**.  
- **Real-time updates & wireframe modifications supported**.  

### 🤖 **Chatbot**  
#### 1️⃣ **Master Agent**  
- **Built using AutoGen agents**.  
- Routes queries to the **Incident Resolution Agent** or **Script Runner Agent**.  

#### 2️⃣ **Incident Resolution Agent**  
- Uses **Retrieval-Augmented Generation (RAG)** to fetch solutions.  
- Retrieves **knowledge base articles** from **ServiceNow**.  
- Stores **vector embeddings in ChromaDB**.  

#### 3️⃣ **Script Runner Agent**  
- Executes scripts and **returns responses** to the chatbot UI.  

#### 4️⃣ **Similar Incident Finder**  
- Uses **ChromaDB embeddings** to **search for past incidents** with similar data - description, comments, or and text attachments.  

#### 5️⃣ **Health Checker**  
- **API-based Health Check** – Provides system health reports.  
- **Agent-Based Monitoring** – **Continuously polls Prometheus** and triggers alerts.  

---

### 🤖 **Health Check**  

### 📌 1. **Health API (`health_api.py`)**  
- Fetches **Prometheus metrics**.  
- Detects **anomalies in real time**.  
- Returns **health status reports**.  

### 📌 2. **Agent Model (`executeScript.py`)**  
- Continuously **monitors system metrics**.  
- Detects anomalies using **ML models**.  
- Sends **reports to an AI agent (AutoGen)**.  

### 📌 3. **Prometheus Polling Agent (`prometheus_polling_agent.py`)**  
- Fetches **all system metrics** from Prometheus.  
- Detects **anomalies** and reports to the **Master Agent**.  

### 📌 4. **System Health Check (`healthcheck.py`)**  
- Collects and logs **system metrics**.  
- Generates **health status reports**.

## 🚀 **Deployment Plan**  
📌 **Refer to the Deployment Playbook in the repository.**  

---

## 🎯 **Key Benefits**  
✅ **Faster Incident Resolution** – AI-powered analysis and automation.  
✅ **Proactive Monitoring** – Real-time anomaly detection prevents failures.  
✅ **Knowledge-Driven Support** – RAG pipeline ensures relevant and accurate solutions.  
✅ **Seamless Integration** – Connects with **ServiceNow, ChromaDB, Gemini**.  
✅ **Scalability & Extensibility** – Supports additional AI models and automation scripts.  

---

## 📖 **References**  
1️⃣ [ChatGPT](https://chatgpt.com/)  
2️⃣ [AutoGen Documentation](https://microsoft.github.io/autogen/dev//user-guide/agentchat-user-guide/tutorial/agents.html)  
3️⃣ [CrewAI Docs](https://docs.crewai.com/introduction)  
4️⃣ [AWS RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)  

---

🚀 **By leveraging AI and automation, this platform ensures that engineers can efficiently manage incidents, automate routine tasks, and proactively address system issues—driving higher operational efficiency and reliability.**  
