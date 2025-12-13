# Fabric SDK

**Official Python SDK for Fabric - Distributed AI Compute Network**

Submit AI workloads to the Fabric network programmatically.

## Installation

```bash
pip install fabric-compute-sdk
```

## Quick Start

### Option 1: Email/Password Authentication

```python
from fabric_sdk import FabricClient

# Initialize client with email/password
client = FabricClient(
    api_url="https://api.fabric.carmel.so",
    email="your@email.com",
    password="your_password"
)

# Submit a job
job = client.submit_job(
    workload_type="llm_inference",
    params={
        "prompt": "Explain quantum computing in simple terms",
        "max_length": 200,
        "temperature": 0.7,
        "use_gpu": True
    },
    job_name="My LLM Inference Job"
)

print(f"Job submitted: {job['id']}")

# Wait for completion
result = client.wait_for_job(job['id'], timeout=300)
print(f"Job completed in {result['duration_seconds']}s")
print(f"Cost: ${result['actual_cost']}")
```

### Option 2: API Key Authentication (Recommended for Google OAuth users)

```python
from fabric_sdk import FabricClient

# Initialize client with API key
client = FabricClient(
    api_url="https://api.fabric.carmel.so",
    api_key="fb_live_..."  # Get this from dashboard Settings > API Keys
)

# Works exactly the same!
job = client.submit_job(
    workload_type="llm_inference",
    params={"prompt": "Explain quantum computing"},
    job_name="My Job"
)
```

**Why use API keys?**
- No password needed (great for Google/GitHub OAuth users)
- More secure for CI/CD pipelines
- Easy to rotate and revoke
- Each project can have its own key

## Features

- **Dual Authentication** - Email/password OR API keys (NEW!)
- **API Key Management** - Create, list, and revoke keys programmatically
- **Job Submission** - Submit 28 production workload types
- **Batch Submission** - Submit 1000s of jobs in seconds (100x faster!)
- **Custom Workloads** - Upload and run your own Python code
- **Job Monitoring** - Track progress and get results
- **Credit Management** - Check balance and purchase credits
- **Node Discovery** - List available compute nodes
- **Auto-Retry** - Built-in network resilience
- **Type Hints** - Full TypeScript-style typing support

## Supported Workload Types (26 Total)

**Compute & Simulation (5)**
- `cpu_compute_benchmark`, `gpu_compute_benchmark`
- `eigenvalue_decomposition`, `financial_forecast_simulation`, `agent_simulation`

**Data Processing (5)**
- `data_cleaning`, `feature_extraction`, `csv_vectorization`
- `data_augmentation`, `outlier_detection`

**AI Inference (7)**
- `llm_inference`, `llm_inference_batch`, `image_classification`
- `embedding_generation`, `sentiment_analysis`
- `text_summarization`, `question_answering`

**Media Processing (5)**
- `video_transcode`, `audio_to_text`, `video_object_detection`
- `image_resize_batch`, `video_summarization`

**ML Training (4)**
- `random_forest_training`, `svm_training`
- `xgboost_training`, `neural_network_training`

**Custom (1)**
- `custom_python`

## Documentation

Complete documentation, guides, and examples are available in the **[Fabric Dashboard](https://fabric.carmel.so)**.

### Key Features
- **Custom Workloads** - Upload and run your own Python code on Fabric
- **Enterprise Integration** - Complete API reference and best practices
- **Batch Submission** - Large-scale job processing (1M+ jobs/week)
- **API Key Management** - Secure authentication for production systems

## Support

Access the **[Fabric Dashboard](https://fabric.carmel.so)** for documentation, support, and account management.

## License

Apache License 2.0

Copyright 2025 Carmel Labs, Inc.


