# Revenium Middleware for Anthropic - Examples

This directory contains practical examples demonstrating the complete functionality of the Revenium middleware with both direct Anthropic API and AWS Bedrock integration.

## Example Files

### **getting_started.py**
The minimal getting started example with all metadata fields documented.
- Demonstrates basic Anthropic API usage with automatic metering
- Documents all 13 required and optional metadata fields
- Perfect for understanding the middleware basics
- Zero-config setup with auto-initialization

### **anthropic-basic.py**
The simplest way to get started with Revenium middleware.
- Zero-config setup with auto-initialization
- Basic Anthropic API usage with automatic metering
- Demonstrates hybrid initialization approach
- Perfect for quick testing and simple applications

### **anthropic-advanced.py**
Production-ready example with detailed metadata tracking.
- Custom metadata for granular usage tracking
- Perfect for multi-tenant applications
- Enables detailed billing and analytics
- Shows advanced configuration options

### **anthropic-streaming.py**
Complete streaming API example with real-time response display.
- Uses Anthropic's streaming API with full token tracking
- Automatic token counting for streaming responses
- Context-based metadata setting with `usage_context`
- Thread-safe streaming support

### **anthropic-bedrock.py** (AWS Bedrock Only)
Complete AWS Bedrock integration demonstration.
- **All examples route through AWS Bedrock exclusively**
- Basic chat completion via Bedrock
- Metadata tracking via Bedrock
- Streaming support via Bedrock
- Advanced streaming with detailed usage tracking via Bedrock
- Model mapping examples and configuration options

### **trace_visualization_example.py**
Comprehensive trace visualization and distributed tracing demonstration.
- Basic trace visualization with environment variables
- Distributed tracing with parent-child transaction relationships
- Retry tracking for failed operations
- Custom trace categorization and naming
- Region and credential tracking
- Usage metadata override patterns

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/revenium/revenium-middleware-anthropic-python.git
   cd revenium-middleware-anthropic-python
   ```

2. **Create virtual environment:**
   ```bash
   # Create virtual environment
   python -m venv .venv

   # Activate virtual environment
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install the middleware:**
   ```bash
   # Basic installation
   pip install revenium-middleware-anthropic python-dotenv

   # With AWS Bedrock support
   pip install revenium-middleware-anthropic[bedrock] python-dotenv
   ```

4. **Set up your environment variables:**
   Create a `.env` file in the project root:
   ```env
   # Revenium API keys
   REVENIUM_METERING_API_KEY="hak_..."
   REVENIUM_METERING_BASE_URL="https://api.revenium.ai"

   # Vendor API keys
   ANTHROPIC_API_KEY="sk-ant-..."

   # Optional for Bedrock examples
   AWS_ACCESS_KEY_ID="your_aws_key"
   AWS_SECRET_ACCESS_KEY="your_aws_secret"
   AWS_REGION="us-east-1"
   ```

5. **Run any example:**
   ```bash
   # Getting started example
   python examples/getting_started.py

   # Basic usage
   python examples/anthropic-basic.py

   # Advanced with metadata
   python examples/anthropic-advanced.py

   # Streaming example
   python examples/anthropic-streaming.py

   # AWS Bedrock integration
   python examples/anthropic-bedrock.py

   # Trace visualization
   python examples/trace_visualization_example.py
   ```

## Hybrid Initialization

The middleware supports both automatic and explicit initialization for maximum flexibility:

### **Simple (Auto-initialization) - Recommended**
```python
import revenium_middleware_anthropic  # Auto-initializes on import
import anthropic

client = anthropic.Anthropic()
# Middleware is automatically active - zero configuration needed!
```

### **Advanced (Explicit Control)**
```python
import revenium_middleware_anthropic

# Check initialization status
if not revenium_middleware_anthropic.is_initialized():
    # Manual initialization with custom configuration
    success = revenium_middleware_anthropic.initialize()
    if not success:
        print("Configuration needed - check environment variables")
```

### **Production Pattern**
```python
import revenium_middleware_anthropic

# Verify middleware is ready in production
assert revenium_middleware_anthropic.is_initialized(), "Middleware not configured"

import anthropic
client = anthropic.Anthropic()
# Guaranteed to be metered
```

## What Gets Tracked

All examples automatically track:
- **Token Usage**: Input, output, cache creation/read, and total tokens
- **Request Timing**: Duration, timestamps, and time-to-first-token
- **Model Information**: Which model was used and provider routing
- **Provider Detection**: Automatic detection of Anthropic direct vs AWS Bedrock
- **Streaming Support**: Complete token tracking for streaming responses
- **Thread Safety**: Concurrent request handling with zero errors
- **Custom Metadata**: Organization, user, task details (in advanced examples)

## Metadata Examples

The examples use different organization IDs to help you identify them in your Revenium dashboard:

- `anthropic-basic.py` → Default automatic tracking (no custom metadata)
- `anthropic-advanced.py` → `acme-corp` organization with detailed metadata
- `anthropic-streaming.py` → `content-team-emea` organization with streaming context
- `anthropic-bedrock.py` → Multiple organization IDs demonstrating different Bedrock scenarios:
  - `anthropic-python-bedrock-chat` (basic Bedrock chat)
  - `anthropic-python-bedrock` (Bedrock with metadata)
  - `anthropic-python-bedrock-streaming` (Bedrock streaming)
  - `anthropic-python-bedrock-streaming` (advanced Bedrock streaming)

## Configuration

All examples automatically load environment variables from a `.env` file.

### Required Variables
- `ANTHROPIC_API_KEY` - Your Anthropic API key
- `REVENIUM_METERING_API_KEY` - Your Revenium API key
- `REVENIUM_METERING_BASE_URL` - Revenium API endpoint

### Optional for Bedrock Examples
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `AWS_REGION` - AWS region (default: us-east-1)
- `REVENIUM_BEDROCK_DISABLE` - Set to `1` to disable Bedrock detection

### Debug Configuration
- `REVENIUM_LOG_LEVEL` - Set to `DEBUG` for detailed logging

### Trace Visualization (Optional)
- `REVENIUM_ENVIRONMENT` - Deployment environment (e.g., 'production', 'staging')
- `REVENIUM_REGION` - Cloud region (e.g., 'us-east-1', 'eu-west-1')
- `REVENIUM_CREDENTIAL_ALIAS` - Friendly name for API credentials
- `REVENIUM_TRACE_TYPE` - Custom trace type for categorization (alphanumeric, hyphens, underscores, max 128 chars)
- `REVENIUM_TRACE_NAME` - Human-readable trace name (max 256 chars)
- `REVENIUM_PARENT_TRANSACTION_ID` - Parent transaction ID for distributed tracing
- `REVENIUM_TRANSACTION_NAME` - Name of the current transaction
- `REVENIUM_RETRY_NUMBER` - Retry attempt number (default: 0)

## Tips

1. **Start with `anthropic-basic.py`** to verify your setup works
2. **Use `anthropic-advanced.py`** as a template for production applications
3. **Try `anthropic-streaming.py`** to see streaming functionality
4. **Run `anthropic-bedrock.py`** for comprehensive AWS Bedrock integration
5. **Check your Revenium dashboard** to see all tracked usage
6. **Customize metadata** to match your application's tracking needs
7. **Use auto-initialization** for simple projects (just import and use)
8. **Use explicit initialization** for advanced configuration control
9. **Check `is_initialized()`** to verify middleware status in production
10. **Enable debug logging** with `REVENIUM_LOG_LEVEL=DEBUG` for troubleshooting

## Streaming Features

All streaming examples demonstrate:
- **Real-time response display** as tokens are generated
- **Automatic token counting** for streaming responses
- **Provider-agnostic interface** (same code works with Anthropic API and Bedrock)
- **Thread-safe operation** for concurrent streaming
- **Complete usage tracking** including time-to-first-token metrics

## 🆘 Troubleshooting

If examples don't work:
1. **Verify your `.env` file** has the correct API keys
2. **Update to latest version**: `pip install -U revenium-middleware-anthropic[bedrock]`
3. **Check Anthropic API key** has sufficient credits
4. **For Bedrock examples**: Verify AWS credentials with `aws sts get-caller-identity`
5. **Check permissions**: Ensure AWS credentials have `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream`
6. **Enable debug logging**: `REVENIUM_LOG_LEVEL=DEBUG python examples/anthropic-basic.py`
7. **Test initialization**: Check if `revenium_middleware_anthropic.is_initialized()` returns `True`

## Documentation

For more details, see the main [README.md](https://github.com/revenium/revenium-middleware-anthropic-python/blob/HEAD/README.md) in the project root.
