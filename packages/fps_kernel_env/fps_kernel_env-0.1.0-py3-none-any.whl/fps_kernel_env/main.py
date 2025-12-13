from fps import Module
from jupyverse_api.app import App
from jupyverse_api.auth import Auth

from .routes import _KernelEnvRoutes


class KernelEnvModule(Module):
    async def prepare(self) -> None:
        app = await self.get(App)
        auth = await self.get(Auth)  # type: ignore[type-abstract]
        kernel_env = _KernelEnvRoutes(app, auth)
        self.put(kernel_env)
