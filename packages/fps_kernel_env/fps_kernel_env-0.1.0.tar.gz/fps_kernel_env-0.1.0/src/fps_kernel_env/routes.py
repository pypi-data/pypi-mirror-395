from fastapi import APIRouter
from jupyverse_api.app import App
from jupyverse_api.auth import Auth
from jupyverse_api import Router


class _KernelEnvRoutes(Router):
    def __init__(
        self,
        app: App,
        auth: Auth,
    ) -> None:
        super().__init__(app)

        router = APIRouter()

        @router.get("/api/kernel-env")
        async def get_kernel_env_info():
            return {"status": "creating"}

        @router.post("/api/kernel-env")
        async def create_kernel_env():
            return {"status": "creating"}

        self.include_router(router)
