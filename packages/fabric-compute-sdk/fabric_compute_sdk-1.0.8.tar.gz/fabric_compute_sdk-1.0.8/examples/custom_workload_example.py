"""
Example: Uploading and running custom workload packages

This example demonstrates how to:
1. Upload a custom Python package (zip file with your code + dependencies)
2. Submit multiple jobs with different parameters
3. Monitor job execution
"""

from fabric_sdk import FabricClient

# Initialize client
client = FabricClient(
    api_url="https://api.fabric.carmel.so",
    email="your-enterprise@email.com",
    password="your-password"
)

# ============================================================================
# STEP 1: Upload your custom workload package
# ============================================================================

print("📦 Uploading custom workload...")

workload = client.upload_custom_workload(
    zip_path="path/to/your_code.zip",  # Your zip file with Python code
    name="My Analysis Pipeline",
    main_file="main.py",  # Entry point script
    description="Custom data analysis pipeline with NMF",
    requirements=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "matplotlib>=3.7.0"
    ],
    python_version="3.11"
)

print(f"\n✅ Workload uploaded!")
print(f"   ID: {workload['id']}")
print(f"   Name: {workload['name']}")
print(f"   Version: {workload['version']}")

# Save workload ID for future use
workload_id = workload['id']

# ============================================================================
# STEP 2: List available nodes (optional - for targeted execution)
# ============================================================================

print("\n🖥️  Available nodes:")
nodes = client.list_nodes(status="active")
for node in nodes[:3]:  # Show first 3
    print(f"   - {node['id']}: {node.get('cpu_info', 'Unknown CPU')}")

# Optional: Target a specific node
target_node = nodes[0]['id'] if nodes else None

# ============================================================================
# STEP 3: Submit jobs with different parameters
# ============================================================================

print("\n🚀 Submitting jobs...")

# Example: Submit multiple jobs with parameter sweep
jobs = []

for rank in [5, 10, 15, 20]:
    job = client.submit_job(
        workload_type="custom_python",
        params={
            "rank": rank,
            "init": "nndsvd",
            "normalize_X": "minmax"
        },
        custom_workload_id=workload_id,
        target_node_id=target_node,  # Optional: run on specific node
        job_name=f"NMF Rank {rank}",
        max_runtime_minutes=60,
        budget_cap_usd=5.0
    )
    
    jobs.append(job)
    print(f"   ✅ Job submitted: {job['id']} (Rank {rank})")

# ============================================================================
# STEP 4: Wait for jobs to complete
# ============================================================================

print("\n⏳ Waiting for jobs to complete...")

results = []
for job in jobs:
    try:
        result = client.wait_for_job(job['id'], timeout=600)
        
        if result.status == 'completed':
            print(f"   ✅ Job {job['id']}: SUCCESS (Cost: ${result.actual_cost:.4f})")
            results.append(result)
        else:
            print(f"   ❌ Job {job['id']}: FAILED - {result.error_message}")
    
    except Exception as e:
        print(f"   ❌ Job {job['id']}: ERROR - {e}")

# ============================================================================
# STEP 5: Process results
# ============================================================================

print("\n📊 Results Summary:")
print(f"   Completed: {len(results)}/{len(jobs)}")
print(f"   Total cost: ${sum(r.actual_cost for r in results):.4f}")

for result in results:
    print(f"\n   Job {result.job_id}:")
    print(f"      Result: {result.result}")
    print(f"      Duration: {result.duration_seconds}s")
    print(f"      Cost: ${result.actual_cost:.4f}")

# ============================================================================
# BONUS: List all your custom workloads
# ============================================================================

print("\n📦 Your custom workloads:")
workloads = client.list_custom_workloads()
for w in workloads:
    print(f"   - {w['name']} (v{w['version']}) - ID: {w['id']}")


