# CloudOps Dashboard

A web-based cloud infrastructure monitoring and management platform built with HTML, CSS, JavaScript, Python, FastAPI and AWS Boto3.

## Project Overview

CloudOps Dashboard provides a web interface and REST API for monitoring and managing AWS infrastructure resources.

The backend integrates with AWS services to retrieve EC2 instances, S3 buckets and RDS database instances. It also provides resource-management operations for starting, stopping and rebooting EC2 and RDS instances.

The project is being developed incrementally, with an emphasis on modular backend architecture, API error handling and automated testing.

## Current Implementation Status

### Implemented

- Interactive frontend dashboard using HTML, CSS and JavaScript.
- Python FastAPI backend.
- REST API with versioned endpoints.
- AWS SDK integration using Boto3.
- AWS region configuration through environment variables.
- EC2, S3 and RDS resource retrieval.
- EC2 instance start, stop and reboot API operations.
- RDS instance start, stop and reboot API operations.
- AWS STS identity and connectivity endpoint.
- Monitoring service for EC2, S3 and RDS.
- API error handling.
- CORS configuration for local frontend development.
- Automated backend tests using Pytest.
- Git and GitHub version control.

### Planned

- CloudWatch metrics and monitoring.
- CloudWatch-based alerts and notifications.
- Authentication and role-based access control.
- Cloud cost monitoring and optimization.
- Additional security features.
- Docker containerization.
- Terraform infrastructure automation.
- AWS deployment.

## Technology Stack

| Area | Technologies |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python 3.11, FastAPI |
| AWS SDK | Boto3 |
| AWS Services | EC2, S3, RDS, STS |
| Testing | Pytest, FastAPI TestClient |
| Server | Uvicorn |
| Version Control | Git, GitHub |

## Project Architecture

```text
CloudOps-Dashboard/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── router.py
│   │   ├── models/
│   │   │   ├── monitoring.py
│   │   │   └── resources.py
│   │   ├── services/
│   │   │   ├── monitoring_service.py
│   │   │   └── resource_service.py
│   │   └── main.py
│   │
│   ├── aws/
│   │   ├── config.py
│   │   └── services.py
│   │
│   └── tests/
│
├── frontend/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── index.html
│
├── docs/
├── infrastructure/
├── requirements.txt
└── README.md
```

## Features

### Frontend Dashboard

- Web-based dashboard interface.
- Navigation and dashboard sections.
- Resource summary cards and interface components.
- Backend health connectivity check.
- Responsive styling and JavaScript interactions.

### Backend API

- FastAPI application.
- Versioned REST API under `/api/v1`.
- Structured API responses.
- Error handling for AWS resource operations.
- Interactive API documentation through Swagger UI.

### AWS Integration

The backend uses Boto3 to communicate with AWS services.

**EC2**
- Retrieve instance IDs, types, states and IP addresses.
- Start instances.
- Stop instances.
- Reboot instances.

**S3**
- Retrieve bucket names and creation dates.

**RDS**
- Retrieve database identifiers, engines, versions and status.
- Start database instances.
- Stop database instances.
- Reboot database instances.

**STS**
- Retrieve AWS account identity information.

## API Endpoints

### General

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Backend health check |
| GET | `/api/v1/status` | API status |
| GET | `/api/v1/aws/status` | AWS identity and connectivity |

### Monitoring

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/monitoring` | Retrieve EC2, S3 and RDS monitoring data |

### Resource Retrieval

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/resources/ec2` | List EC2 instances |
| GET | `/api/v1/resources/s3` | List S3 buckets |
| GET | `/api/v1/resources/rds` | List RDS instances |

### EC2 Management

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/resources/ec2/{instance_id}/start` | Start EC2 instance |
| POST | `/api/v1/resources/ec2/{instance_id}/stop` | Stop EC2 instance |
| POST | `/api/v1/resources/ec2/{instance_id}/reboot` | Reboot EC2 instance |

### RDS Management

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/resources/rds/{db_instance_identifier}/start` | Start RDS instance |
| POST | `/api/v1/resources/rds/{db_instance_identifier}/stop` | Stop RDS instance |
| POST | `/api/v1/resources/rds/{db_instance_identifier}/reboot` | Reboot RDS instance |

**Note:** Resource-management POST endpoints can modify AWS resources. Use them only with the appropriate AWS permissions and intended resource identifiers.

## Installation and Setup

### Prerequisites

- Python 3.11 or compatible version.
- Git.
- AWS account and valid AWS credentials for live AWS operations.
- Appropriate IAM permissions for the AWS operations being performed.

### 1. Clone the repository

```bash
git clone https://github.com/relkarsanket-oss/CloudOps-Dashboard.git
cd CloudOps-Dashboard
```

### 2. Create a virtual environment

Windows CMD:

```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```cmd
pip install -r requirements.txt
```

### 4. Configure AWS region

The default AWS region is:

```text
ap-south-1
```

To override it in Windows CMD:

```cmd
set AWS_REGION=ap-south-1
```

Configure valid AWS credentials using an appropriate AWS CLI profile or environment variables before making live AWS API requests.

Do not commit AWS access keys, secret keys or other credentials to GitHub.

## Running the Application

The frontend and backend run in separate terminals.

### Terminal 1 – Start the backend

Activate the virtual environment and run:

```cmd
python -m uvicorn backend.app.main:app --reload
```

Backend address:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

### Terminal 2 – Start the frontend

From the project root:

```cmd
python -m http.server 5500 --directory frontend
```

Frontend address:

```text
http://127.0.0.1:5500
```

The backend CORS configuration currently allows this local frontend origin.

## API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## Running Tests

Activate the virtual environment and execute:

```cmd
pytest -q
```

The project currently has 49 passing automated tests.

The backend tests use mocked AWS interactions where appropriate, allowing the test suite to run without depending on live AWS resources.

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `AWS_REGION` | `ap-south-1` | AWS region used by Boto3 clients |

AWS credentials should be supplied securely through the standard AWS credential mechanisms.

## Future Development Roadmap

1. Complete backend resource management.
2. Integrate CloudWatch metrics.
3. Implement monitoring alerts and notifications.
4. Introduce authentication and role-based access control.
5. Add cost monitoring and security improvements.
6. Containerize the application using Docker.
7. Explore Terraform for infrastructure automation.
8. Deploy the application to AWS.

## Project Status

This is an actively developed portfolio project demonstrating frontend development, Python backend engineering, REST API development, AWS SDK integration, resource-management operations and automated testing.

---

**GitHub Repository:**
https://github.com/relkarsanket-oss/CloudOps-Dashboard
