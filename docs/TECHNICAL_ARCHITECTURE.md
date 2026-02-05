# 🏗️ ORBIT Technical Architecture
### Production-Ready AI System Design

> **Complete technical blueprint for building ORBIT's three-agent system with transparent evaluation and autonomous workflows**

---

## 🎯 System Overview

ORBIT's architecture is built on three core principles:
1. **Reliability**: Multi-agent validation with transparent evaluation
2. **Scalability**: Microservices architecture supporting millions of users
3. **Transparency**: Every AI decision logged, evaluated, and explainable

```mermaid
graph TB
    subgraph "User Layer"
        Web[🖥️ Web Dashboard]
        Mobile[📱 Mobile Apps]
        API[🔌 Public API]
    end
    
    subgraph "Application Layer"
        Gateway[🚪 API Gateway]
        Auth[🔐 Auth Service]
        UserService[👤 User Service]
        GoalService[🎯 Goal Service]
        InterventionService[⚡ Intervention Service]
    end
    
    subgraph "AI Agent Layer"
        Worker[🤖 Worker Agent<br/>Gemini 1.5 Pro]
        Supervisor[🛡️ Supervisor Agent<br/>Claude + Opik]
        Optimizer[🔧 Optimizer Agent<br/>Analysis & Learning]
    end
    
    subgraph "Automation Layer"
        N8N[⚡ n8n Workflows]
        Scheduler[⏰ Task Scheduler]
        EventBus[📡 Event Bus]
    end
    
    subgraph "Data Layer"
        PostgreSQL[(🗄️ PostgreSQL<br/>User Data)]
        Redis[(⚡ Redis<br/>Cache & Sessions)]
        Vector[(🧠 Vector DB<br/>Embeddings)]
        Opik[(📊 Opik<br/>AI Traces)]
    end
    
    subgraph "External Services"
        Integrations[🔌 External APIs<br/>Calendar, Health, Finance]
        LLMs[🤖 LLM Providers<br/>OpenAI, Anthropic, Google]
    end
    
    Web --> Gateway
    Mobile --> Gateway
    API --> Gateway
    
    Gateway --> Auth
    Gateway --> UserService
    Gateway --> GoalService
    Gateway --> InterventionService
    
    InterventionService --> Worker
    Worker --> Supervisor
    Supervisor --> Opik
    Supervisor --> Optimizer
    
    N8N --> InterventionService
    N8N --> Integrations
    EventBus --> N8N
    
    UserService --> PostgreSQL
    GoalService --> PostgreSQL
    InterventionService --> Redis
    Worker --> Vector
    
    Worker --> LLMs
    Supervisor --> LLMs
```

---

## 🤖 Three-Agent System Architecture

### 🔧 **Worker Agent: The Executor**

**Purpose**: Generate personalized interventions, plans, and content
**Model**: Gemini 1.5 Pro (primary), GPT-4 (fallback)
**Responsibilities**:
- Analyze user context and goals
- Generate daily plans and interventions
- Create personalized content and nudges
- Adapt strategies based on user feedback

```python
class WorkerAgent:
    def __init__(self):
        self.model = GeminiClient("gemini-1.5-pro")
        self.context_manager = ContextManager()
        self.personalization_engine = PersonalizationEngine()
    
    async def generate_intervention(self, user_id: str, context: Dict) -> Intervention:
        # Gather user context
        user_profile = await self.context_manager.get_user_profile(user_id)
        current_state = await self.context_manager.get_current_state(user_id)
        
        # Generate intervention
        prompt = self.build_intervention_prompt(user_profile, current_state, context)
        response = await self.model.generate(prompt)
        
        # Parse and structure intervention
        intervention = self.parse_intervention(response)
        intervention.metadata = {
            "model": "gemini-1.5-pro",
            "timestamp": datetime.utcnow(),
            "context": context
        }
        
        return intervention
```

### 🛡️ **Supervisor Agent: The Guardian**

**Purpose**: Real-time quality control and safety validation
**Model**: Claude Sonnet (evaluation) + Opik (logging)
**Evaluation Dimensions**:

```python
class SupervisorAgent:
    def __init__(self):
        self.evaluator = ClaudeClient("claude-3-sonnet")
        self.opik_client = OpikClient()
        self.safety_checker = SafetyChecker()
    
    async def evaluate_intervention(self, intervention: Intervention, user_context: Dict) -> EvaluationResult:
        # Multi-dimensional evaluation
        evaluation = await asyncio.gather(
            self.evaluate_safety(intervention, user_context),
            self.evaluate_relevance(intervention, user_context),
            self.evaluate_accuracy(intervention),
            self.evaluate_adherence_probability(intervention, user_context),
            self.evaluate_engagement_quality(intervention, user_context)
        )
        
        # Aggregate scores
        result = EvaluationResult(
            safety_score=evaluation[0],
            relevance_score=evaluation[1],
            accuracy_score=evaluation[2],
            adherence_probability=evaluation[3],
            engagement_quality=evaluation[4],
            overall_score=self.calculate_weighted_score(evaluation),
            timestamp=datetime.utcnow()
        )
        
        # Log to Opik
        await self.opik_client.log_evaluation(intervention, result)
        
        # Safety check
        if result.safety_score < 0.8 or result.overall_score < 0.6:
            await self.handle_low_quality_intervention(intervention, result)
        
        return result
```

### 🔧 **Optimizer Agent: The Learner**

**Purpose**: Continuous improvement through pattern analysis
**Capabilities**:
- Weekly Opik trace analysis
- A/B test result evaluation
- Prompt optimization
- Strategy refinement

```python
class OptimizerAgent:
    def __init__(self):
        self.analyzer = PatternAnalyzer()
        self.opik_client = OpikClient()
        self.ab_tester = ABTester()
    
    async def weekly_optimization(self):
        # Fetch week's traces
        traces = await self.opik_client.get_traces(
            start_date=datetime.utcnow() - timedelta(days=7)
        )
        
        # Analyze patterns
        analysis = await self.analyzer.analyze_traces(traces)
        
        # Identify improvement opportunities
        improvements = self.identify_improvements(analysis)
        
        # Generate optimization recommendations
        recommendations = await self.generate_recommendations(improvements)
        
        # Implement approved optimizations
        await self.implement_optimizations(recommendations)
        
        return OptimizationReport(
            analysis=analysis,
            improvements=improvements,
            recommendations=recommendations
        )
```

---

## ⚡ n8n Workflow Architecture

### 🌅 **Morning Orchestrator Workflow**

```json
{
  "name": "Morning Orchestrator",
  "nodes": [
    {
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.cron",
      "parameters": {
        "rule": {
          "hour": 7,
          "minute": 0
        }
      }
    },
    {
      "name": "Get User Context",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "{{$env.ORBIT_API_URL}}/api/users/{{$json.user_id}}/context",
        "method": "GET"
      }
    },
    {
      "name": "Check Calendar",
      "type": "n8n-nodes-base.googleCalendar",
      "parameters": {
        "operation": "getAll",
        "timeMin": "{{$now}}",
        "timeMax": "{{$now.plus({days: 1})}}"
      }
    },
    {
      "name": "Get Weather",
      "type": "n8n-nodes-base.openWeatherMap",
      "parameters": {
        "operation": "currentWeather",
        "location": "{{$json.user_location}}"
      }
    },
    {
      "name": "Generate Daily Plan",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "{{$env.ORBIT_API_URL}}/api/ai/generate-daily-plan",
        "method": "POST",
        "body": {
          "user_id": "{{$json.user_id}}",
          "calendar": "{{$json.calendar_events}}",
          "weather": "{{$json.weather}}",
          "context": "{{$json.user_context}}"
        }
      }
    },
    {
      "name": "Supervisor Evaluation",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "{{$env.ORBIT_API_URL}}/api/ai/evaluate",
        "method": "POST",
        "body": {
          "intervention": "{{$json.daily_plan}}",
          "user_context": "{{$json.user_context}}"
        }
      }
    },
    {
      "name": "Send to User",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "{{$env.ORBIT_API_URL}}/api/notifications/send",
        "method": "POST",
        "body": {
          "user_id": "{{$json.user_id}}",
          "type": "morning_briefing",
          "content": "{{$json.daily_plan}}",
          "evaluation": "{{$json.evaluation}}"
        }
      }
    }
  ]
}
```

### ⚡ **Real-Time Intervention Monitor**

```json
{
  "name": "Real-Time Intervention Monitor",
  "nodes": [
    {
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "intervention-trigger"
      }
    },
    {
      "name": "Context Gathering",
      "type": "n8n-nodes-base.function",
      "parameters": {
        "functionCode": `
          const context = {
            user_id: $json.user_id,
            trigger_event: $json.event,
            timestamp: new Date().toISOString(),
            location: $json.location,
            recent_activity: $json.recent_activity
          };
          
          return { context };
        `
      }
    },
    {
      "name": "Decision Engine",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "{{$env.ORBIT_API_URL}}/api/ai/should-intervene",
        "method": "POST",
        "body": "{{$json.context}}"
      }
    },
    {
      "name": "Generate Intervention",
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "boolean": [
            {
              "value1": "{{$json.should_intervene}}",
              "value2": true
            }
          ]
        }
      }
    },
    {
      "name": "Worker Agent",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "{{$env.ORBIT_API_URL}}/api/ai/generate-intervention",
        "method": "POST",
        "body": "{{$json.context}}"
      }
    },
    {
      "name": "Supervisor Validation",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "{{$env.ORBIT_API_URL}}/api/ai/evaluate",
        "method": "POST",
        "body": {
          "intervention": "{{$json.intervention}}",
          "context": "{{$json.context}}"
        }
      }
    },
    {
      "name": "Execute Intervention",
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "number": [
            {
              "value1": "{{$json.evaluation.overall_score}}",
              "operation": "larger",
              "value2": 0.7
            }
          ]
        }
      }
    }
  ]
}
```

---

## 🗄️ Database Schema

### **Core Tables**

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    profile JSONB,
    preferences JSONB,
    timezone VARCHAR(50),
    subscription_tier VARCHAR(20) DEFAULT 'starter'
);

-- Goals table
CREATE TABLE goals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    domain VARCHAR(50) NOT NULL, -- health, finance, productivity, learning, social
    title VARCHAR(255) NOT NULL,
    description TEXT,
    target_value NUMERIC,
    current_value NUMERIC DEFAULT 0,
    unit VARCHAR(50),
    deadline DATE,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB
);

-- Interventions table
CREATE TABLE interventions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    goal_id UUID REFERENCES goals(id),
    type VARCHAR(50) NOT NULL, -- nudge, plan, friction, reward
    content JSONB NOT NULL,
    trigger_context JSONB,
    generated_at TIMESTAMP DEFAULT NOW(),
    delivered_at TIMESTAMP,
    user_response VARCHAR(20), -- accepted, dismissed, modified
    response_at TIMESTAMP,
    effectiveness_score NUMERIC,
    metadata JSONB
);

-- Evaluations table (Opik integration)
CREATE TABLE evaluations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    intervention_id UUID REFERENCES interventions(id),
    safety_score NUMERIC(3,2),
    relevance_score NUMERIC(3,2),
    accuracy_score NUMERIC(3,2),
    adherence_probability NUMERIC(3,2),
    engagement_quality NUMERIC(3,2),
    overall_score NUMERIC(3,2),
    evaluator_model VARCHAR(100),
    evaluation_reasoning TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    opik_trace_id VARCHAR(255)
);

-- User context table
CREATE TABLE user_context (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    context_type VARCHAR(50), -- calendar, health, finance, location
    data JSONB NOT NULL,
    source VARCHAR(100),
    collected_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
);

-- Integrations table
CREATE TABLE integrations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    service_name VARCHAR(100) NOT NULL,
    service_type VARCHAR(50), -- calendar, health, finance, productivity
    credentials JSONB, -- encrypted
    settings JSONB,
    status VARCHAR(20) DEFAULT 'active',
    last_sync TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### **Indexes for Performance**

```sql
-- User queries
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_subscription ON users(subscription_tier);

-- Goal queries
CREATE INDEX idx_goals_user_domain ON goals(user_id, domain);
CREATE INDEX idx_goals_status ON goals(status);
CREATE INDEX idx_goals_deadline ON goals(deadline);

-- Intervention queries
CREATE INDEX idx_interventions_user_time ON interventions(user_id, generated_at);
CREATE INDEX idx_interventions_goal ON interventions(goal_id);
CREATE INDEX idx_interventions_type ON interventions(type);

-- Evaluation queries
CREATE INDEX idx_evaluations_intervention ON evaluations(intervention_id);
CREATE INDEX idx_evaluations_scores ON evaluations(overall_score, created_at);

-- Context queries
CREATE INDEX idx_context_user_type ON user_context(user_id, context_type);
CREATE INDEX idx_context_expires ON user_context(expires_at);
```

---

## 🔒 Security & Privacy Architecture

### **Data Protection**

```python
class SecurityManager:
    def __init__(self):
        self.encryption_key = os.getenv('ENCRYPTION_KEY')
        self.jwt_secret = os.getenv('JWT_SECRET')
    
    def encrypt_sensitive_data(self, data: Dict) -> str:
        """Encrypt PII and sensitive information"""
        cipher = Fernet(self.encryption_key)
        return cipher.encrypt(json.dumps(data).encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> Dict:
        """Decrypt sensitive information"""
        cipher = Fernet(self.encryption_key)
        return json.loads(cipher.decrypt(encrypted_data.encode()).decode())
    
    def generate_jwt_token(self, user_id: str, permissions: List[str]) -> str:
        """Generate JWT token with specific permissions"""
        payload = {
            'user_id': user_id,
            'permissions': permissions,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
```

### **Privacy Controls**

```python
class PrivacyManager:
    def __init__(self):
        self.data_retention_policies = {
            'user_context': timedelta(days=30),
            'interventions': timedelta(days=365),
            'evaluations': timedelta(days=730)
        }
    
    async def anonymize_user_data(self, user_id: str):
        """GDPR-compliant data anonymization"""
        # Replace PII with anonymous identifiers
        await self.db.execute("""
            UPDATE users 
            SET email = 'deleted_' || id::text || '@example.com',
                profile = '{"anonymized": true}'
            WHERE id = $1
        """, user_id)
    
    async def export_user_data(self, user_id: str) -> Dict:
        """Export all user data for GDPR compliance"""
        return {
            'user_profile': await self.get_user_profile(user_id),
            'goals': await self.get_user_goals(user_id),
            'interventions': await self.get_user_interventions(user_id),
            'context_data': await self.get_user_context(user_id)
        }
```

---

## 📊 Monitoring & Observability

### **Application Monitoring**

```python
class MonitoringManager:
    def __init__(self):
        self.prometheus = PrometheusClient()
        self.sentry = SentryClient()
        self.datadog = DatadogClient()
    
    def track_intervention_metrics(self, intervention: Intervention, evaluation: EvaluationResult):
        """Track key intervention metrics"""
        self.prometheus.counter('interventions_generated_total').inc()
        self.prometheus.histogram('intervention_evaluation_score').observe(evaluation.overall_score)
        self.prometheus.gauge('user_goal_completion_rate').set(self.calculate_completion_rate())
    
    def track_ai_performance(self, model: str, response_time: float, tokens_used: int):
        """Track AI model performance"""
        self.prometheus.histogram('ai_response_time_seconds', ['model']).labels(model=model).observe(response_time)
        self.prometheus.counter('ai_tokens_used_total', ['model']).labels(model=model).inc(tokens_used)
    
    def alert_on_anomalies(self, metric: str, value: float, threshold: float):
        """Alert on performance anomalies"""
        if value > threshold:
            self.sentry.capture_message(f"Anomaly detected: {metric} = {value} > {threshold}")
```

### **Health Checks**

```python
@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint"""
    checks = {
        'database': await check_database_connection(),
        'redis': await check_redis_connection(),
        'ai_models': await check_ai_model_availability(),
        'external_apis': await check_external_integrations(),
        'n8n_workflows': await check_n8n_status()
    }
    
    overall_status = 'healthy' if all(checks.values()) else 'unhealthy'
    
    return {
        'status': overall_status,
        'timestamp': datetime.utcnow().isoformat(),
        'checks': checks,
        'version': os.getenv('APP_VERSION', 'unknown')
    }
```

---

## 🚀 Deployment Architecture

### **Container Configuration**

```dockerfile
# Dockerfile for ORBIT API
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash orbit
USER orbit

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Docker Compose for Development**

```yaml
version: '3.8'

services:
  orbit-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://orbit:password@postgres:5432/orbit
      - REDIS_URL=redis://redis:6379
      - OPIK_API_KEY=${OPIK_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    depends_on:
      - postgres
      - redis
    volumes:
      - ./:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=orbit
      - POSTGRES_USER=orbit
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=password
      - WEBHOOK_URL=http://localhost:5678/
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  postgres_data:
  redis_data:
  n8n_data:
```

### **Kubernetes Production Deployment**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orbit-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: orbit-api
  template:
    metadata:
      labels:
        app: orbit-api
    spec:
      containers:
      - name: orbit-api
        image: orbit/api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: orbit-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: orbit-secrets
              key: redis-url
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: orbit-api-service
spec:
  selector:
    app: orbit-api
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

This technical architecture provides the foundation for building ORBIT as a production-ready AI platform. The three-agent system ensures reliability, the n8n workflows enable automation, and the comprehensive monitoring ensures operational excellence.

Want me to continue with the implementation of specific components or dive deeper into any particular aspect?
