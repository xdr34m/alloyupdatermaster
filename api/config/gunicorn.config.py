import multiprocessing

# Anzahl der Worker-Prozesse
workers = 10

# Worker-Klasse
worker_class = "uvicorn.workers.UvicornWorker"

# Binden an alle Schnittstellen auf Port 8000
bind = "0.0.0.0:8000"

# Protokollierung
loglevel = "info"
accesslog = "-"  # "-" bedeutet stdout
errorlog = "-"   # "-" bedeutet stderr