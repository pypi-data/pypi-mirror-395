# small helpers (kept minimal for v0.1)
from typing import Any

def pretty_print_config(cfg: dict, mask: bool = True) -> None:
    try:
        safe = cfg.safe_repr() if mask else {k: v for k, v in cfg.items()}
    except Exception:
        safe = {k: v for k, v in cfg.items()}
    for k, v in safe.items():
        print(f"{k} = {v}")

