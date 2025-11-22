# Azure Deployment Guide for ShiftHelper

## Prerequisites

1. **Azure Account**: Sign up at [portal.azure.com](https://portal.azure.com)
2. **Azure CLI**: Install from [docs.microsoft.com/cli/azure/install-azure-cli](https://docs.microsoft.com/cli/azure/install-azure-cli)
3. **Git**: Ensure your code is in a Git repository

## Deployment Steps

### 1. Login to Azure

```bash
az login
```

### 2. Create Resource Group

```bash
az group create --name shifthelper-rg --location eastus
```

### 3. Create App Service Plan

```bash
az appservice plan create \
  --name shifthelper-plan \
  --resource-group shifthelper-rg \
  --sku B1 \
  --is-linux
```

### 4. Create Web App

```bash
az webapp create \
  --resource-group shifthelper-rg \
  --plan shifthelper-plan \
  --name shifthelper-app \
  --runtime "PYTHON:3.11"
```

**Note**: Replace `shifthelper-app` with a unique name (must be globally unique across Azure).

### 5. Configure Startup Command

```bash
az webapp config set \
  --resource-group shifthelper-rg \
  --name shifthelper-app \
  --startup-file "startup.txt"
```

### 6. Deploy from Local Git

```bash
# Get deployment credentials
az webapp deployment user set \
  --user-name <username> \
  --password <password>

# Get Git URL
az webapp deployment source config-local-git \
  --name shifthelper-app \
  --resource-group shifthelper-rg

# Add Azure remote (use the URL from previous command)
git remote add azure <deployment-git-url>

# Push to Azure
git add .
git commit -m "Initial Azure deployment"
git push azure main
```

### 7. Configure Environment Variables (Optional)

```bash
az webapp config appsettings set \
  --resource-group shifthelper-rg \
  --name shifthelper-app \
  --settings WEBSITE_TIME_ZONE="America/Chicago"
```

### 8. Handle Google Calendar Credentials

**Option A: Manual Upload via Azure Portal**
1. Go to Azure Portal → Your App Service
2. Navigate to "Advanced Tools" (Kudu)
3. Go to "Debug console" → "CMD"
4. Upload `credentials.json` to `/home/site/wwwroot/`

**Option B: Use Azure Key Vault** (Recommended for production)
```bash
# Create Key Vault
az keyvault create \
  --name shifthelper-vault \
  --resource-group shifthelper-rg \
  --location eastus

# Store credentials as secret
az keyvault secret set \
  --vault-name shifthelper-vault \
  --name google-credentials \
  --file credentials.json
```

Then update your app to read from Key Vault.

### 9. View Your App

```bash
az webapp browse --name shifthelper-app --resource-group shifthelper-rg
```

Your app will be available at: `https://shifthelper-app.azurewebsites.net`

## Testing Locally with FastAPI

Before deploying, test the FastAPI version locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run FastAPI app
python app_fastapi.py
```

Visit `http://localhost:8000`

## Switching from Socket Server to FastAPI

The original `app.py` uses a custom socket server. The new `app_fastapi.py` provides the same functionality using FastAPI.

**To switch permanently:**
```bash
mv app.py app_socket.py
mv app_fastapi.py app.py
```

Or update `startup.txt` to reference `app_fastapi.py`.

## Troubleshooting

### View Logs
```bash
az webapp log tail --name shifthelper-app --resource-group shifthelper-rg
```

### SSH into Container
```bash
az webapp ssh --name shifthelper-app --resource-group shifthelper-rg
```

### Check App Status
```bash
az webapp show \
  --name shifthelper-app \
  --resource-group shifthelper-rg \
  --query state
```

## File Storage Considerations

**Current Setup**: Files are stored locally in `uploads/` and `output/` directories.

**Limitation**: Files will be lost when the app restarts or scales.

**Solution for Production**: Use Azure Blob Storage
1. Create a Storage Account
2. Update code to save/retrieve files from Blob Storage
3. Use `azure-storage-blob` Python package

## Continuous Deployment with GitHub Actions

Create `.github/workflows/azure-deploy.yml`:

```yaml
name: Deploy to Azure

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Deploy to Azure Web App
      uses: azure/webapps-deploy@v2
      with:
        app-name: 'shifthelper-app'
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
```

## Cost Estimation

- **B1 Basic Plan**: ~$13/month
- **Storage**: Minimal (< $1/month for small usage)
- **Total**: ~$15-20/month

## Next Steps

1. Test FastAPI app locally
2. Deploy to Azure following steps above
3. Configure Google Calendar credentials
4. Test all functionality
5. (Optional) Set up custom domain
6. (Optional) Enable HTTPS/SSL
