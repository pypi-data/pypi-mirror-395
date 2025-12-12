"""ASGI app factory for the duckalog dashboard."""

from __future__ import annotations


from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from starlette.routing import Route

from .state import DashboardContext
from .views import home_page, query_page, view_detail_page, views_page


async def _home(request: Request) -> Response:
    ctx: DashboardContext = request.app.state.dashboard_ctx  # type: ignore[attr-defined]
    return home_page(ctx)


async def _views(request: Request) -> Response:
    ctx: DashboardContext = request.app.state.dashboard_ctx  # type: ignore[attr-defined]
    q = request.query_params.get("q")
    return views_page(ctx, q)


async def _view_detail(request: Request) -> Response:
    ctx: DashboardContext = request.app.state.dashboard_ctx  # type: ignore[attr-defined]
    name = request.path_params["name"]
    return view_detail_page(ctx, name)


async def _query_get(request: Request) -> Response:
    return query_page()


async def _query_post(request: Request) -> Response:
    ctx: DashboardContext = request.app.state.dashboard_ctx  # type: ignore[attr-defined]
    form = await request.form()
    sql = form.get("sql") or ""
    result = ctx.run_query(str(sql))
    return query_page(result=result, sql_text=str(sql))


async def _build(request: Request) -> Response:
    ctx: DashboardContext = request.app.state.dashboard_ctx  # type: ignore[attr-defined]
    ctx.trigger_build()
    return RedirectResponse(url="/", status_code=303)


def create_app(context: DashboardContext) -> Starlette:
    routes = [
        Route("/", _home, methods=["GET"]),
        Route("/views", _views, methods=["GET"]),
        Route("/views/{name:str}", _view_detail, methods=["GET"]),
        Route("/query", _query_get, methods=["GET"]),
        Route("/query", _query_post, methods=["POST"]),
        Route("/build", _build, methods=["POST"]),
    ]
    app = Starlette(debug=False, routes=routes)
    app.state.dashboard_ctx = context  # type: ignore[attr-defined]
    return app
