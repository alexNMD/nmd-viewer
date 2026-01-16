import os

bind = "0.0.0.0:8000"
forwarded_allow_ips = "*"
workers = 4
# int(os.getenv("CONCURRENCY")) if os.getenv("CONCURRENCY") else (multiprocessing.cpu_count() + 1)
# Enable workers count regarding cpu

accesslog = "-"
errorlog = "-"
