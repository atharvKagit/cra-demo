def execute(sql: str, params: tuple = ()):
    """Pretend DB driver that runs parameterized SQL."""
    print(f"EXEC: {sql} params={params}")
    return [{"ok": True}]


def query(sql: str):
    """Runs caller-provided SQL with no parameterization."""
    return execute(sql)


def query_params(sql: str, params: tuple):
    """Runs SQL with bound parameters (demo-safe API)."""
    return execute(sql, params)
