"""
Simple example: Submit an LLM inference job
"""

from fabric_sdk import FabricClient

# Initialize client (auto-login)
client = FabricClient(
    api_url="https://api.fabric.carmel.so",
    email="ai@org.com",
    password="Test@1234"
)

# Check credit balance
try:
    balance = client.get_credit_balance()
    print(f"💰 Credit balance: ${balance['credits_balance']:.2f}")
except Exception as e:
    print(f"⚠️  Could not fetch balance: {e}")

# List available nodes
try:
    nodes = client.list_nodes(status='active')
    print(f"🖥️  Available nodes: {len(nodes)}")
except Exception as e:
    print(f"⚠️  Could not fetch nodes: {e}")

# Submit a job
print("\n📤 Submitting LLM Inference job...")
job = client.submit_job(
    workload_type="llm_inference",
    params={
        "prompt": "Explain the concept of distributed computing in simple terms",
        "max_length": 200,
        "temperature": 0.7,
        "use_gpu": True
    },
    job_name="Simple LLM Inference Example"
)

print(f"✅ Job submitted: {job['id']}")
print(f"   Status: {job['status']}")

# Wait for completion
print("\n⏳ Waiting for job to complete...")
result = client.wait_for_job(job['id'], timeout=300, poll_interval=3)

if result['status'] == 'completed':
    print(f"✅ Job completed!")
    if result.get('duration_seconds'):
        print(f"   Duration: {result['duration_seconds']:.1f}s")
    print(f"   Cost: ${result['actual_cost']:.6f}")
    if result.get('result'):
        print(f"\n📝 Generated text:")
        print(f"   {result['result'].get('generated_text', 'No text generated')}")
else:
    print(f"❌ Job failed: {result['error_message']}")

