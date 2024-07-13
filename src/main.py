from fastapi import FastAPI
from api.routers import routers
import uvicorn

app = FastAPI()

for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
