from fastapi import APIRouter

from .docs.router import router as router_docs
from .gids.router import router as router_gids

router = APIRouter(prefix='/v1')

router.include_router(router_docs)
router.include_router(router_gids)