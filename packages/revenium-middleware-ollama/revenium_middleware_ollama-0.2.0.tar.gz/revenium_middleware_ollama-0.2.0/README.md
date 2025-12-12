# Revenium Middleware for Ollama

[![PyPI version](https://img.shields.io/pypi/v/revenium-middleware-ollama.svg)](https://pypi.org/project/revenium-middleware-ollama/)
[![Python Versions](https://img.shields.io/pypi/pyversions/revenium-middleware-ollama.svg)](https://pypi.org/project/revenium-middleware-ollama/)
[![Documentation](https://img.shields.io/badge/docs-revenium.io-blue)](https://docs.revenium.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[//]: # ([![Build Status]&#40;https://github.com/revenium/revenium-middleware-ollama/actions/workflows/ci.yml/badge.svg&#41;]&#40;https://github.com/revenium/revenium-middleware-ollama/actions&#41;)

A middleware library for metering and monitoring Ollama API usage in Python applications.

## Features

- **Precise Usage Tracking**: Monitor tokens, costs, and request counts across all Ollama API endpoints
- **Seamless Integration**: Drop-in middleware that works with minimal code changes
- **Flexible Configuration**: Customize metering behavior to suit your application needs
- **Rich Metadata Support**: Track usage by subscriber, organization, task type, and more

## Installation

```bash
pip install revenium-middleware-ollama
```

## Quick Start

**For complete examples and setup instructions, see [`examples/README.md`](examples/README.md).**

### 1. Create Project Directory

```bash
# Create project directory and navigate to it
mkdir my-ollama-project
cd my-ollama-project
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Package

```bash
pip install revenium-middleware-ollama
```

### 4. Configure Environment Variables

Create a `.env` file in your project directory:

```bash
# Revenium API keys
REVENIUM_METERING_API_KEY="hak_..."
REVENIUM_METERING_BASE_URL="https://api.revenium.ai"

# Ollama is local - no API key needed
# Ensure Ollama is running: ollama serve

# Optional: Enable debug logging
# REVENIUM_LOG_LEVEL="DEBUG"
```

### 5. Run Your First Example

Download and run an example from the repository:

```bash
curl -O https://raw.githubusercontent.com/revenium/revenium-middleware-ollama-python/main/examples/getting_started.py
python getting_started.py
```

Or use this simple code:

```python
from dotenv import load_dotenv
load_dotenv()

import ollama
import revenium_middleware_ollama

# Ensure REVENIUM_METERING_API_KEY is set in your .env file
# Ensure Ollama is running (ollama serve)

response: ollama.ChatResponse = ollama.chat(
    model='qwen2.5:0.5b',
    messages=[{'role': 'user', 'content': 'Please verify you are ready to assist me.'}]
)
print(response['message']['content'])
```

**That's it!** The middleware automatically meters all Ollama API calls. No code changes required.

**For complete examples and setup instructions, see [`examples/README.md`](examples/README.md).**

- [`examples/getting_started.py`](examples/getting_started.py) - Minimal example with automatic metering
- [`examples/example_simple.py`](examples/example_simple.py) - Basic middleware usage
- [`examples/example_metadata.py`](examples/example_metadata.py) - Enhanced tracking with metadata
- [`examples/example_streaming.py`](examples/example_streaming.py) - Streaming responses

## Usage

### Zero-Config Integration

Simply set your REVENIUM_METERING_API_KEY in your `.env` file and import the middleware.
Your Ollama calls will be metered automatically:

```python
from dotenv import load_dotenv
load_dotenv()

import ollama
import revenium_middleware_ollama

# Ensure REVENIUM_METERING_API_KEY is set in your .env file

response: ollama.ChatResponse = ollama.chat(
    model='qwen2.5:0.5b', messages=[
        {
            'role': 'user',
            'content': 'Why is the sky blue?',
        },
    ])
print(response['message']['content'])
```

The middleware automatically intercepts Ollama API calls and sends metering data to Revenium without requiring any
changes to your existing code.

### Enhanced Tracking with Metadata

For more granular usage tracking and detailed reporting, add the `usage_metadata` parameter:

```python
from dotenv import load_dotenv
load_dotenv()

import ollama
import revenium_middleware_ollama

response = ollama.chat(
    model='qwen2.5:0.5b', messages=[
        {
            'role': 'user',
            'content': 'Why is the sky blue?',
        },
    ],
    usage_metadata={
         "trace_id": "conv-28a7e9d4",
         "task_type": "summarize-customer-issue",
         "subscriber": {
             "id": "subscriberid-1234567890",
             "email": "user@example.com",
             "credential": {
                 "name": "engineering-api-key",
                 "value": "sk-1234567890abcdef"
             }
         },
         "organization_id": "acme-corp",
         "subscription_id": "startup-plan-Q1",
         "product_id": "saas-app-gold-tier",
         "agent": "support-agent",
    },
)
print(response['message']['content'])
```

### OpenAI Compatibility Mode

The middleware can also be used with Ollama's OpenAI [compatibility mode.](https://ollama.com/blog/openai-compatibility) 



```python
import openai
import revenium_middleware_openai

openai.api_key = 'ollama'
openai.base_url = 'http://localhost:11434/v1/'
question = "Why is the sky blue?"

response = openai.chat.completions.create(
    model="gemma2:2b",
    messages=[
       {"role": "system", "content": "You are a helpful assistant."},
       {"role": "user", "content": question}
    ],
    usage_metadata={
         "trace_id": "conv-28a7e9d4",
         "task_type": "summarize-customer-issue",
         "subscriber": {
             "id": "subscriberid-1234567890",
             "email": "user@example.com",
             "credential": {
                 "name": "engineering-api-key",
                 "value": "sk-1234567890abcdef"
             }
         },
         "organization_id": "acme-corp",
         "subscription_id": "startup-plan-Q1",
         "product_id": "saas-app-gold-tier",
         "agent": "support-agent",
    }
)

print(response)
```

#### Metadata Fields

The `usage_metadata` parameter supports the following fields:

| Field                        | Description                                               | Use Case                                                          |
|------------------------------|-----------------------------------------------------------|-------------------------------------------------------------------|
| `trace_id`                   | Unique identifier for a conversation or session           | Group multi-turn conversations into single event for performance & cost tracking                           |
| `task_type`                  | Classification of the AI operation by type of work        | Track cost & performance by purpose (e.g., classification, summarization)                                  |
| `subscriber`                 | Object containing subscriber information                   | Track cost & performance by individual users or API keys                                                   |
| `subscriber.id`              | The id of the subscriber from non-Revenium systems        | Track cost & performance by individual users (if customers are anonymous or tracking by emails is not desired)   |
| `subscriber.email`           | The email address of the subscriber                       | Track cost & performance by individual users (if customer e-mail addresses are known)                      |
| `subscriber.credential`      | Object containing credential information                   | Track cost & performance by API key                                                                        |
| `subscriber.credential.name` | An alias for an API key used by one or more users         | Track cost & performance by individual API keys                                                            |
| `subscriber.credential.value`| The key value associated with the subscriber (i.e an API key)     | Track cost & performance by API key value (normally used when the only identifier for a user is an API key) |
| `organization_id`            | Customer or department ID from non-Revenium systems       | Track cost & performance by customers or business units                                                    |
| `subscription_id`            | Reference to a billing plan in non-Revenium systems       | Track cost & performance by a specific subscription                                                        |
| `product_id`                 | Your product or feature making the AI call                | Track cost & performance across different products                                                         |
| `agent`                      | Identifier for the specific AI agent                      | Track cost & performance performance by AI agent                                                           |
| `response_quality_score`     | Custom quality rating for the AI response (0.0-1.0 scale) | Track user satisfaction or automated quality metrics (e.g., RAGAS, human feedback) for model performance analysis |

**All metadata fields are optional**. Adding them enables more detailed reporting and analytics in Revenium.

### Trace Visualization Fields (v0.2.0+)

Enhanced observability fields for distributed tracing and analytics. These can be set via environment variables or passed in `usage_metadata`:

| Field | Environment Variable | Description | Use Case |
|-------|---------------------|-------------|----------|
| `environment` | `REVENIUM_ENVIRONMENT` | Deployment environment (e.g., "production", "staging") | Track usage across different deployment environments; auto-detects from `ENVIRONMENT`, `DEPLOYMENT_ENV` |
| `region` | `REVENIUM_REGION` | Cloud region identifier (e.g., "us-east-1", "eastus") | Multi-region deployment tracking; auto-detects from `AWS_REGION`, `AZURE_REGION`, `GCP_REGION` |
| `credential_alias` | `REVENIUM_CREDENTIAL_ALIAS` | Human-readable API key name (e.g., "prod-ollama-key") | Track which credential was used for credential rotation and security auditing |
| `trace_type` | `REVENIUM_TRACE_TYPE` | Workflow category identifier (max 128 chars) | Group similar workflows (e.g., "customer-support", "data-analysis") for analytics |
| `trace_name` | `REVENIUM_TRACE_NAME` | Human-readable trace label (max 256 chars) | Label trace instances (e.g., "Customer Support Chat", "Document Analysis") |
| `parent_transaction_id` | `REVENIUM_PARENT_TRANSACTION_ID` | Parent transaction ID for distributed tracing | Link child operations to parent transactions across services |
| `transaction_name` | `REVENIUM_TRANSACTION_NAME` | Human-friendly operation name | Label individual operations (e.g., "Generate Response", "Analyze Sentiment") |

**Note:** `operation_type` and `operation_subtype` are automatically detected by the middleware based on the API endpoint and request parameters.

**Resources:**
- [API Reference](https://revenium.readme.io/reference/meter_ai_completion) - Complete metadata field documentation
- [`.env.example`](.env.example) - Environment variable configuration examples
- [`examples/trace_visualization_example.py`](examples/trace_visualization_example.py) - Comprehensive trace visualization examples

### Response Attributes

Response objects include a `_revenium_transaction_id` attribute for correlating requests with Revenium metering records:

```python
response = ollama.chat(
    model='qwen2.5:0.5b',
    messages=[{'role': 'user', 'content': 'Hello!'}]
)

# Access transaction ID if needed for debugging/correlation
transaction_id = response._revenium_transaction_id
```

## Configuration

### Configuration Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `REVENIUM_METERING_API_KEY` | Yes | Your Revenium API key for authentication with the metering service |
| `REVENIUM_METERING_BASE_URL` | No | Revenium API base URL. Defaults to `https://api.revenium.ai` |
| `REVENIUM_LOG_LEVEL` | No | Log level for middleware output. Options: `DEBUG`, `INFO` (default), `WARNING`, `ERROR`, `CRITICAL` |

### Environment Setup Examples

**Using a `.env` file (Recommended):**

First, copy the example file:
```bash
cp .env.example .env
```

Then edit `.env` with your actual API key:
```bash
# Revenium API keys
REVENIUM_METERING_API_KEY="hak_..."
REVENIUM_METERING_BASE_URL="https://api.revenium.ai"

# Ollama is local - no API key needed
# Ensure Ollama is running: ollama serve

# Optional: Enable debug logging
# REVENIUM_LOG_LEVEL="DEBUG"
```

**⚠️ Security Note:** Never commit your `.env` file to version control. It's already included in `.gitignore`.

Then load it in your Python code:
```python
from dotenv import load_dotenv
load_dotenv()

import ollama
import revenium_middleware_ollama

# Your Ollama calls will now be metered
```

## Compatibility

- Python 3.8+
- Ollama Python SDK 1.0.0+

## Supported Models

This middleware works with any Ollama model. Examples in this package use:
- `qwen2.5:0.5b`, `qwen2.5:1.5b` (Qwen models)
- `llama3.1`, `llama3.2` (Llama models)
- `gemma2`, `codellama` (Other popular models)

For the complete list of available models, see the [Ollama Model Library](https://ollama.com/library).

For cost tracking across providers, see the [Revenium Model Catalog](https://docs.revenium.io).

## Logging

This module uses Python's standard logging system. You can control the log level by setting the `REVENIUM_LOG_LEVEL` environment variable in your `.env` file:

```bash
# Add to your .env file
REVENIUM_LOG_LEVEL="DEBUG"
```

Or when running your script:
```bash
REVENIUM_LOG_LEVEL=DEBUG python your_script.py
```

Available log levels:
- `DEBUG`: Detailed debugging information
- `INFO`: General information (default)
- `WARNING`: Warning messages only
- `ERROR`: Error messages only
- `CRITICAL`: Critical error messages only

## Documentation

For detailed documentation, visit [docs.revenium.io](https://docs.revenium.io)

## Contributing

See [CONTRIBUTING.md](https://github.com/revenium/revenium-middleware-ollama-python/blob/HEAD/CONTRIBUTING.md)

## Code of Conduct

See [CODE_OF_CONDUCT.md](https://github.com/revenium/revenium-middleware-ollama-python/blob/HEAD/CODE_OF_CONDUCT.md)

## Security

See [SECURITY.md](https://github.com/revenium/revenium-middleware-ollama-python/blob/HEAD/SECURITY.md)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/revenium/revenium-middleware-ollama-python/blob/HEAD/LICENSE) file for details.

## Acknowledgments

- Built by the Revenium team
