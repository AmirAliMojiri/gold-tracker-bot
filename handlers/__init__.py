from aiogram import Router
from .start import router as start_router
from .prices import router as prices_router
from .portfolio import router as portfolio_router
from .advisor import router as advisor_router
from .alerts import router as alerts_router

main_router = Router()
main_router.include_router(start_router)
main_router.include_router(prices_router)
main_router.include_router(portfolio_router)
main_router.include_router(advisor_router)
main_router.include_router(alerts_router)
