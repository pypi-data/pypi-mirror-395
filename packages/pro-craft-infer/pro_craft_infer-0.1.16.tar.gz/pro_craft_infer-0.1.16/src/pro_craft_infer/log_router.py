from fastapi import APIRouter, HTTPException, status, Header, Depends
from pro_craft_infer.core import AsyncIntel
from contextlib import asynccontextmanager, AsyncExitStack
import os
import logging

def create_router(database_url_no_protocol: str,
                  model_name: str,
                  log_path: str):


    intels = AsyncIntel(
        database_url=database_url_no_protocol,
        model_name=model_name
        )

    @asynccontextmanager
    async def lifespan(router: APIRouter):
        """_summary_

        Args:
            app (FastAPI): _description_
        """
        # mcp 服务
        logging.info("Log Router lifespan: up , create_database")
        await intels.create_database()
        yield
        logging.info("Log Router lifespan: down")
        

    router = APIRouter(
        tags=["log"], # 这里使用 Depends 确保每次请求都验证
        lifespan=lifespan
    )
    @router.get("/sync_log")
    async def update_log():
        try:
            result = await intels.sync_log(os.path.join(log_path,"app.log"),
                                           database_url="mysql+aiomysql://"+ database_url_no_protocol)

            return {'msg':"success","content":result}
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"{e}"
            )
    
    return router