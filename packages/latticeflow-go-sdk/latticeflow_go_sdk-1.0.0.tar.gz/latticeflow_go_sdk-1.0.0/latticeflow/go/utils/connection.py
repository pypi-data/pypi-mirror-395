from __future__ import annotations

import requests


def check_connection(
    host: str,
    default_connect_timeout_sec: float = 3.5,
    default_read_timeout_sec: float = 60.0,
) -> bool:
    try:
        response = requests.get(
            host, timeout=(default_connect_timeout_sec, default_read_timeout_sec)
        )
        return response.status_code == 200
    except:  # noqa: E722
        return False
