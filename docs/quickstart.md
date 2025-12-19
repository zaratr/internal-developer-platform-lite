# Running the IDP-Lite Platform

## Prerequisites
- Python 3.11+
- Node.js 18+
- Java 17+ (optional, for Spring Boot services)

## Quick Start

### 1. Start the Control Plane API
```bash
cd platform/api
pip install -r requirements.txt
uvicorn platform.api.main:app --reload --port 8000
```

### 2. Start the Dashboard
```bash
cd dashboard
npm install
npm run dev
```

Access the dashboard at http://localhost:5173

### 3. Create Services via CLI
```bash
# Python FastAPI service
python -m platform.cli.idp create service my-api

# Java Spring Boot service
python -m platform.cli.idp create service my-java-api --template springboot_service

# With AI optimization
python -m platform.cli.idp create service smart-api --ai-enhance
```

### 4. Run a Generated Service
```bash
cd examples/my-api
pip install -e .
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs for API documentation
Visit http://localhost:8000/metrics for Prometheus metrics

## Architecture
- **CLI**: `platform/cli/idp.py` - Service generation
- **API**: `platform/api/` - REST API for dashboard
- **Dashboard**: `dashboard/` - React control plane UI
- **Templates**: `platform/templates/` - Service scaffolds
