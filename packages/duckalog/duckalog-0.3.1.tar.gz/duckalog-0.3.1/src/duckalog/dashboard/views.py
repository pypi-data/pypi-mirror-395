"""starhtml/starui view helpers for the dashboard."""

from __future__ import annotations

from collections.abc import Iterable

from starlette.responses import HTMLResponse

from .state import DashboardContext, QueryResult, summarize_config


# --- Minimal starhtml/starui compatibility -------------------------------------

try:  # pragma: no cover - import-time fallback
    import starhtml as sh
    import starui as ui
except Exception:  # pragma: no cover - allow running without deps installed
    class _Elt:
        def __init__(self, tag: str, *children, **attrs):
            self.tag = tag
            self.children = children
            self.attrs = attrs

        def __str__(self):
            attr_str = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in self.attrs.items() if v is not None)
            inner = "".join(str(c) for c in self.children)
            if attr_str:
                return f"<{self.tag} {attr_str}>{inner}</{self.tag}>"
            return f"<{self.tag}>{inner}</{self.tag}>"

        def __html__(self):
            return str(self)

    class sh:  # type: ignore
        @staticmethod
        def html(*children, **attrs):
            return _Elt("html", *children, **attrs)

        @staticmethod
        def head(*children, **attrs):
            return _Elt("head", *children, **attrs)

        @staticmethod
        def title(*children, **attrs):
            return _Elt("title", *children, **attrs)

        @staticmethod
        def body(*children, **attrs):
            return _Elt("body", *children, **attrs)

        @staticmethod
        def div(*children, **attrs):
            return _Elt("div", *children, **attrs)

        @staticmethod
        def h1(*children, **attrs):
            return _Elt("h1", *children, **attrs)

        @staticmethod
        def h2(*children, **attrs):
            return _Elt("h2", *children, **attrs)

        @staticmethod
        def h3(*children, **attrs):
            return _Elt("h3", *children, **attrs)

        @staticmethod
        def p(*children, **attrs):
            return _Elt("p", *children, **attrs)

        @staticmethod
        def br(**attrs):
            return _Elt("br", **attrs)

        @staticmethod
        def ul(*children, **attrs):
            return _Elt("ul", *children, **attrs)

        @staticmethod
        def li(*children, **attrs):
            return _Elt("li", *children, **attrs)

        @staticmethod
        def a(*children, **attrs):
            return _Elt("a", *children, **attrs)

        @staticmethod
        def pre(*children, **attrs):
            return _Elt("pre", *children, **attrs)

        @staticmethod
        def table(*children, **attrs):
            return _Elt("table", *children, **attrs)

        @staticmethod
        def thead(*children, **attrs):
            return _Elt("thead", *children, **attrs)

        @staticmethod
        def tbody(*children, **attrs):
            return _Elt("tbody", *children, **attrs)

        @staticmethod
        def tr(*children, **attrs):
            return _Elt("tr", *children, **attrs)

        @staticmethod
        def th(*children, **attrs):
            return _Elt("th", *children, **attrs)

        @staticmethod
        def td(*children, **attrs):
            return _Elt("td", *children, **attrs)

        @staticmethod
        def form(*children, **attrs):
            return _Elt("form", *children, **attrs)

        @staticmethod
        def input(**attrs):
            return _Elt("input", **attrs)

        @staticmethod
        def textarea(*children, **attrs):
            return _Elt("textarea", *children, **attrs)

        @staticmethod
        def button(*children, **attrs):
            return _Elt("button", *children, **attrs)

    class ui:  # type: ignore
        @staticmethod
        def card(*children, **attrs):
            return sh.div(*children, **attrs)

        @staticmethod
        def button(*children, **attrs):
            return sh.button(*children, **attrs)

        @staticmethod
        def table(*children, **attrs):
            return sh.table(*children, **attrs)

        @staticmethod
        def input(**attrs):
            return sh.input(**attrs)

        @staticmethod
        def textarea(*children, **attrs):
            return sh.textarea(*children, **attrs)


# --- Rendering helpers ---------------------------------------------------------

def _page(title: str, body_children: Iterable) -> HTMLResponse:
    doc = sh.html(
        sh.head(sh.title(title)),
        sh.body(*body_children),
    )
    return HTMLResponse(str(doc))


def home_page(ctx: DashboardContext) -> HTMLResponse:
    summary = summarize_config(ctx)
    last = ctx.last_build
    status_text = (
        f"{'✅' if last and last.success else '❌' if last and last.success is False else '—'} "
        f"{last.completed_at.isoformat() if last and last.completed_at else 'Not run yet'}"
    )
    return _page(
        "Duckalog Dashboard",
        [
            sh.h1("Duckalog Dashboard"),
            sh.div(
                sh.p(f"Config: {summary['config_path']}" if summary["config_path"] else "Config: (in-memory)"),
                sh.p(f"DuckDB: {summary['database']}"),
                sh.p(f"Views: {summary['views']}  |  Attachments: {summary['attachments']}  |  Semantic models: {summary['semantic_models']}"),
                sh.p(f"Last build: {status_text}"),
            ),
            sh.ul(
                sh.li(sh.a("Views", href="/views")),
                sh.li(sh.a("Query", href="/query")),
            ),
            sh.form(
                sh.button("Build catalog", type="submit"),
                method="post",
                action="/build",
            ),
        ],
    )


def views_page(ctx: DashboardContext, q: str | None) -> HTMLResponse:
    rows = ctx.view_list()
    if q:
        q_lower = q.lower()
        rows = [r for r in rows if q_lower in r["name"].lower()]

    header = ["name", "source", "uri", "database", "table", "semantic"]
    table_rows = [
        sh.tr(*(sh.td(str(r[h])) for h in header)) for r in rows
    ]
    return _page(
        "Views",
        [
            sh.h1("Views"),
            sh.form(
                ui.input(type="text", name="q", value=q or "", placeholder="Search view name"),
                sh.button("Search", type="submit"),
                method="get",
            ),
            ui.table(
                sh.thead(sh.tr(*(sh.th(h.capitalize()) for h in header))),
                sh.tbody(*table_rows),
            ),
            sh.p(sh.a("Back to home", href="/")),
        ],
    )


def view_detail_page(ctx: DashboardContext, name: str) -> HTMLResponse:
    view = ctx.get_view(name)
    if view is None:
        return HTMLResponse("View not found", status_code=404)

    semantic_models = ctx.semantic_for_view(name)

    definition_parts: list[str] = []
    if view.sql:
        definition_parts.append(view.sql)
    else:
        definition_parts.append(f"source={view.source or 'sql'}")
        if view.uri:
            definition_parts.append(f"uri={view.uri}")
        if view.database:
            definition_parts.append(f"database={view.database}")
        if view.table:
            definition_parts.append(f"table={view.table}")

    semantics_block: list = []
    if semantic_models:
        for sm in semantic_models:
            semantics_block.append(sh.h3(f"Semantic model: {sm.name}"))
            semantics_block.append(sh.p(f"Dimensions: {', '.join(d.name for d in sm.dimensions) or '—'}"))
            semantics_block.append(sh.p(f"Measures: {', '.join(m.name for m in sm.measures) or '—'}"))
    else:
        semantics_block.append(sh.p("No semantic-layer metadata for this view."))

    return _page(
        f"View {name}",
        [
            sh.h1(f"View: {name}"),
            sh.p("Definition:"),
            sh.pre("\n".join(definition_parts)),
            *semantics_block,
            sh.p(sh.a("Back to views", href="/views")),
        ],
    )


def query_page(result: QueryResult | None = None, sql_text: str = "") -> HTMLResponse:
    table_part: list = []
    if result:
        if result.error:
            table_part.append(sh.p(f"Error: {result.error}"))
        else:
            header = [sh.th(col) for col in result.columns]
            body_rows = [
                sh.tr(*(sh.td(str(v)) for v in row)) for row in result.rows
            ]
            table_part.append(
                ui.table(
                    sh.thead(sh.tr(*header)),
                    sh.tbody(*body_rows),
                )
            )
            if result.truncated:
                table_part.append(sh.p("Results truncated."))
    return _page(
        "Query",
        [
            sh.h1("Ad-hoc Query"),
            sh.form(
                ui.textarea(sql_text, name="sql", rows=6, cols=80),
                sh.br(),
                ui.button("Run", type="submit"),
                method="post",
            ),
            *table_part,
            sh.p(sh.a("Back to home", href="/")),
        ],
    )


def build_status_fragment(status) -> str:
    if status is None:
        return "No builds have been run yet."
    if status.success:
        return f"Last build succeeded in {status.duration_seconds or 0:.2f}s"
    return f"Last build failed: {status.message or 'unknown error'}"
