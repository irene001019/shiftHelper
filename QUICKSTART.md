# ShiftHelper - Quick Start Guide

## Running Locally

### Option 1: Original Socket Server
```bash
venv/bin/python app.py
```

### Option 2: FastAPI Server (Azure-compatible)
```bash
venv/bin/python app_fastapi.py
```

Visit: `http://localhost:8000`

## Deploying to Azure

See [AZURE_DEPLOYMENT.md](./AZURE_DEPLOYMENT.md) for complete deployment instructions.

### Quick Deploy Steps:
1. Install Azure CLI
2. Login: `az login`
3. Create resources and deploy (see AZURE_DEPLOYMENT.md)

## Key Files

- `app.py` - Original socket-based server
- `app_fastapi.py` - FastAPI version for Azure
- `startup.txt` - Azure startup command
- `requirements.txt` - Python dependencies
- `.deployment` - Azure deployment config

## Testing FastAPI Locally

```bash
# Install dependencies
venv/bin/pip install -r requirements.txt

# Run FastAPI
venv/bin/python app_fastapi.py
```

The app will be available at `http://localhost:8000`
