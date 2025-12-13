# 🚀 **DEPLOYMENT GUIDE - EVOLVISHUB OUTLOOK INGESTOR**

## 📋 **QUICK START**

### **1. Installation**

```bash
# Clone the repository
git clone https://github.com/evolvisai/metcal.git
cd metcal/shared/libs/evolvis-outlook-ingestor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with all dependencies
pip install -e .[all,dev]
```

### **2. Basic Configuration**

```python
# config.py
config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "database": "outlook_ingestor",
        "username": "ingestor_user",
        "password": "secure_password_123!",
        "ssl_mode": "require",
    },
    "protocols": {
        "graph_api": {
            "client_id": "your_client_id",
            "client_secret": "your_client_secret",
            "tenant_id": "your_tenant_id",
        }
    },
    "processing": {
        "batch_size": 100,
        "max_concurrent": 10,
        "duplicate_cache_size": 10000,
    }
}
```

### **3. Run Tests**

```bash
# Run all tests
python run_tests.py

# Run specific test categories
pytest tests/unit/ -v                    # Unit tests
pytest tests/integration/ -v             # Integration tests
pytest tests/performance/ -m performance # Performance tests
pytest tests/security/ -m security       # Security tests
```

---

## 🔧 **PRODUCTION DEPLOYMENT**

### **1. Environment Setup**

```bash
# Production environment variables
export OUTLOOK_INGESTOR_ENV=production
export OUTLOOK_INGESTOR_LOG_LEVEL=INFO
export OUTLOOK_INGESTOR_DB_HOST=prod-db.company.com
export OUTLOOK_INGESTOR_DB_PASSWORD=encrypted_password_here
export OUTLOOK_INGESTOR_ENCRYPTION_KEY=your_encryption_key_here
```

### **2. Database Setup**

```sql
-- PostgreSQL setup
CREATE DATABASE outlook_ingestor;
CREATE USER ingestor_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE outlook_ingestor TO ingestor_user;

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
```

### **3. Application Startup**

```python
# main.py
import asyncio
from evolvishub_outlook_ingestor import OutlookIngestor
from monitoring.metrics import get_system_monitor

async def main():
    # Initialize monitoring
    monitor = get_system_monitor()
    await monitor.start_monitoring(interval=60)
    
    # Initialize ingestor
    ingestor = OutlookIngestor(config)
    
    try:
        # Start processing
        async with ingestor:
            await ingestor.start_processing()
    finally:
        await monitor.stop_monitoring()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 📊 **MONITORING SETUP**

### **1. Health Check Endpoint**

```python
# health.py
from fastapi import FastAPI
from monitoring.metrics import get_system_monitor

app = FastAPI()

@app.get("/health")
async def health_check():
    monitor = get_system_monitor()
    return monitor.get_status()

@app.get("/metrics")
async def get_metrics():
    monitor = get_system_monitor()
    return monitor.metrics.get_current_metrics()
```

### **2. Alert Configuration**

```python
# alerts.py
from monitoring.metrics import get_system_monitor, AlertSeverity

monitor = get_system_monitor()

# Add custom alert rules
monitor.alert_manager.add_alert_rule(
    name="high_processing_errors",
    metric_name="processing.error_rate",
    threshold=5.0,
    comparison="greater_than",
    severity=AlertSeverity.HIGH,
    component="processing",
)

# Add notification handler
async def send_slack_notification(alert):
    # Send alert to Slack
    pass

monitor.alert_manager.add_notification_handler(send_slack_notification)
```

---

## 🔒 **SECURITY CONFIGURATION**

### **1. Credential Management**

```python
# credentials.py
from evolvishub_outlook_ingestor.utils.security import SecureCredentialManager

# Initialize credential manager
manager = SecureCredentialManager(encryption_key="your_master_key")

# Encrypt sensitive credentials
encrypted_db_password = manager.encrypt_credential("actual_db_password")
encrypted_api_secret = manager.encrypt_credential("actual_api_secret")

# Store encrypted credentials in config
config = {
    "database": {
        "password": encrypted_db_password,
    },
    "api": {
        "client_secret": encrypted_api_secret,
    }
}
```

### **2. Input Validation**

```python
# validation.py
from evolvishub_outlook_ingestor.utils.security import InputSanitizer

# Validate all user inputs
def validate_email_filter(email_filter):
    if not InputSanitizer.validate_email_address(email_filter):
        raise ValueError("Invalid email filter")
    
    return InputSanitizer.sanitize_sql_input(email_filter)
```

---

## ⚡ **PERFORMANCE OPTIMIZATION**

### **1. Connection Pooling**

```python
# database.py
config = {
    "database": {
        "enable_connection_pooling": True,
        "pool_size": 20,
        "max_overflow": 10,
        "pool_timeout": 30,
        "pool_recycle": 3600,
    }
}
```

### **2. Batch Processing**

```python
# processing.py
from optimization.performance import BatchProcessor

# Initialize batch processor
batch_processor = BatchProcessor(
    batch_size=100,
    max_wait_time=1.0,
    max_concurrent_batches=5
)

# Process emails in batches
async def process_email_batch(emails):
    # Process batch of emails
    pass

for email in email_stream:
    await batch_processor.add_item(email, process_email_batch)
```

### **3. Caching**

```python
# caching.py
from optimization.performance import AsyncLRUCache

# Initialize cache
email_cache = AsyncLRUCache(maxsize=1000, ttl=3600)

async def get_processed_email(email_id):
    # Check cache first
    cached_email = await email_cache.get(email_id)
    if cached_email:
        return cached_email
    
    # Process and cache
    processed_email = await process_email(email_id)
    await email_cache.put(email_id, processed_email)
    return processed_email
```

---

## 🐳 **DOCKER DEPLOYMENT**

### **1. Dockerfile**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install application
RUN pip install -e .[all]

# Create non-root user
RUN useradd --create-home --shell /bin/bash ingestor
USER ingestor

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Start application
CMD ["python", "main.py"]
```

### **2. Docker Compose**

```yaml
# docker-compose.yml
version: '3.8'

services:
  outlook-ingestor:
    build: .
    environment:
      - OUTLOOK_INGESTOR_ENV=production
      - OUTLOOK_INGESTOR_DB_HOST=postgres
      - OUTLOOK_INGESTOR_DB_PASSWORD=${DB_PASSWORD}
    depends_on:
      - postgres
      - redis
    ports:
      - "8000:8000"
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=outlook_ingestor
      - POSTGRES_USER=ingestor_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

---

## 🔍 **TROUBLESHOOTING**

### **Common Issues**

#### **1. Connection Errors**
```bash
# Check database connectivity
python -c "
import asyncpg
import asyncio
async def test():
    conn = await asyncpg.connect('postgresql://user:pass@host/db')
    await conn.close()
asyncio.run(test())
"
```

#### **2. Memory Issues**
```bash
# Monitor memory usage
python -c "
from monitoring.metrics import get_system_monitor
monitor = get_system_monitor()
print(monitor.get_status())
"
```

#### **3. Performance Issues**
```bash
# Run performance tests
pytest tests/performance/ -v --tb=short
```

### **Logging Configuration**

```python
# logging_config.py
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'outlook_ingestor.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'detailed',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
        },
    },
    'loggers': {
        'evolvishub_outlook_ingestor': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
```

---

## 📞 **SUPPORT**

### **Getting Help**
- 📧 **Email**: support@evolvisai.com
- 📚 **Documentation**: [Internal Wiki]
- 🐛 **Issues**: GitHub Issues
- 💬 **Chat**: Slack #outlook-ingestor

### **Maintenance**
- 🔄 **Updates**: Monthly security updates
- 📊 **Monitoring**: 24/7 system monitoring
- 🧪 **Testing**: Continuous integration pipeline
- 📈 **Performance**: Weekly performance reviews

---

## ✅ **DEPLOYMENT CHECKLIST**

- [ ] Environment variables configured
- [ ] Database setup completed
- [ ] SSL certificates installed
- [ ] Monitoring configured
- [ ] Alerts set up
- [ ] Backup strategy implemented
- [ ] Security scan completed
- [ ] Performance tests passed
- [ ] Documentation updated
- [ ] Team training completed

**🎉 Ready for Production!**
