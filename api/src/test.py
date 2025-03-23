import aiomysql
import asyncio
from fastapi import FastAPI
from jinja2 import Template
from fastapi.responses import PlainTextResponse
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST, CollectorRegistry
from contextlib import asynccontextmanager

# FastAPI app
app = FastAPI()

# Database configuration
DB_CONFIG = {
    "host": "your-mariadb-host",   # Change this to your DB host
    "user": "your-db-user",        # Your DB username
    "password": "your-db-password",  # Your DB password
    "database": "your-db-name",     # Your DB name
}

# Prometheus Metrics
db_connection_failures_total = Counter(
    "db_connection_failures_total", "Total number of database connection failures"
)
db_connection_status = Gauge(
    "db_connection_status", "Database connection status (1 = Connected, 0 = Down)"
)

# New Gauge to track pool connections
db_pool_connections = Gauge(
    "db_pool_connections", "Number of active connections in the DB connection pool"
)

# Create a connection pool
async def create_pool():
    return await aiomysql.create_pool(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        db=DB_CONFIG["database"],
        minsize=1,
        maxsize=10,
    )

# Global pool variable
pool = None

# Function to get a connection from the pool with retry logic
async def get_connection():
    global pool
    while True:
        try:
            async with pool.acquire() as conn:
                db_connection_status.set(1)  # DB is available
                return conn
        except aiomysql.MySQLError as e:
            db_connection_failures_total.inc()  # Track failures
            db_connection_status.set(0)  # DB is down
            print(f"Database connection failed: {e}, retrying in 2 seconds...")
            await asyncio.sleep(2)  # Retry after a short delay

# Fetch data from DB
async def fetch_config_entries():
    conn = await get_connection()
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT `key`, `value` FROM config_entries")
        return await cursor.fetchall()

# Track pool connections
async def update_pool_connections():
    global pool
    while True:
        # Update the pool connections count
        db_pool_connections.set(len(pool._connections))  # Get the current number of connections
        await asyncio.sleep(1)  # Update every second

# Define lifespan context manager for FastAPI lifecycle events (startup, shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool
    pool = await create_pool()

    # Start the task to monitor and update pool connection count
    asyncio.create_task(update_pool_connections())

    # Yield control back to FastAPI to handle requests
    yield

    # On shutdown, clean up resources
    pool.close()
    await pool.wait_closed()

# Add lifespan to FastAPI app
app = FastAPI(lifespan=lifespan)

@app.get("/config", response_class=PlainTextResponse)
async def get_config():
    entries = await fetch_config_entries()  # This fetches the data asynchronously
    template = Template("[general]\napp_name = 'FastAPI App'\nversion = '1.0'\n\n[database]\n{% for entry in entries %}{{ entry.key }} = '{{ entry.value }}'\n{% endfor %}")
    return template.render(entries=entries)

@app.get("/metrics")
async def metrics():
    registry = CollectorRegistry()
    return PlainTextResponse(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)