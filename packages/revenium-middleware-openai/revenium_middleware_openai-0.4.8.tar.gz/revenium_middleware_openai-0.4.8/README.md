# Revenium Middleware for OpenAI

[![PyPI version](https://img.shields.io/pypi/v/revenium-middleware-openai.svg)](https://pypi.org/project/revenium-middleware-openai/)
[![Python Versions](https://img.shields.io/pypi/pyversions/revenium-middleware-openai.svg)](https://pypi.org/project/revenium-middleware-openai/)
[![Documentation](https://img.shields.io/badge/docs-revenium.io-blue)](https://docs.revenium.io)
[![Website](https://img.shields.io/badge/website-revenium.ai-blue)](https://www.revenium.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Transparent Python middleware for automatic Revenium usage tracking with OpenAI**

A professional-grade Python middleware that seamlessly integrates with OpenAI and Azure OpenAI to provide automatic usage tracking, billing analytics, and comprehensive metadata collection. Features drop-in integration with zero code changes required and supports both Chat Completions and Embeddings APIs.

## Features

- **Seamless Integration** - Drop-in middleware, just import and go
- **Optional Metadata** - Track users, organizations, and business context (all fields optional)
- **Multiple API Support** - Chat Completions and Embeddings
- **Azure OpenAI Support** - Full Azure OpenAI integration with automatic model resolution
- **LangChain Integration** - Native support for LangChain with async detection
- **Streaming Support** - Handles regular and streaming requests seamlessly
- **Fire-and-Forget** - Never blocks your application flow
- **Accurate Pricing** - Automatic model name resolution for precise cost calculation

## Getting Started

**For complete examples and setup instructions, see [`examples/README.md`](https://github.com/revenium/revenium-middleware-openai-python/blob/HEAD/examples/README.md)**

### 1. Create Project Directory

```bash
# Create project directory and navigate to it
mkdir my-openai-project
cd my-openai-project
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
# Install packages (run after activation)
pip install revenium-middleware-openai

# For LangChain support
pip install revenium-middleware-openai[langchain]
```

### 4. Configure Environment Variables

Create a `.env` file in your project root. See [`.env.example`](.env.example) for all available configuration options.

**Minimum required configuration:**

```env
REVENIUM_METERING_API_KEY=hak_your_revenium_api_key_here
REVENIUM_METERING_BASE_URL=https://api.revenium.ai
OPENAI_API_KEY=sk_your_openai_api_key_here
```

**NOTE: Replace the placeholder values with your actual API keys.**

### 5. Run Your First Example

Download and run an example from the repository:

```bash
curl -O https://raw.githubusercontent.com/revenium/revenium-middleware-openai-python/main/examples/getting_started.py
python getting_started.py
```

Or use this simple code:

```python
from dotenv import load_dotenv
import openai
import revenium_middleware_openai  # Auto-initializes on import

load_dotenv()  # Load environment variables from .env file
client = openai.OpenAI()
# Your OpenAI API calls here - automatically metered
```

**That's it!** The middleware automatically meters all OpenAI API calls.

**For complete examples and setup instructions, see [`examples/README.md`](https://github.com/revenium/revenium-middleware-openai-python/blob/HEAD/examples/README.md)**

---

## Requirements

- Python 3.8+
- OpenAI Python SDK 1.0.0+
- Works with all OpenAI models and endpoints
- Works with all Azure OpenAI deployments

---

## What Gets Tracked

The middleware automatically captures comprehensive usage data:

### **Usage Metrics**

- **Token Counts** - Input tokens, output tokens, total tokens
- **Model Information** - Model name, provider (OpenAI/Azure), API version
- **Request Timing** - Request duration, response time
- **Cost Calculation** - Estimated costs based on current pricing

### **Business Context (Optional)**

- **User Tracking** - Subscriber ID, email, credentials
- **Organization Data** - Organization ID, subscription ID, product ID
- **Task Classification** - Task type, agent identifier, trace ID
- **Quality Metrics** - Response quality scores, task identifiers

### **Technical Details**

- **API Endpoints** - Chat completions, embeddings
- **Request Types** - Streaming vs non-streaming
- **Error Tracking** - Failed requests, error types
- **Provider Info** - OpenAI vs Azure OpenAI detection

## Metadata Fields

Add business context to track usage by organization, user, task type, or custom fields. Pass a `usage_metadata` dictionary with any of these optional fields:

| Field | Description | Use Case |
|-------|-------------|----------|
| `trace_id` | Unique identifier for session or conversation tracking | Link multiple API calls together for debugging, user session analytics, or distributed tracing across services |
| `task_type` | Type of AI task being performed | Categorize usage by workload (e.g., "chat", "code-generation", "doc-summary") for cost analysis and optimization |
| `subscriber.id` | Unique user identifier | Track individual user consumption for billing, rate limiting, or user analytics |
| `subscriber.email` | User email address | Identify users for support, compliance, or usage reports |
| `subscriber.credential.name` | Authentication credential name | Track which API key or service account made the request |
| `subscriber.credential.value` | Authentication credential value | Associate usage with specific credentials for security auditing |
| `organization_id` | Organization or company identifier | Multi-tenant cost allocation, usage quotas per organization |
| `subscription_id` | Subscription plan identifier | Track usage against subscription limits, identify plan upgrade opportunities |
| `product_id` | Your product or feature identifier | Attribute AI costs to specific features in your application (e.g., "chatbot", "email-assistant") |
| `agent` | AI agent or bot identifier | Distinguish between multiple AI agents or automation workflows in your system |
| `response_quality_score` | Custom quality rating (0.0-1.0) | Track user satisfaction or automated quality metrics for model performance analysis |

### Trace Visualization Fields (v0.4.8+)

Enhanced observability fields for distributed tracing and analytics. These can be set via environment variables or passed in `usage_metadata`:

| Field | Environment Variable | Description | Use Case |
|-------|---------------------|-------------|----------|
| `environment` | `REVENIUM_ENVIRONMENT` | Deployment environment (e.g., "production", "staging") | Track usage across different deployment environments; auto-detects from `ENVIRONMENT`, `DEPLOYMENT_ENV` |
| `region` | `REVENIUM_REGION` | Cloud region identifier (e.g., "us-east-1", "eastus") | Multi-region deployment tracking; auto-detects from `AWS_REGION`, `AZURE_REGION`, `GCP_REGION` |
| `credential_alias` | `REVENIUM_CREDENTIAL_ALIAS` | Human-readable API key name (e.g., "prod-openai-key") | Track which credential was used for credential rotation and security auditing |
| `trace_type` | `REVENIUM_TRACE_TYPE` | Workflow category identifier (max 128 chars) | Group similar workflows (e.g., "customer-support", "data-analysis") for analytics |
| `trace_name` | `REVENIUM_TRACE_NAME` | Human-readable trace label (max 256 chars) | Label trace instances (e.g., "Customer Support Chat", "Document Analysis") |
| `parent_transaction_id` | `REVENIUM_PARENT_TRANSACTION_ID` | Parent transaction ID for distributed tracing | Link child operations to parent transactions across services |
| `transaction_name` | `REVENIUM_TRANSACTION_NAME` | Human-friendly operation name | Label individual operations (e.g., "Generate Response", "Analyze Sentiment") |

**Note:** `operation_type` and `operation_subtype` are automatically detected by the middleware based on the API endpoint and request parameters.

**Resources:**
- [API Reference](https://revenium.readme.io/reference/meter_ai_completion) - Complete metadata field documentation
- [`.env.example`](.env.example) - Environment variable configuration examples

## Configuration Options

### Environment Variables

For a complete list of all available environment variables with examples, see [`.env.example`](.env.example).

**Key variables:**
- `REVENIUM_METERING_API_KEY` - Your Revenium API key (required)
- `REVENIUM_METERING_BASE_URL` - Revenium API endpoint (default: https://api.revenium.ai)
- `OPENAI_API_KEY` - Your OpenAI API key
- `AZURE_OPENAI_ENDPOINT` - Azure OpenAI endpoint (for Azure)
- `REVENIUM_LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)

## Examples

The package includes comprehensive examples in the [`examples/`](examples/) directory.

### Getting Started

```bash
python examples/getting_started.py
```

### OpenAI Examples

| Example                  | File                        | Description                      |
| ------------------------ | --------------------------- | -------------------------------- |
| Basic Chat               | `openai_basic.py`           | Simple chat with metadata        |
| Streaming Chat           | `openai_streaming.py`       | Streaming responses              |
| Azure Basic              | `azure_basic.py`            | Azure OpenAI integration         |
| Azure Streaming          | `azure_streaming.py`        | Azure streaming                  |
| LangChain Async          | `langchain_async_examples.py` | LangChain with async support   |

**See [`examples/README.md`](examples/README.md) for detailed documentation of all examples.**

---

## LangChain Integration

### Installation

```bash
pip install revenium-middleware-openai[langchain]
```

This installs both `langchain` and `langchain-openai` packages required for LangChain integration.

For LangChain integration examples and documentation, see [`examples/README.md`](examples/README.md#langchain-integration).

Quick example:

```python
from langchain_openai import ChatOpenAI
from revenium_middleware_openai.langchain import wrap

# Wrap your LLM with Revenium tracking
llm = wrap(ChatOpenAI(model="gpt-4o-mini"))

# Use normally - usage is automatically tracked
response = llm.invoke("What is the meaning of life?")
print(response.content)
```

Features:
- ✅ Zero-Touch Integration
- ✅ Automatic Async Detection
- ✅ Streaming Support
- ✅ Embeddings Support
- ✅ Thread Safe
- ✅ Error Resilient

---

## Provider Detection & Features

### Automatic Provider Detection
The middleware automatically detects whether you're using standard OpenAI or Azure OpenAI:

- **OpenAI**: Detected via `OpenAI()` client
- **Azure OpenAI**: Detected via `AzureOpenAI()` client

### Model Name Resolution (Azure)
For Azure OpenAI, the middleware automatically resolves Azure deployment names to standard OpenAI model names for accurate pricing and tracking.

### Supported Operations
Both providers support:
- Chat completions (streaming and non-streaming)
- Embeddings
- All metadata fields
- Token counting and cost calculation
- Error handling and logging

**Note:** Azure OpenAI examples (`examples/azure_*.py`) require valid Azure OpenAI credentials. Set `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, and `AZURE_OPENAI_DEPLOYMENT` environment variables to test Azure functionality.

---

## Logging

The middleware logs errors and warnings automatically. Logging is controlled by the upstream `revenium_middleware` package.

---

## Documentation

For detailed documentation, visit [docs.revenium.io](https://docs.revenium.io)

## Contributing

See [CONTRIBUTING.md](https://github.com/revenium/revenium-middleware-openai-python/blob/main/CONTRIBUTING.md)

## Code of Conduct

See [CODE_OF_CONDUCT.md](https://github.com/revenium/revenium-middleware-openai-python/blob/main/CODE_OF_CONDUCT.md)

## Security

See [SECURITY.md](https://github.com/revenium/revenium-middleware-openai-python/blob/main/SECURITY.md)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/revenium/revenium-middleware-openai-python/blob/main/LICENSE) file for details.

## Support

For issues, feature requests, or contributions:

- **Website**: [www.revenium.ai](https://www.revenium.ai)
- **GitHub Repository**: [revenium/revenium-middleware-openai-python](https://github.com/revenium/revenium-middleware-openai-python)
- **Issues**: [Report bugs or request features](https://github.com/revenium/revenium-middleware-openai-python/issues)
- **Documentation**: [docs.revenium.io](https://docs.revenium.io)
- **Email**: support@revenium.io

---

**Built by Revenium**
