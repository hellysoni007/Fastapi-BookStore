import time

import uvicorn
from fastapi import FastAPI

from database import engine, Base
from orders.views import cart_router
from users.views import router as user_router, roles_router
from products.views import router as books_router

app = FastAPI()


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response


Base.metadata.create_all(bind=engine)
app.include_router(router=user_router)
app.include_router(router=books_router)
app.include_router(router=roles_router)
app.include_router(router=cart_router)

if __name__ == "__main__":
    uvicorn.run("main:app",
                host="0.0.0.0",
                port=5000,
                log_level="info",
                reload=True)
