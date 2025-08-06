from fastapi import FastAPI
from routes.bulk_query_route import router as bulk_query_route
from routes.bulk_push_route import router as bulk_push_route
from routes.auto_bulk_push_route import router as auto_push


app = FastAPI(
    title="VictoriaMetrics API",
    description="Push and Query Time Series Data from VictoriaMetrics",
    version="1.0.0",
)

app.include_router(bulk_query_route)
app.include_router(bulk_push_route)
app.include_router(auto_push)