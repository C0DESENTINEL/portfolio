import multiprocessing
import os

os.environ.setdefault('TMPDIR', '/var/tmp')

bind = "unix:/run/gunicorn/gunicorn.sock"
workers = 2
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
forwarded_allow_ips = "127.0.0.1"

umask = 0o007
