from __future__ import annotations
from typing import Mapping, Optional, Any, Tuple

from sqlalchemy import text, bindparam, literal
from sqlalchemy.engine import default
from sqlalchemy.sql import Executable
from sqlalchemy.sql.type_api import TypeEngine

import sqlglot

try:
    # Optional: better identifier quoting if present (pip install sqlalchemy-trino)
    from sqlalchemy_trino.base import TrinoDialect  # type: ignore
    _DIALECT = TrinoDialect()
except Exception:
    _DIALECT = default.DefaultDialect()
    _DIALECT.paramstyle = "named"

# ---- helpers ---------------------------------------------------------------

def _render_literal(value: Any, type_: Optional[TypeEngine] = None) -> str:
    """Render a single Python value as a SQL literal using SQLAlchemy."""
    lit = literal(value, type_=type_) if type_ is not None else literal(value)
    return str(lit.compile(dialect=_DIALECT, compile_kwargs={"literal_binds": True}))


def _render_iterable(values: Any, type_: Optional[TypeEngine] = None) -> str:
    items = list(values)
    if not items:
        # Athena/Presto: IN () is invalid; return (NULL)
        return "(NULL)"
    return "(" + ", ".join(_render_literal(v, type_) for v in items) + ")"


def _split_scalar_and_iterable_params(params: Mapping[str, Any]) -> Tuple[dict[str, Any], dict[str, Any]]:
    scalars: dict[str, Any] = {}
    iters: dict[str, Any] = {}
    for k, v in params.items():
        if isinstance(v, (list, tuple, set, frozenset)):
            iters[k] = v
        else:
            scalars[k] = v
    return scalars, iters

# ---- core API --------------------------------------------------------------

def compile_with_literals(stmt: Executable,
                          params: Optional[Mapping[str, Any]] = None,
                          types: Optional[Mapping[str, TypeEngine]] = None) -> str:
    """
    Render a SQLAlchemy statement to a SQL string with values safely inlined.

    This implementation avoids SQLAlchemy 2.x's requirement for typed bindparams
    when using `literal_binds=True` on `text()` by:
      1) compiling without literal_binds to preserve placeholders, then
      2) substituting each `:name` with a dialect-rendered literal.
    """
    types = types or {}
    params = dict(params or {})

    # Ensure it's a TextClause we can compile; if not, coerce
    if hasattr(stmt, "compile"):
        compiled_sql = str(stmt.compile(dialect=_DIALECT))
    else:
        compiled_sql = str(text(str(stmt)).compile(dialect=_DIALECT))

    # Replace scalar params first
    scalar_params, iter_params = _split_scalar_and_iterable_params(params)
    for name, value in scalar_params.items():
        lit = _render_literal(value, types.get(name)) if name in types else _render_literal(value)
        compiled_sql = compiled_sql.replace(f":{name}", lit)

    # Then expand iterable params (e.g., IN :ids)
    for name, values in iter_params.items():
        lit_list = _render_iterable(values, types.get(name)) if name in types else _render_iterable(values)
        compiled_sql = compiled_sql.replace(f":{name}", lit_list)

    return compiled_sql


def validate_and_format_for_athena(sql: str, *, pretty: bool = True, dialect: str = "athena") -> str:
    """Parse & re-write using Presto/Trino dialect to match Athena. Optionally prettify."""
    transpiled = sqlglot.transpile(
        sql,
        read=dialect,
        write=dialect,
        identify=True,
        pretty=pretty,
    )[0]
    return transpiled



def render_safe_athena_sql(template_sql: str,
                           params: Mapping[str, Any],
                           *,
                           types: Optional[Mapping[str, TypeEngine]] = None,
                           pretty: bool = True,
                           dialect: str = "athena") -> str:
    """
    End-to-end: take a SQLAlchemy text() template with named binds, inline values safely
    (including IN-lists), then normalize/format for Athena via sqlglot.

    Example template usage:
        ... WHERE dt BETWEEN :start_dt AND :end_dt AND user_id IN :uids
    """
    t = text(template_sql)
    # Bind scalar names up-front (iterables are expanded post-compile)
    scalar_params, iter_params = _split_scalar_and_iterable_params(params)
    types = types or {}

    for k in scalar_params.keys():
        bp = bindparam(k, type_=types.get(k)) if k in types else bindparam(k)
        t = t.bindparams(bp)

    sql_with_literals = compile_with_literals(t, scalar_params, types)

    # Now expand any iterable params left in template
    for name, values in iter_params.items():
        lit = _render_iterable(values, types.get(name)) if name in types else _render_iterable(values)
        sql_with_literals = sql_with_literals.replace(f":{name}", lit)

    return validate_and_format_for_athena(sql_with_literals, pretty=pretty, dialect=dialect)