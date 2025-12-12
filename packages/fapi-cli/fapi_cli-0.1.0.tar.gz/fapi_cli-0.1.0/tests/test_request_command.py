from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent
from typing import List

import pytest
from typer.testing import CliRunner, Result

from fapi_cli.cli import app


runner = CliRunner()


def _write_app(tmp_path: Path, content: str, filename: str = "main.py") -> Path:
    app_path = tmp_path / filename
    app_path.write_text(dedent(content), encoding="utf-8")
    return app_path


def _invoke(args: List[str]) -> Result:
    return runner.invoke(app, args)


def _basic_app() -> str:
    return """
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"message": "hello"}

    @app.post("/items")
    def create_item(payload: dict):
        return {"received": payload}

    @app.get("/headers")
    def read_headers():
        return {"ok": True}
    """


def test_basic_get_request(tmp_path: Path) -> None:
    app_path = _write_app(tmp_path, _basic_app())
    result = _invoke(["request", str(app_path)])

    assert result.exit_code == 0, result.output
    payload = json.loads(result.stdout)
    assert payload["status_code"] == 200
    assert payload["body"] == {"message": "hello"}


def test_get_with_custom_path_and_query(tmp_path: Path) -> None:
    app_path = _write_app(
        tmp_path,
        """
        from fastapi import FastAPI

        app = FastAPI()

        @app.get("/search")
        def search(q: str, limit: int = 10):
            return {"q": q, "limit": limit}
        """,
    )

    result = _invoke(
        [
            "request",
            str(app_path),
            "-P",
            "/search",
            "-q",
            "q=test",
            "-q",
            "limit=5",
        ]
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.stdout)
    assert payload["status_code"] == 200
    assert payload["body"] == {"q": "test", "limit": 5}


def test_post_with_json_body(tmp_path: Path) -> None:
    app_path = _write_app(tmp_path, _basic_app())
    result = _invoke(
        [
            "request",
            str(app_path),
            "-X",
            "POST",
            "-P",
            "/items",
            "-d",
            '{"name": "Alice"}',
        ]
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.stdout)
    assert payload["status_code"] == 200
    assert payload["body"] == {"received": {"name": "Alice"}}


def test_include_headers(tmp_path: Path) -> None:
    app_path = _write_app(tmp_path, _basic_app())
    result = _invoke(
        [
            "request",
            str(app_path),
            "-P",
            "/headers",
            "--include-headers",
        ]
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.stdout)
    assert payload["status_code"] == 200
    assert "headers" in payload
    assert isinstance(payload["headers"], dict)


def test_custom_app_name(tmp_path: Path) -> None:
    app_path = _write_app(
        tmp_path,
        """
        from fastapi import FastAPI

        fastapi_app = FastAPI()

        @fastapi_app.get("/")
        def read_root():
            return {"custom": True}
        """,
    )

    result = _invoke(["request", str(app_path), "--app-name", "fastapi_app"])

    assert result.exit_code == 0, result.output
    payload = json.loads(result.stdout)
    assert payload["status_code"] == 200
    assert payload["body"] == {"custom": True}


def test_invalid_json_body(tmp_path: Path) -> None:
    app_path = _write_app(tmp_path, _basic_app())
    result = _invoke(["request", str(app_path), "-d", "{invalid"])

    assert result.exit_code == 1
    assert "JSON" in result.output


def test_invalid_method(tmp_path: Path) -> None:
    app_path = _write_app(tmp_path, _basic_app())
    result = _invoke(["request", str(app_path), "-X", "INVALID"])

    assert result.exit_code == 1
    assert "HTTPメソッド" in result.output


def test_missing_file(tmp_path: Path) -> None:
    missing = tmp_path / "missing.py"
    result = _invoke(["request", str(missing)])

    assert result.exit_code == 1
    assert "見つかりません" in result.output


def test_invalid_app(tmp_path: Path) -> None:
    app_path = _write_app(
        tmp_path,
        """
        from fastapi import FastAPI

        not_app = object()
        """,
    )

    result = _invoke(["request", str(app_path)])

    assert result.exit_code == 1
    assert "アプリケーション" in result.output


@pytest.mark.parametrize("header_option", [["Authorization: Bearer token"]])
def test_headers(tmp_path: Path, header_option: List[str]) -> None:
    app_path = _write_app(
        tmp_path,
        """
        from fastapi import FastAPI
        from fastapi import Header

        app = FastAPI()

        @app.get("/protected")
        def protected(authorization: str = Header(...)):
            return {"authorization": authorization}
        """,
    )

    result = _invoke(
        ["request", str(app_path), "-P", "/protected", "-H", header_option[0]]
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.stdout)
    assert payload["status_code"] == 200
    assert payload["body"] == {"authorization": "Bearer token"}
