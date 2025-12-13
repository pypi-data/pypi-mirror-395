"""
Vizu automatic instrumentation via sitecustomize.

This file is automatically loaded by Python if it's in the site-packages directory.
It enables zero-code instrumentation - just set env vars and run!

Usage:
    export VIZU_ENABLED=true
    export VIZU_URL=http://localhost:9600
    python my_app.py  # Automatically instrumented!

Environment Variables:
    VIZU_ENABLED: Set to 'true' to enable auto-instrumentation
    VIZU_URL: Vizu server URL (default: http://localhost:9600)
    VIZU_TENANT_ID: Tenant ID (default: 1)
    VIZU_PROJECT_ID: Project ID (default: 0)
    VIZU_DEBUG: Set to 'true' for verbose logging
    OTEL_SERVICE_NAME: Service name for traces
    OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT: Capture message content

Note:
    This module is loaded very early in the Python startup process.
    It must handle all errors gracefully to avoid breaking user applications.
"""

import os
import sys

# Only auto-instrument if explicitly enabled
if os.getenv('VIZU_ENABLED', '').lower() == 'true':
    try:
        # Import and initialize BEFORE any user code runs
        from vizu.otel_bridge import init_otel_instrumentation
        
        init_otel_instrumentation(
            service_name=os.getenv('OTEL_SERVICE_NAME', os.path.basename(sys.argv[0])),
            vizu_url=os.getenv('VIZU_URL', 'http://localhost:9600'),
            tenant_id=int(os.getenv('VIZU_TENANT_ID', '1')),
            project_id=int(os.getenv('VIZU_PROJECT_ID', '0')),
            capture_content=os.getenv('OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT', 'false').lower() == 'true'
        )
        
        # Silent by default, verbose if DEBUG enabled
        if os.getenv('VIZU_DEBUG', '').lower() == 'true':
            print("[Vizu] ✓ Auto-instrumentation enabled", file=sys.stderr)
            print(f"[Vizu]   Service: {os.getenv('OTEL_SERVICE_NAME', os.path.basename(sys.argv[0]))}", file=sys.stderr)
            print(f"[Vizu]   URL: {os.getenv('VIZU_URL', 'http://localhost:9600')}", file=sys.stderr)
            print(f"[Vizu]   Project: {os.getenv('VIZU_PROJECT_ID', '0')}", file=sys.stderr)
        
    except ImportError as e:
        if os.getenv('VIZU_DEBUG', '').lower() == 'true':
            print(f"[Vizu] ✗ Failed to auto-instrument: {e}", file=sys.stderr)
            print("[Vizu]   Install: pip install opentelemetry-api opentelemetry-sdk", file=sys.stderr)
    
    except Exception as e:
        if os.getenv('VIZU_DEBUG', '').lower() == 'true':
            print(f"[Vizu] ✗ Auto-instrumentation error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
