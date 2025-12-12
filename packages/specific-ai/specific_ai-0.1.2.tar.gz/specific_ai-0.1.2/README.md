# Specific.ai SDK

## Installation

```bash
pip install specific-ai
```

## Quick Start

```python
from specific_ai import OpenAI

# Initialize the client
client = OpenAI(
    specific_ai_url="<your-specific-ai-service-URL>",
    api_key="<your-openai-api-key>",
    use_specific_ai_inference=False,
)

# Use like regular OpenAI client with the SpecificAI additional field
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Hello!"}
    ],
    specific_ai={
        "task_name": "greeting",
    }
)
```

## Features

- 🎯 Custom-tailored models optimized for your specific use cases
- 🚀 Drop-in replacement for OpenAI's official Python client
- 📊 Automatic request and response logging
- 🎯 Response optimization capabilities
- 📈 Advanced analytics integration

## Core Features Explained

### Model Inference Options

The SDK offers two approaches to model inference, controlled by `use_specific_ai_inference`:

```python
client = OpenAI(
    api_key="your-key",
    use_specific_ai_inference=True  # Enable SpecificAI's optimized models
)
```

- **Standard Inference** (`use_specific_ai_inference=False`):
  - Uses OpenAI's models directly
  - Standard pricing and performance
  - No optimization layer

- **SpecificAI Inference** (`use_specific_ai_inference=True`):
  - Uses task-specific models optimized for your use cases
  - Potential improvements in performance and cost
  - Automatic fallback to standard OpenAI models if needed
  - Requires prior data collection for model training


### Best Practices

1. **Start with Data Collection**: 
   - Keep `use_specific_ai_inference=False` initially
   - This builds up training data for your use cases

2. **Transition to Optimized Models**:
   - Once sufficient data is collected
   - Enable `use_specific_ai_inference=True`
   - Monitor performance improvements

3. **Testing New Features**:
   - Use A/B testing between standard and optimized models
   - Compare performance metrics
   - Gradually roll out optimization to production


## Logging

This SDK uses Python's standard logging module. To capture logs from the SDK, 
configure logging in your application:

```python
import logging

# Basic console logging
logging.basicConfig(level=logging.INFO)

# Or for more detailed logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Support

Need help? Contact our support team at support@specifc.ai
