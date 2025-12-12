"""
SDI Python SDK - Language-agnostic client for Synthetic Digital Immunity

Install: pip install sdi-python-sdk

Usage:
    from sdi import SDIClient
    
    sdi = SDIClient("http://localhost:8080")
    result = sdi.analyze_request(
        service_id="my-service",
        path="/api/endpoint",
        method="POST",
        body=request_data
    )
    
    if result.anomaly_detected:
        print(f"Anomaly detected! Score: {result.anomaly_score}")
"""

import requests
from typing import Optional, Dict, Any
from dataclasses import dataclass
import os


@dataclass
class AnalysisResult:
    """Result of SDI analysis"""
    anomaly_detected: bool
    anomaly_score: float = 0.0
    severity: str = "none"
    service_id: Optional[str] = None
    timestamp: Optional[int] = None
    pipeline_triggered: bool = False


class SDIClient:
    """
    SDI Client for Python applications
    
    Examples:
        # Basic usage
        sdi = SDIClient("http://localhost:8080")
        result = sdi.analyze_request(
            service_id="my-service",
            path="/api/users",
            method="POST",
            body='{"user": "data"}'
        )
        
        # With Flask
        @app.before_request
        def check_sdi():
            result = sdi.analyze_request(
                service_id="flask-app",
                path=request.path,
                method=request.method,
                body=request.get_data()
            )
            if result.anomaly_detected and result.severity == "critical":
                abort(403)
        
        # With Django
        class SDIMiddleware:
            def __call__(self, request):
                result = sdi.analyze_request(
                    service_id="django-app",
                    path=request.path,
                    method=request.method,
                    body=request.body
                )
                if result.anomaly_detected:
                    # Log or handle
                    pass
                return self.get_response(request)
    """
    
    def __init__(self, base_url: str = None, timeout: int = 5):
        """
        Initialize SDI client
        
        Args:
            base_url: SDI service URL (default: from SDI_URL env var or localhost:8080)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url or os.environ.get('SDI_URL', 'http://localhost:8080')
        self.timeout = timeout
        self.api_version = 'v1'
    
    def analyze_request(
        self,
        service_id: str,
        path: str,
        method: str,
        headers: Optional[Dict[str, str]] = None,
        body: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AnalysisResult:
        """
        Analyze a request for anomalies
        
        Args:
            service_id: Your service identifier
            path: Request path
            method: HTTP method
            headers: Request headers (optional)
            body: Request body (optional)
            metadata: Additional metadata (optional)
        
        Returns:
            AnalysisResult with detection results
        """
        url = f"{self.base_url}/api/{self.api_version}/analyze"
        
        payload = {
            'serviceId': service_id,
            'path': path,
            'method': method,
            'headers': headers or {},
            'body': body or '',
            'metadata': metadata or {}
        }
        
        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            return AnalysisResult(
                anomaly_detected=data.get('anomalyDetected', False),
                anomaly_score=data.get('anomalyScore', 0.0),
                severity=data.get('severity', 'none'),
                service_id=data.get('serviceId'),
                timestamp=data.get('timestamp'),
                pipeline_triggered=data.get('pipelineTriggered', False)
            )
        
        except requests.exceptions.RequestException as e:
            # Fail open - don't block requests if SDI is down
            print(f"SDI analysis failed: {e}")
            return AnalysisResult(anomaly_detected=False)
    
    def detect_anomaly(
        self,
        service_id: str,
        path: str,
        method: str,
        body: Optional[str] = None
    ) -> bool:
        """
        Quick anomaly detection (lightweight)
        
        Returns:
            True if anomaly detected, False otherwise
        """
        url = f"{self.base_url}/api/{self.api_version}/detect"
        
        payload = {
            'serviceId': service_id,
            'path': path,
            'method': method,
            'body': body or ''
        }
        
        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data.get('anomalyDetected', False)
        
        except requests.exceptions.RequestException as e:
            print(f"SDI detection failed: {e}")
            return False
    
    def health_check(self) -> bool:
        """
        Check if SDI service is healthy
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/{self.api_version}/health",
                timeout=self.timeout
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False


# Flask integration
class SDIFlaskMiddleware:
    """
    Flask middleware for SDI
    
    Usage:
        from flask import Flask
        from sdi import SDIFlaskMiddleware
        
        app = Flask(__name__)
        SDIFlaskMiddleware(app, service_id="my-flask-app")
    """
    
    def __init__(self, app, service_id: str, sdi_url: str = None):
        self.client = SDIClient(sdi_url)
        self.service_id = service_id
        app.before_request(self.before_request)
    
    def before_request(self):
        from flask import request
        result = self.client.analyze_request(
            service_id=self.service_id,
            path=request.path,
            method=request.method,
            headers=dict(request.headers),
            body=request.get_data(as_text=True)
        )
        # Store result for logging/monitoring
        request.sdi_result = result


# Django integration
class SDIDjangoMiddleware:
    """
    Django middleware for SDI
    
    Usage:
        # settings.py
        MIDDLEWARE = [
            'sdi.SDIDjangoMiddleware',
            ...
        ]
        
        SDI_SERVICE_ID = 'my-django-app'
        SDI_URL = 'http://localhost:8080'
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        from django.conf import settings
        self.client = SDIClient(getattr(settings, 'SDI_URL', None))
        self.service_id = getattr(settings, 'SDI_SERVICE_ID', 'django-app')
    
    def __call__(self, request):
        result = self.client.analyze_request(
            service_id=self.service_id,
            path=request.path,
            method=request.method,
            headers=dict(request.headers),
            body=request.body.decode('utf-8') if request.body else ''
        )
        
        # Attach result to request for logging
        request.sdi_result = result
        
        response = self.get_response(request)
        return response

