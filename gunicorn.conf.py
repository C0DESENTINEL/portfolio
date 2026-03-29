import multiprocessing

bind = "127.0.0.1:8080"
workers = 2  # 4GB RAM = 2 workers is voldoende voor portfolio
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

# =============================================================================
# CRUCIALE TOEVOEGING: Forwarded Headers Vertrouwen
# =============================================================================
# Dit vertelt Gunicorn om de X-Forwarded-For header van Caddy te gebruiken
# in plaats van het TCP connection IP (127.0.0.1)
forwarded_allow_ips = "127.0.0.1"  # Alleen van Caddy (localhost) - veilig
