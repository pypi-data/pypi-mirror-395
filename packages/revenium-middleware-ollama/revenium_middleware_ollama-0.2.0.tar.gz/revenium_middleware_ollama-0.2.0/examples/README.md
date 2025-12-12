# Revenium Ollama Middleware Examples

This directory contains practical examples demonstrating how to use the Revenium Ollama middleware for usage tracking and metadata.

## Quick Start

### Setup (One-time)

1. Create virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install revenium-middleware-ollama
```

3. Copy the environment template:
```bash
cd examples
cp ../.env.example .env
```

4. Edit `.env` and add your Revenium API key:
```bash
# Revenium API keys
REVENIUM_METERING_API_KEY="hak_..."
REVENIUM_METERING_BASE_URL="https://api.revenium.ai"

# Ollama is local - no API key needed
# Ensure Ollama is running: ollama serve

# Optional: Enable debug logging
# REVENIUM_LOG_LEVEL="DEBUG"
```

5. Ensure Ollama is running:
```bash
ollama serve
```

### Run Examples

```bash
# Simple usage
python example_simple.py

# Usage with metadata
python example_metadata.py

# Streaming responses
python example_streaming.py

# Getting started example
python getting_started.py
```

## Examples

### 1. example_simple.py

**What it demonstrates:** Basic middleware usage

**Description:**
The simplest example showing how to use the middleware with basic Ollama requests. Perfect for getting started.

**How to run:**
```bash
python example_simple.py
```

**Expected output:**
```
================================================================================
SIMPLE REQUEST EXAMPLE
================================================================================

Question: What is 2+2?
Answer: 2+2 equals 4. This is the standard mathematical addition of two numbers.

Transaction ID: ollama-1761658969.464719

Usage is automatically tracked in Revenium dashboard.

================================================================================
```

**Key points:**
- Minimal setup required
- Automatic usage tracking
- Works with all Ollama models
- Transaction ID available in response if needed

---

### 2. example_metadata.py

**What it demonstrates:** Enhanced tracking with metadata

**Description:**
Shows how to send custom metadata with requests for advanced tracking and reporting in Revenium. Metadata helps you categorize and analyze usage by subscriber, organization, task type, and more.

**How to run:**
```bash
python example_metadata.py
```

**Expected output:**
```
================================================================================
REQUEST WITH METADATA
================================================================================

Question: Explain Python in 5 words.
Answer: Python is an interpreted language...

Metadata sent with this request:
  - Subscriber ID: user-12345
  - Subscriber Email: user@example.com
  - Trace ID: trace-abc-123
  - Task Type: explanation
  - Organization ID: org-demo

In Revenium, you can now:
  - Filter requests by subscriber, organization, or task type
  - Correlate with your distributed tracing system using trace_id
  - Analyze usage patterns by task type
  - Track costs per subscriber or organization

================================================================================
```

**Metadata fields:**
- `trace_id`: Correlate with distributed tracing systems
- `task_type`: Categorize requests by operation type
- `subscriber`: Track usage by user/API key
- `organization_id`: Track usage by customer/department
- `subscription_id`: Track usage by billing plan
- `product_id`: Track usage by product/feature
- `agent`: Track usage by AI agent

---

### 3. example_streaming.py

**What it demonstrates:** Streaming responses

**Description:**
Demonstrates how the middleware works with streaming responses. The middleware tracks the entire stream as a single request in Revenium.

**How to run:**
```bash
python example_streaming.py
```

**Expected output:**
```
================================================================================
STREAMING REQUEST EXAMPLE
================================================================================

Question: Count to 5.
Answer (streaming): Sure! Here's the count up to 5:
1, 2, 3, 4, 5

Total chunks received: 25

In Revenium, this stream will be recorded as:
  - Single transaction
  - Total tokens for the entire stream
  - Complete request/response metadata

================================================================================
```

**Key points:**
- Streaming mode works seamlessly with the middleware
- Entire stream tracked as one request
- All chunks share the same transaction ID
- Useful for long-running requests

---

### 4. getting_started.py

**What it demonstrates:** Minimal setup example

**Description:**
A minimal example showing the bare minimum code needed to use the middleware. Great for quickly integrating into your project.

**How to run:**
```bash
python getting_started.py
```

**Expected output:**
```
Of course! I'm ready to help with your question or inquiry. Just let me know what you need assistance with and we can proceed from there.
```

**Key points:**
- Minimal code required
- Middleware works automatically
- Optional metadata support (commented out)
- Ready to customize for your use case

---

## Common Use Cases

### Use Case 1: Track Usage by User

```python
response = ollama.chat(
    model='qwen2.5:0.5b',
    messages=[{'role': 'user', 'content': 'Hello!'}],
    usage_metadata={
        "subscriber": {
            "id": "user-123",
            "email": "user@example.com"
        }
    }
)
```

### Use Case 2: Correlate with Distributed Tracing

```python
response = ollama.chat(
    model='qwen2.5:0.5b',
    messages=[{'role': 'user', 'content': 'Hello!'}],
    usage_metadata={
        "trace_id": "trace-abc-123"  # From your tracing system
    }
)
```

### Use Case 3: Categorize by Task Type

```python
response = ollama.chat(
    model='qwen2.5:0.5b',
    messages=[{'role': 'user', 'content': 'Summarize this...'}],
    usage_metadata={
        "task_type": "summarization"
    }
)
```

### Use Case 4: Track by Organization

```python
response = ollama.chat(
    model='qwen2.5:0.5b',
    messages=[{'role': 'user', 'content': 'Hello!'}],
    usage_metadata={
        "organization_id": "acme-corp"
    }
)
```

---

## Troubleshooting

### Error: REVENIUM_METERING_API_KEY not set

**Solution:** Make sure your `.env` file exists and contains:
```bash
REVENIUM_METERING_API_KEY="hak_your_api_key_here"
```

### Error: Model not found

**Solution:** Ensure the model is available in Ollama:
```bash
ollama list
```

If the model isn't listed, pull it:
```bash
ollama pull qwen2.5:0.5b
```

### Error: Connection refused

**Solution:** Make sure Ollama is running:
```bash
ollama serve
```

### Middleware not tracking requests

**Solution:** Ensure the middleware is imported:
```python
import revenium_middleware_ollama
```

This must be imported after `import ollama` to properly wrap the API calls.

---

## Questions or Issues?

For more information:
- Visit [docs.revenium.io](https://docs.revenium.io)
- Check the main [README.md](https://github.com/revenium/revenium-middleware-ollama-python/blob/HEAD/README.md)
- See [CONTRIBUTING.md](https://github.com/revenium/revenium-middleware-ollama-python/blob/HEAD/CONTRIBUTING.md)
