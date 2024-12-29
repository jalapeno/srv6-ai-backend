# Network UI

A modern web interface for visualizing network topology data from ArangoDB/Jalapeno.

## Project Structure 

network-ui/
├── frontend/ # React frontend application
├── api/ # FastAPI backend service
└── k8s/ # Kubernetes deployment configurations

## Prerequisites

- Python 3.9+
- Node.js 16+
- Access to a Kubernetes cluster
- Access to Jalapeno ArangoDB instance

## Quick Start

### Development Setup
1. API Setup

```bash
cd api
python -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

2. Frontend Setup

```bash
cd frontend
npm install
npm start
```

3. Access the application
- API Documentation: http://localhost:8000/docs
- Frontend: http://localhost:3000

### Production Deployment

```bash
kubectl apply -f k8s/
```

## Architecture
- Frontend: React with TypeScript
- API: FastAPI
- Database: ArangoDB (Jalapeno)
- Deployment: Kubernetes

## Contributing
[Contributing guidelines]

## License
[License information]

