# 🔍 ORBIT Monitoring & Error Tracking Setup

## ✅ Configured Services

### **1. Sentry Error Monitoring** ✅

**Status**: Fully configured and ready to use

**What it does**:
- Captures all errors and exceptions automatically
- Tracks API performance and response times
- Monitors user sessions and request flows
- Provides real-time error alerts
- Shows stack traces and context for debugging

**Configuration**:
```python
DSN: https://1e7c8ab363d59011dfe897cbd193f8a7@o4510291442335744.ingest.us.sentry.io/4510838905503744
Environment: development
Traces Sample Rate: 100% (development), 10% (production)
Send PII: Enabled (for better debugging)
```

**Features Enabled**:
- ✅ FastAPI automatic integration
- ✅ SQLAlchemy query tracking
- ✅ Performance monitoring
- ✅ User context tracking
- ✅ Request/Response logging
- ✅ Error grouping and deduplication

---

### **2. Opik AI Monitoring** ✅

**Status**: Configured with API key

**What it does**:
- Tracks AI model performance
- Monitors intervention quality
- Evaluates safety scores
- Tracks token usage and costs
- Provides AI-specific insights

**Configuration**:
```python
API Key: f4cpW5kqIzG6UuWxmphBxIcUl
Project: orbit-development
Workspace: orbit-dev
```

**Features**:
- ✅ Agent execution tracking
- ✅ Model performance metrics
- ✅ Cost tracking per request
- ✅ Quality evaluation scores
- ✅ A/B testing support

---

## 🚀 How to Use

### **Test Sentry Integration**

1. **Start the backend**:
```bash
python -m uvicorn src.main:app --reload
```

2. **Trigger a test error**:
```bash
# Open in browser or use curl
curl http://localhost:8000/sentry-debug
```

3. **Check Sentry Dashboard**:
- Go to: https://sentry.io
- Navigate to your project
- You should see the error appear within seconds
- Click on it to see full stack trace, request details, and context

### **Monitor Real Errors**

All errors are automatically captured:
```python
# Any unhandled exception will be sent to Sentry
@app.get("/api/v1/test")
async def test_endpoint():
    # This error will be automatically captured
    raise ValueError("Something went wrong!")
```

### **Manual Error Tracking**

You can also manually capture errors:
```python
import sentry_sdk

try:
    risky_operation()
except Exception as e:
    # Capture with additional context
    sentry_sdk.capture_exception(e)
    sentry_sdk.set_context("custom", {
        "user_id": user_id,
        "operation": "risky_operation"
    })
```

---

## 📊 What Gets Tracked

### **Automatic Tracking**

1. **All HTTP Requests**:
   - URL, method, headers
   - Response status and time
   - User IP and location
   - Request body (if enabled)

2. **All Exceptions**:
   - Full stack trace
   - Local variables
   - Request context
   - User information

3. **Performance**:
   - API response times
   - Database query times
   - External API calls
   - Cache hit/miss rates

4. **AI Operations** (via Opik):
   - Model used
   - Token usage
   - Response quality
   - Execution time
   - Cost per request

---

## 🎯 Monitoring Endpoints

### **Health Check**
```bash
GET http://localhost:8000/health
```

Returns:
```json
{
  "status": "healthy",
  "services": {
    "redis": {"status": "healthy"},
    "database": {"status": "healthy"},
    "api": {"status": "healthy"},
    "sentry": {
      "status": "enabled",
      "environment": "development"
    }
  },
  "version": "1.0.0"
}
```

### **Sentry Debug** (Development Only)
```bash
GET http://localhost:8000/sentry-debug
```

Triggers a test error to verify Sentry integration.

### **API Root**
```bash
GET http://localhost:8000/
```

Returns platform information including monitoring status.

---

## 🔧 Configuration Options

### **Environment Variables**

```bash
# Sentry Configuration
SENTRY_DSN=https://1e7c8ab363d59011dfe897cbd193f8a7@o4510291442335744.ingest.us.sentry.io/4510838905503744

# Opik Configuration
OPIK_API_KEY=f4cpW5kqIzG6UuWxmphBxIcUl
OPIK_PROJECT_NAME=orbit-development
OPIK_WORKSPACE=orbit-dev

# Logging
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
ENABLE_METRICS=true
```

### **Sentry Settings** (in `src/main.py`)

```python
sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    
    # Sample rate for performance monitoring
    # 1.0 = 100% of transactions, 0.1 = 10%
    traces_sample_rate=1.0,  # Use 0.1 in production
    
    # Send user data (IP, headers, etc.)
    send_default_pii=True,
    
    # Environment (development, staging, production)
    environment=settings.ENVIRONMENT,
    
    # Release version for tracking
    release=f"orbit@{settings.APP_VERSION}",
    
    # Profiling sample rate (optional)
    profiles_sample_rate=0.1,
)
```

---

## 📈 Sentry Dashboard Features

### **Issues**
- View all errors grouped by type
- See frequency and impact
- Track resolution status
- Assign to team members

### **Performance**
- API endpoint response times
- Database query performance
- External API latency
- Slowest transactions

### **Releases**
- Track errors by version
- Compare error rates
- Monitor deployment impact

### **Alerts**
- Email notifications
- Slack integration
- Custom alert rules
- Threshold-based alerts

---

## 🎯 Best Practices

### **1. Error Context**

Always add context to errors:
```python
sentry_sdk.set_user({
    "id": user_id,
    "email": user_email,
    "username": username
})

sentry_sdk.set_context("goal", {
    "goal_id": goal_id,
    "domain": domain,
    "progress": progress
})
```

### **2. Custom Tags**

Add tags for filtering:
```python
sentry_sdk.set_tag("agent_type", "worker")
sentry_sdk.set_tag("model", "gemini-2.5-flash")
sentry_sdk.set_tag("domain", "health")
```

### **3. Breadcrumbs**

Track user actions:
```python
sentry_sdk.add_breadcrumb(
    category="user_action",
    message="User created goal",
    level="info",
    data={"goal_id": goal_id}
)
```

### **4. Performance Tracking**

Track custom operations:
```python
with sentry_sdk.start_transaction(op="ai_generation", name="Generate Intervention"):
    with sentry_sdk.start_span(op="worker_agent"):
        worker_response = await worker_agent.execute(...)
    
    with sentry_sdk.start_span(op="supervisor_agent"):
        supervisor_response = await supervisor_agent.execute(...)
```

---

## 💰 Cost & Limits

### **Sentry Free Tier**
- 5,000 errors/month
- 10,000 performance units/month
- 1 project
- 7-day data retention

**Current Usage**: ~0 (just configured)

### **Opik Free Tier**
- Unlimited traces
- 30-day data retention
- Basic analytics

**Current Usage**: ~0 (just configured)

---

## 🔍 Troubleshooting

### **Sentry not capturing errors**

1. Check DSN is set:
```bash
python -c "from src.core.config import settings; print(settings.SENTRY_DSN)"
```

2. Test with debug endpoint:
```bash
curl http://localhost:8000/sentry-debug
```

3. Check Sentry dashboard for events

### **Performance data not showing**

1. Increase `traces_sample_rate` to 1.0
2. Make some API requests
3. Wait 1-2 minutes for data to appear
4. Check Performance tab in Sentry

### **Too many events**

1. Reduce `traces_sample_rate` to 0.1 or lower
2. Add filters in Sentry dashboard
3. Use `before_send` hook to filter events

---

## 📚 Resources

### **Sentry**
- Dashboard: https://sentry.io
- Docs: https://docs.sentry.io/platforms/python/guides/fastapi/
- Python SDK: https://docs.sentry.io/platforms/python/

### **Opik**
- Dashboard: https://www.comet.com/site/products/opik/
- Docs: https://www.comet.com/docs/opik/
- Python SDK: https://github.com/comet-ml/opik

---

## ✅ Verification Checklist

- [x] Sentry DSN configured in `.env.local`
- [x] Sentry initialized in `src/main.py`
- [x] FastAPI integration enabled
- [x] Test endpoint created (`/sentry-debug`)
- [x] Global exception handler configured
- [x] Performance monitoring enabled
- [x] Opik API key configured
- [x] Health check includes monitoring status

---

## 🎉 You're All Set!

Your ORBIT platform now has **enterprise-grade error monitoring** with:

✅ **Automatic error capture** - All exceptions tracked  
✅ **Performance monitoring** - API response times tracked  
✅ **AI monitoring** - Model performance tracked via Opik  
✅ **Real-time alerts** - Get notified of issues immediately  
✅ **Detailed debugging** - Full context for every error  

**Test it now**:
```bash
# Start backend
python -m uvicorn src.main:app --reload

# Trigger test error
curl http://localhost:8000/sentry-debug

# Check Sentry dashboard
# You should see the error within seconds!
```

---

*Monitoring configured and ready to track everything! 🚀*
