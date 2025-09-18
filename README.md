# SolTech REST API

A high-performance REST API built with **FastAPI** designed to bridge IoT devices (ESP32) with a centralized database system.  
This API efficiently handles sensor data transmission, validation, storage, and retrieval for IoT applications.

---

## 🚀 Features

- **RESTful Architecture:** Clean and intuitive API design following REST principles.  
- **Real-time Data Processing:** Efficient handling of sensor data from ESP32 devices.  
- **Advanced Validation:** Robust data validation using Pydantic schemas.  
- **Comprehensive Authentication:** API key-based authentication for secure communications.  
- **Automated Documentation:** Interactive API documentation with Swagger UI and ReDoc.  
- **Database Management:** PostgreSQL with SQLAlchemy ORM for reliable data storage.  
- **CORS Support:** Built-in Cross-Origin Resource Sharing support for web applications.  
- **Containerized Deployment:** Docker and Docker Compose for easy deployment.  

---

## 🛠️ Technology Stack

| Component             | Technology                          |
|----------------------|-----------------------------------|
| **Backend Framework** | FastAPI (Python 3.11+)            |
| **Database**          | PostgreSQL + SQLAlchemy ORM       |
| **Authentication**    | JWT tokens + API key validation   |
| **Data Validation**   | Pydantic + email-validator        |
| **Containerization**  | Docker & Docker Compose           |
| **Documentation**     | Swagger UI & ReDoc                |

---

## 🔗 API Endpoints

### 🔑 Authentication
- `POST /token` – Generate access tokens for device authentication.

### 👤 User Management
- `POST /users` – Create new system users.  
- `GET /users` – Retrieve all users.  
- `GET /users/{user_id}` – Get details of a specific user.  

### 📡 Station Management
- `POST /user-stations` – Register new sensor stations.  
- `GET /user-stations` – List all stations.  
- `GET /user-stations/{station_id}` – Get specific station details.  

### 📊 Data Operations
- `POST /station-data` – Submit sensor data (requires API key).  
- `GET /station-data` – Retrieve filtered sensor data.  
- `GET /station-data/latest` – Get latest sensor readings.  
- `GET /station-data/{data_id}` – Get a specific data record.  
- `DELETE /station-data/cleanup` – Remove old data records.  

### 🌍 Region Management
- `POST /regions` – Create new regions.  
- `GET /regions` – List all regions.  
- `GET /regions/{region_id}` – Get specific region details.  

---

## ⚡ Quick Start

### 🔹 Prerequisites
- Docker & Docker Compose installed  
- Python 3.11+ (for local development)

### 🔹 Setup & Run

```bash
# Clone the repository
git clone git@github.com:Andyflow28/SolTech_RESTAPI.git
cd SolTech_RESTAPI

# Copy example environment file
cp .env.example .env

# Build and start with Docker Compose
docker-compose up --build
