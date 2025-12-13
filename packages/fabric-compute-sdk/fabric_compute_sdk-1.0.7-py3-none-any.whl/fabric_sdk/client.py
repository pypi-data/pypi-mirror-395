"""
Fabric SDK Client - Main interface for interacting with Fabric API

Copyright 2025 Carmel Labs, Inc.
Licensed under the Apache License, Version 2.0
"""

import requests
import time
from typing import Dict, Any, Optional, List
from .exceptions import (
    AuthenticationError,
    JobSubmissionError,
    InsufficientCreditsError,
    JobTimeoutError,
    NetworkError
)
from .types import Job, Node, CreditBalance, JobResult


class FabricClient:
    """
    Fabric SDK Client for programmatic job submission
    
    Supports two authentication methods:
    1. Email/Password (requires login)
    2. API Key (no login needed)
    
    Example (email/password):
        >>> client = FabricClient(
        ...     api_url="https://api.fabric.carmel.so",
        ...     email="user@example.com",
        ...     password="password"
        ... )
        >>> job = client.submit_job("pytorch_cnn", params={...})
    
    Example (API key):
        >>> client = FabricClient(
        ...     api_url="https://api.fabric.carmel.so",
        ...     api_key="fb_live_..."
        ... )
        >>> job = client.submit_job("pytorch_cnn", params={...})
    """
    
    def __init__(
        self,
        api_url: str,
        email: Optional[str] = None,
        password: Optional[str] = None,
        api_key: Optional[str] = None,
        auto_login: bool = True,
        timeout: int = 30
    ):
        """
        Initialize Fabric client
        
        Args:
            api_url: Fabric API base URL (e.g., "https://api.fabric.carmel.so")
            email: User email (required if not using api_key)
            password: User password (required if not using api_key)
            api_key: API key for authentication (alternative to email/password)
            auto_login: Automatically login on initialization (only for email/password)
            timeout: Default request timeout in seconds
        
        Raises:
            ValueError: If neither (email+password) nor api_key is provided
        """
        self.api_url = api_url.rstrip('/')
        self.email = email
        self.password = password
        self.api_key = api_key
        self.timeout = timeout
        self.token: Optional[str] = None
        
        # Validate authentication parameters
        if api_key:
            # Using API key authentication
            if not api_key.startswith('fb_live_'):
                raise ValueError("Invalid API key format. Must start with 'fb_live_'")
        elif email and password:
            # Using email/password authentication
            if auto_login:
                self.login()
        else:
            raise ValueError("Must provide either api_key OR (email and password)")
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        auth_required: bool = True
    ) -> Dict[str, Any]:
        """Make HTTP request with error handling and retry logic"""
        url = f"{self.api_url}{endpoint}"
        headers = {}
        
        if auth_required:
            if self.api_key:
                # Use API key authentication
                headers['X-API-Key'] = self.api_key
            elif self.token:
                # Use JWT token authentication
                headers['Authorization'] = f'Bearer {self.token}'
            else:
                raise AuthenticationError("Not authenticated. Call login() first or provide an API key.")
        
        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 401:
                raise AuthenticationError("Authentication failed or token expired")
            elif response.status_code == 403:
                raise AuthenticationError("Access forbidden")
            elif response.status_code == 400:
                error_data = response.json()
                if "insufficient credits" in str(error_data).lower():
                    raise InsufficientCreditsError(f"Insufficient credits: {error_data}")
                raise JobSubmissionError(f"Bad request: {error_data}")
            elif response.status_code >= 400:
                raise NetworkError(f"HTTP {response.status_code}: {response.text}")
            
            return response.json()
        
        except requests.exceptions.Timeout:
            raise NetworkError(f"Request timeout after {self.timeout}s")
        except requests.exceptions.ConnectionError as e:
            raise NetworkError(f"Connection error: {e}")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Request failed: {e}")
    
    def login(self) -> str:
        """
        Authenticate and obtain access token
        
        Returns:
            Access token
            
        Raises:
            AuthenticationError: If login fails
        """
        try:
            response = self._make_request(
                'POST',
                '/api/auth/login',
                data={'email': self.email, 'password': self.password},
                auth_required=False
            )
            self.token = response.get('access_token')
            return self.token
        except Exception as e:
            raise AuthenticationError(f"Login failed: {e}")
    
    def get_credit_balance(self) -> CreditBalance:
        """
        Get current credit balance
        
        Returns:
            Credit balance object
        """
        return self._make_request('GET', '/api/payment/balance')
    
    def list_nodes(self, status: Optional[str] = None) -> List[Node]:
        """
        List available compute nodes
        
        Args:
            status: Filter by node status (active, inactive, busy)
            
        Returns:
            List of nodes
        """
        params = {'status': status} if status else None
        return self._make_request('GET', '/api/nodes', params=params)
    
    def submit_job(
        self,
        workload_type: str,
        params: Dict[str, Any],
        input_file_url: Optional[str] = None,
        requirements: Optional[Dict[str, Any]] = None,
        job_name: Optional[str] = None,
        max_runtime_minutes: Optional[int] = None,
        budget_cap_usd: Optional[float] = None,
        custom_workload_id: Optional[str] = None,
        target_node_id: Optional[str] = None
    ) -> Job:
        """
        Submit a job to the Fabric network
        
        Args:
            workload_type: Type of workload (e.g., "llm_inference", "video_transcode", "custom_python")
            params: Workload-specific parameters
            input_file_url: URL to input file for media processing jobs (optional)
            requirements: Hardware requirements (optional)
                - min_cpu_cores: Minimum CPU cores
                - min_ram_gb: Minimum RAM in GB
                - gpu_required: Whether GPU is required
                - min_gpu_memory_gb: Minimum GPU memory in GB
            job_name: User-friendly identifier for the job (optional)
            max_runtime_minutes: Maximum runtime in minutes (optional, default: 30)
            budget_cap_usd: Maximum budget in USD (optional, job rejected if cost exceeds)
            custom_workload_id: ID of uploaded custom workload (for custom_python jobs)
            target_node_id: Specific node to run job on (optional)
        
        Returns:
            Created job object
            
        Raises:
            JobSubmissionError: If submission fails
            InsufficientCreditsError: If insufficient credits
            
        Example (Custom Workload):
            >>> # First upload your custom workload
            >>> workload = client.upload_custom_workload(
            ...     zip_path="analysis.zip",
            ...     name="My Analysis",
            ...     main_file="run.py",
            ...     requirements=["pandas", "numpy"]
            ... )
            >>> 
            >>> # Then submit jobs with different parameters
            >>> job = client.submit_job(
            ...     workload_type="custom_python",
            ...     params={"dataset": "test_data.csv", "iterations": 100},
            ...     custom_workload_id=workload['id']
            ... )
        """
        # Prepare job parameters
        job_params = params.copy()
        if requirements:
            job_params['requirements'] = requirements
        
        payload = {
            'job_type': workload_type,
            'params': job_params
        }
        
        # Add optional fields if provided
        if input_file_url:
            payload['input_file_url'] = input_file_url
        if job_name:
            payload['job_name'] = job_name
        if max_runtime_minutes:
            payload['max_runtime_minutes'] = max_runtime_minutes
        if budget_cap_usd is not None:
            payload['budget_cap_usd'] = budget_cap_usd
        if custom_workload_id:
            payload['custom_workload_id'] = custom_workload_id
        if target_node_id:
            payload['target_node_id'] = target_node_id
        
        try:
            job_data = self._make_request('POST', '/api/jobs/submit', data=payload)
            
            # Check for capacity warning
            if job_data.get('warning'):
                print(f"⚠️  Warning: {job_data['warning'].get('message')}")
                if job_data['warning'].get('suggestions'):
                    print("Suggestions:")
                    for suggestion in job_data['warning']['suggestions']:
                        print(f"  - {suggestion}")
            
            return job_data
        except Exception as e:
            raise JobSubmissionError(f"Job submission failed: {e}")
    
    def submit_batch(
        self,
        jobs: List[Dict[str, Any]],
        show_progress: bool = True
    ) -> Dict[str, Any]:
        """
        Submit multiple jobs in a single batch request (FAST!)
        
        This is 100x faster than submitting jobs in a loop because:
        - Only 1 network request (vs 1000 requests for 1000 jobs)
        - Single database transaction
        - No connection overhead
        
        Args:
            jobs: List of job specifications, each with:
                - workload_type: str (required)
                - params: dict (required)
                - job_name: str (optional)
                - custom_workload_id: str (optional, for custom_python jobs)
                - max_runtime_minutes: int (optional)
                - budget_cap_usd: float (optional)
                - target_node_id: str (optional)
            show_progress: Whether to print progress (default: True)
        
        Returns:
            {
                'jobs': List[Job],  # All submitted jobs
                'total_submitted': int,
                'total_cost_estimate': float,
                'submitted_at': str
            }
        
        Raises:
            JobSubmissionError: If batch submission fails
            
        Example:
            >>> # Submit 1000 jobs with different parameters
            >>> jobs = [
            ...     {
            ...         'workload_type': 'custom_python',
            ...         'params': {'rank': 5, 'init': 'nndsvd'},
            ...         'custom_workload_id': workload_id,
            ...         'job_name': f'NMF_r5_{i}'
            ...     }
            ...     for i in range(1000)
            ... ]
            >>> 
            >>> result = client.submit_batch(jobs)
            >>> print(f"Submitted {result['total_submitted']} jobs")
            >>> print(f"Total cost: ${result['total_cost_estimate']:.2f}")
        """
        if not jobs:
            raise JobSubmissionError("Batch must contain at least 1 job")
        
        if len(jobs) > 1000:
            raise JobSubmissionError(f"Batch size ({len(jobs)}) exceeds maximum of 1000 jobs. Submit in multiple batches.")
        
        if show_progress:
            print(f"📤 Submitting batch of {len(jobs)} jobs...")
        
        # Convert jobs to API format
        batch_payload = []
        for i, job in enumerate(jobs):
            if 'workload_type' not in job or 'params' not in job:
                raise JobSubmissionError(f"Job {i}: 'workload_type' and 'params' are required")
            
            job_payload = {
                'job_type': job['workload_type'],
                'params': job['params']
            }
            
            # Add optional fields
            for field in ['job_name', 'custom_workload_id', 'max_runtime_minutes', 
                         'budget_cap_usd', 'target_node_id', 'input_file_url']:
                if field in job:
                    job_payload[field] = job[field]
            
            batch_payload.append(job_payload)
        
        try:
            result = self._make_request('POST', '/api/jobs/submit/batch', data=batch_payload)
            
            if show_progress:
                print(f"✅ Submitted {result['total_submitted']} jobs")
                print(f"   Total estimated cost: ${result['total_cost_estimate']:.4f}")
            
            return result
            
        except Exception as e:
            raise JobSubmissionError(f"Batch submission failed: {e}")
    
    def list_workloads(self) -> List[Dict[str, Any]]:
        """
        List all custom workloads for the authenticated user.
        
        Returns:
            List of workload dictionaries with metadata
        """
        try:
            result = self._make_request('GET', '/api/workloads')
            return result.get('workloads', [])
        except Exception as e:
            raise Exception(f"Failed to list workloads: {e}")
    
    def get_job(self, job_id: str) -> Job:
        """
        Get job details
        
        Args:
            job_id: Job ID
            
        Returns:
            Job object
        """
        # Use /optimized endpoint to get all jobs, then filter for the specific job
        jobs = self._make_request('GET', '/api/jobs/optimized', params={'limit': 100})
        
        for job in jobs:
            if job['id'] == job_id:
                return job
        
        # Job not found in user's jobs
        raise JobSubmissionError(f"Job {job_id} not found in your jobs")
    
    def get_job_result(self, job_id: str) -> Dict[str, Any]:
        """
        Get job results after completion
        
        Args:
            job_id: Job ID
            
        Returns:
            Dictionary with:
            - success: Whether job completed successfully
            - result: The actual computation result (if success=True)
            - error_message: Error message (if success=False)
            - execution_time: Job execution time in seconds
            - node_id: ID of node that executed the job
            - cost: Actual cost of the job
            
        Raises:
            JobSubmissionError: If job not found or still running
            
        Example:
            >>> result = client.get_job_result(job['id'])
            >>> if result['success']:
            ...     print("Result:", result['result'])
            ...     print("Cost: $", result['cost'])
        """
        # First check if job exists and is completed
        job = self.get_job(job_id)
        
        if job['status'] in ['queued', 'executing']:
            raise JobSubmissionError(
                f"Job is still {job['status']}. Wait for completion before fetching results."
            )
        
        if job['status'] == 'failed':
            return {
                'success': False,
                'result': None,
                'error_message': job.get('error_message', 'Job failed with unknown error'),
                'execution_time': job.get('duration_seconds', 0),
                'node_id': job.get('assigned_node_id'),
                'cost': job.get('actual_cost', 0)
            }
        
        # Fetch results from results endpoint
        try:
            response = self._make_request('GET', f'/api/jobs/{job_id}/results')
            
            return {
                'success': True,
                'result': response.get('result'),
                'error_message': None,
                'execution_time': response.get('execution_time', job.get('duration_seconds', 0)),
                'node_id': response.get('node_id', job.get('assigned_node_id')),
                'cost': job.get('actual_cost', 0)
            }
        except Exception as e:
            # If results endpoint fails, return job data
            return {
                'success': job['status'] == 'completed',
                'result': None,
                'error_message': str(e),
                'execution_time': job.get('duration_seconds', 0),
                'node_id': job.get('assigned_node_id'),
                'cost': job.get('actual_cost', 0)
            }
    
    def wait_for_job(
        self,
        job_id: str,
        timeout: int = 600,
        poll_interval: int = 5
    ) -> JobResult:
        """
        Wait for job to complete
        
        Args:
            job_id: Job ID
            timeout: Maximum wait time in seconds
            poll_interval: Polling interval in seconds
            
        Returns:
            Job result with metadata
            
        Raises:
            JobTimeoutError: If job doesn't complete within timeout
        """
        start_time = time.time()
        
        while True:
            elapsed = time.time() - start_time
            
            if elapsed > timeout:
                raise JobTimeoutError(
                    f"Job {job_id} did not complete within {timeout}s"
                )
            
            job = self.get_job(job_id)
            status = job['status']
            
            if status == 'completed':
                # Get result from /results endpoint
                try:
                    result_response = self._make_request('GET', f'/api/jobs/{job_id}/results')
                    result_data = result_response.get('result')
                    error_msg = result_response.get('error_message')
                except:
                    result_data = None
                    error_msg = None
                
                return JobResult(
                    job_id=job_id,
                    status='completed',
                    result=result_data,
                    actual_cost=job.get('actual_cost', 0.0),
                    duration_seconds=job.get('duration_seconds'),
                    error_message=error_msg
                )
            
            elif status == 'failed':
                # Get error from /results endpoint
                try:
                    result_response = self._make_request('GET', f'/api/jobs/{job_id}/results')
                    error_msg = result_response.get('error_message', 'Job failed')
                except:
                    error_msg = 'Job failed'
                
                return JobResult(
                    job_id=job_id,
                    status='failed',
                    result=None,
                    actual_cost=job.get('actual_cost', 0.0),
                    duration_seconds=job.get('duration_seconds'),
                    error_message=error_msg
                )
            
            # Job still in progress
            time.sleep(poll_interval)
    
    def cancel_job(self, job_id: str) -> Dict[str, Any]:
        """
        Cancel a running job (if supported by backend)
        
        Args:
            job_id: Job ID
            
        Returns:
            Response from backend
        """
        return self._make_request('POST', f'/api/jobs/{job_id}/cancel')
    
    def list_jobs(
        self,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Job]:
        """
        List user's jobs
        
        Args:
            status: Filter by status (queued, executing, completed, failed)
            limit: Maximum number of jobs to return
            
        Returns:
            List of jobs
        """
        # Use the /optimized endpoint which filters by current user
        params = {'limit': limit}
        if status:
            params['status_filter'] = status
        
        return self._make_request('GET', '/api/jobs/optimized', params=params)
    
    def upload_file(self, file_path: str) -> Dict[str, Any]:
        """
        Upload a file for media processing jobs
        
        Args:
            file_path: Path to local file to upload
            
        Returns:
            Dict containing:
                - file_id: Unique file ID
                - file_url: Public URL to access file
                - storage_path: Storage path in Supabase
                - file_size: Size in bytes
                
        Raises:
            FileNotFoundError: If file doesn't exist
            JobSubmissionError: If upload fails
            
        Example:
            >>> upload = client.upload_file("recording.m4a")
            >>> job = client.submit_job("audio_to_text", params={
            ...     "input_file_url": upload['file_url'],
            ...     "language": "en"
            ... })
        """
        import os
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            # Open file
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f)}
                
                # Upload via direct upload endpoint
                response = requests.post(
                    f"{self.api_url}/api/files/upload-direct",
                    headers={'Authorization': f'Bearer {self.token}'},
                    files=files,
                    timeout=300  # 5 minute timeout for large files
                )
                
                if response.status_code == 401:
                    raise AuthenticationError("Authentication failed - token may be expired")
                
                response.raise_for_status()
                result = response.json()
                
                if not result.get('success'):
                    raise JobSubmissionError(f"File upload failed: {result.get('error', 'Unknown error')}")
                
                return {
                    'file_id': result['file_id'],
                    'file_url': result['download_url'],
                    'storage_path': result['storage_path'],
                    'file_size': result['file_size']
                }
                
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"File upload failed: {str(e)}")
        except Exception as e:
            raise JobSubmissionError(f"File upload error: {str(e)}")
    
    def upload_custom_workload(
        self,
        zip_path: str,
        name: str,
        main_file: str,
        description: Optional[str] = None,
        requirements: Optional[List[str]] = None,
        python_version: str = "3.11"
    ) -> Dict[str, Any]:
        """
        Upload a custom workload package
        
        Args:
            zip_path: Path to zip file containing your code
            name: Name for this workload (e.g., "NMF Sensitivity Analysis")
            main_file: Name of the main Python file to execute (e.g., "evaluations.py")
            description: Optional description of the workload
            requirements: Optional list of pip packages (e.g., ["pandas", "numpy", "scikit-learn"])
            python_version: Python version to use (default: "3.11")
            
        Returns:
            Dict containing:
                - id: Workload ID (use this for job submission)
                - name: Workload name
                - version: Version number
                - storage_path: Storage path in Supabase
                - package_size_bytes: Package size
                - created_at: Creation timestamp
                
        Raises:
            FileNotFoundError: If zip file doesn't exist
            JobSubmissionError: If upload fails
            
        Example:
            >>> workload = client.upload_custom_workload(
            ...     zip_path="my_analysis.zip",
            ...     name="Stock Price Prediction",
            ...     main_file="predict.py",
            ...     requirements=["pandas", "scikit-learn", "matplotlib"]
            ... )
            >>> print(f"Workload uploaded: {workload['id']}")
            >>> 
            >>> # Now submit jobs using this workload
            >>> job = client.submit_job(
            ...     workload_type="custom_python",
            ...     params={"stock_symbol": "AAPL"},
            ...     custom_workload_id=workload['id']
            ... )
        """
        import os
        import json
        
        if not os.path.exists(zip_path):
            raise FileNotFoundError(f"Zip file not found: {zip_path}")
        
        if not zip_path.endswith('.zip'):
            raise ValueError("File must be a .zip archive")
        
        try:
            # Prepare multipart form data
            with open(zip_path, 'rb') as f:
                files = {'file': (os.path.basename(zip_path), f, 'application/zip')}
                
                data = {
                    'name': name,
                    'main_file': main_file,
                    'python_version': python_version
                }
                
                if description:
                    data['description'] = description
                
                if requirements:
                    # Convert list to JSON string for form data
                    data['requirements'] = json.dumps(requirements)
                
                # Prepare auth headers
                headers = {}
                if self.api_key:
                    headers['X-API-Key'] = self.api_key
                elif self.token:
                    headers['Authorization'] = f'Bearer {self.token}'
                else:
                    raise AuthenticationError("Not authenticated")
                
                # Upload via custom workload endpoint
                response = requests.post(
                    f"{self.api_url}/api/workloads/upload",
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=300  # 5 minute timeout for large packages
                )
                
                if response.status_code == 401:
                    raise AuthenticationError("Authentication failed - token may be expired")
                elif response.status_code == 400:
                    error_detail = response.json().get('detail', 'Bad request')
                    raise JobSubmissionError(f"Upload failed: {error_detail}")
                
                response.raise_for_status()
                result = response.json()
                
                print(f"✅ Workload uploaded successfully!")
                print(f"   ID: {result['id']}")
                print(f"   Name: {result['name']}")
                print(f"   Version: {result['version']}")
                print(f"   Size: {result['package_size_bytes'] / 1024 / 1024:.2f} MB")
                
                return result
                
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Workload upload failed: {str(e)}")
        except Exception as e:
            raise JobSubmissionError(f"Workload upload error: {str(e)}")
    
    def list_custom_workloads(self) -> List[Dict[str, Any]]:
        """
        List all custom workloads uploaded by current user
        
        Returns:
            List of workload objects
            
        Example:
            >>> workloads = client.list_custom_workloads()
            >>> for w in workloads:
            ...     print(f"{w['name']} (v{w['version']}) - {w['id']}")
        """
        return self._make_request('GET', '/api/workloads')
    
    def get_custom_workload(self, workload_id: str) -> Dict[str, Any]:
        """
        Get details of a specific custom workload
        
        Args:
            workload_id: Workload ID
            
        Returns:
            Workload object with metadata
        """
        return self._make_request('GET', f'/api/workloads/{workload_id}')
    
    def update_custom_workload(
        self,
        workload_id: str,
        zip_path: str,
        description: Optional[str] = None,
        requirements: Optional[List[str]] = None,
        python_version: Optional[str] = None,
        version_increment: str = "patch"
    ) -> Dict[str, Any]:
        """
        Update an existing custom workload with new code.
        Keeps the same workload ID but increments the version number.
        
        Args:
            workload_id: ID of the workload to update
            zip_path: Path to new zip file containing updated code
            description: Optional new description
            requirements: Optional new list of pip packages
            python_version: Optional new Python version
            version_increment: How to increment version ("major", "minor", "patch")
                - patch: 1.0.0 → 1.0.1 (bug fixes, minor changes)
                - minor: 1.0.0 → 1.1.0 (new features, backwards compatible)
                - major: 1.0.0 → 2.0.0 (breaking changes)
                
        Returns:
            Dict containing updated workload metadata
            
        Raises:
            FileNotFoundError: If zip file doesn't exist
            JobSubmissionError: If update fails
            
        Example:
            >>> # Fix a bug in your code
            >>> updated = client.update_custom_workload(
            ...     workload_id="692d55b0-b413-4ef1-be56-d1417a1c06f7",
            ...     zip_path="fixed_code.zip",
            ...     version_increment="patch"  # 1.0.0 → 1.0.1
            ... )
            >>> print(f"Updated to version {updated['version']}")
            >>> 
            >>> # Jobs submitted with this workload_id will now use the new code
            >>> job = client.submit_job(
            ...     workload_type="custom_python",
            ...     params={"rank": 11},
            ...     custom_workload_id="692d55b0-b413-4ef1-be56-d1417a1c06f7"
            ... )
        """
        import os
        import json
        
        if not os.path.exists(zip_path):
            raise FileNotFoundError(f"Zip file not found: {zip_path}")
        
        if not zip_path.endswith('.zip'):
            raise ValueError("File must be a .zip archive")
        
        try:
            # Prepare multipart form data
            with open(zip_path, 'rb') as f:
                files = {'file': (os.path.basename(zip_path), f, 'application/zip')}
                
                data = {
                    'version_increment': version_increment
                }
                
                if description is not None:
                    data['description'] = description
                
                if python_version is not None:
                    data['python_version'] = python_version
                
                if requirements is not None:
                    data['requirements'] = json.dumps(requirements)
                
                # Prepare auth headers
                headers = {}
                if self.api_key:
                    headers['X-API-Key'] = self.api_key
                elif self.token:
                    headers['Authorization'] = f'Bearer {self.token}'
                else:
                    raise AuthenticationError("Not authenticated")
                
                # Upload via update endpoint
                response = requests.put(
                    f"{self.api_url}/api/workloads/{workload_id}",
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=300  # 5 minute timeout for large packages
                )
                
                if response.status_code == 401:
                    raise AuthenticationError("Authentication failed - token may be expired")
                elif response.status_code == 404:
                    raise JobSubmissionError(f"Workload {workload_id} not found")
                elif response.status_code == 400:
                    error_detail = response.json().get('detail', 'Bad request')
                    raise JobSubmissionError(f"Update failed: {error_detail}")
                
                response.raise_for_status()
                result = response.json()
                
                print(f"✅ Workload updated successfully!")
                print(f"   ID: {result['id']}")
                print(f"   Version: {result['version']}")
                print(f"   Size: {result['package_size_bytes'] / 1024 / 1024:.2f} MB")
                
                return result
                
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Workload update failed: {str(e)}")
        except Exception as e:
            raise JobSubmissionError(f"Workload update error: {str(e)}")
    
    def delete_custom_workload(self, workload_id: str) -> Dict[str, Any]:
        """
        Delete a custom workload
        
        Args:
            workload_id: Workload ID
            
        Returns:
            Confirmation message
        """
        return self._make_request('DELETE', f'/api/workloads/{workload_id}')
    
    # ================================================================================
    # API Key Management
    # ================================================================================
    
    def create_api_key(
        self,
        name: Optional[str] = None,
        expires_in_days: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create a new API key for SDK authentication.
        
        WARNING: The API key is only shown once and cannot be retrieved again!
        Store it securely.
        
        Args:
            name: Optional friendly name for the key (e.g., "My Laptop", "CI/CD")
            expires_in_days: Optional expiration in days (1-365)
        
        Returns:
            dict with:
                - id: Key ID
                - api_key: The actual key (ONLY SHOWN ONCE!)
                - key_prefix: First 16 chars for display
                - name: Key name
                - created_at: Creation timestamp
                - expires_at: Expiration timestamp (if set)
        
        Example:
            >>> result = client.create_api_key(name="My Laptop")
            >>> api_key = result['api_key']
            >>> print(f"Save this key: {api_key}")
            >>> # Now you can use it:
            >>> new_client = FabricClient(
            ...     api_url="https://api.fabric.carmel.so",
            ...     api_key=api_key
            ... )
        """
        data = {}
        if name:
            data['name'] = name
        if expires_in_days:
            data['expires_in_days'] = expires_in_days
        
        return self._make_request('POST', '/api/keys/create', data=data)
    
    def list_api_keys(self) -> List[Dict[str, Any]]:
        """
        List all your API keys.
        
        Returns only metadata, not the actual keys.
        
        Returns:
            List of API key objects with:
                - id: Key ID
                - key_prefix: First 16 chars (e.g., "fb_live_abc123...")
                - name: Key name
                - created_at: Creation timestamp
                - last_used_at: Last usage timestamp
                - expires_at: Expiration timestamp
                - is_revoked: Whether the key is revoked
        
        Example:
            >>> keys = client.list_api_keys()
            >>> for key in keys:
            ...     print(f"{key['name']}: {key['key_prefix']}")
        """
        return self._make_request('GET', '/api/keys/list')
    
    def revoke_api_key(self, key_id: str) -> Dict[str, Any]:
        """
        Revoke an API key.
        
        Revoked keys can no longer be used for authentication.
        
        Args:
            key_id: ID of the key to revoke
        
        Returns:
            Confirmation message
        
        Example:
            >>> keys = client.list_api_keys()
            >>> old_key_id = keys[0]['id']
            >>> client.revoke_api_key(old_key_id)
        """
        return self._make_request('DELETE', f'/api/keys/{key_id}')

