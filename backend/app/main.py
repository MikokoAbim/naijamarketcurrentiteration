from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.market_place_api import router as market_place_router
from backend.app.api.agent_api import router as agent_router, initialize_agent, shutdown_agent
from backend.app.api.item_api import router as item_router
from backend.app.api.shop_owner_api import router as shop_owner_router

app_api = FastAPI()

# Open nackend api to frontend
app_api.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app_api.on_event("startup")
async def startup():
    await initialize_agent()

@app_api.on_event("shutdown")
async def shutdown():
    await shutdown_agent()

app_api.include_router(market_place_router, prefix="/marketplace")
app_api.include_router(agent_router, prefix="/agent")
app_api.include_router(item_router, prefix = "/marketplace/item")
app_api.include_router(shop_owner_router, prefix="/naija_market/shop_owner")