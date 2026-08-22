def execute(sql: str):
    """Pretend DB driver that runs raw SQL strings."""
    print(f"EXEC: {sql}")
    return [{"ok": True}]


def query(sql: str):
    """Runs caller-provided SQL with no parameterization."""
    return execute(sql)
