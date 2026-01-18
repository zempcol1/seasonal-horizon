"""Gunicorn configuration for production deployment."""
import multiprocessing
import os

# Bind to PORT environment variable (common for cloud hosts) or default 8080
bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"

# Workers: 2-4 x CPU cores is recommended
workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))

# Worker class
worker_class = "sync"

# Timeout for requests (seconds)
timeout = 30

# Keep-alive connections
keepalive = 5

# Logging
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = os.environ.get('LOG_LEVEL', 'info')

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Graceful restart
graceful_timeout = 30

# Preload app for memory efficiency
preload_app = True
