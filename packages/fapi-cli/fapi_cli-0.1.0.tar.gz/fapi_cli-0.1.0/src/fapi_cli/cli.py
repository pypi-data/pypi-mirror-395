"""FastAPIアプリケーション向けCLIコマンドの実装。"""

from __future__ import annotations

import importlib.util
import json
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import parse_qsl

import typer
from fastapi import FastAPI
from fastapi.testclient import TestClient


app = typer.Typer(
    help="FastAPIアプリケーションに対してローカルでリクエストを送信します。"
)

DEFAULT_APP_NAMES: Tuple[str, ...] = ("app", "application", "fastapi_app")
VALID_METHODS: Tuple[str, ...] = (
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
    "HEAD",
    "TRACE",
)


class CLIError(RuntimeError):
    """CLI実行時の回復可能なエラー。"""


@dataclass
class RequestConfig:
    """リクエスト実行の設定値。"""

    method: str
    path: str
    headers: Dict[str, str]
    query: List[Tuple[str, str]]
    json_body: Optional[Any]
    include_headers: bool


def _normalize_path(path: str) -> str:
    path = path.strip() or "/"
    if not path.startswith("/"):
        path = f"/{path}"
    return path


def _parse_headers(raw_headers: Sequence[str]) -> Dict[str, str]:
    headers: Dict[str, str] = {}
    for header in raw_headers:
        if ":" not in header:
            raise CLIError(
                f"ヘッダーの形式が無効です: '{header}'。'Key: Value' の形式を使用してください。"
            )
        key, value = header.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise CLIError(f"ヘッダー名が空です: '{header}'。")
        headers[key] = value
    return headers


def _parse_query(raw_query: Sequence[str]) -> List[Tuple[str, str]]:
    params: List[Tuple[str, str]] = []
    for query_item in raw_query:
        if not query_item:
            continue
        params.extend(parse_qsl(query_item, keep_blank_values=True))
    return params


def _parse_json(data: Optional[str]) -> Optional[Any]:
    if data is None:
        return None
    try:
        return json.loads(data)
    except json.JSONDecodeError as exc:
        raise CLIError(f"JSONの解析に失敗しました: {exc.msg}") from exc


def _validate_method(method: str) -> str:
    normalized = method.upper()
    if normalized not in VALID_METHODS:
        raise CLIError(
            f"HTTPメソッドが不正です: {method}。対応メソッド: {', '.join(VALID_METHODS)}"
        )
    return normalized


def load_application(file_path: str, app_name: Optional[str] = None) -> FastAPI:
    """指定ファイルからFastAPIアプリケーションを読み込む。"""

    path = Path(file_path)
    if not path.exists():
        raise CLIError(f"アプリケーションファイルが見つかりません: {path}")

    module_name = path.stem.replace("-", "_")
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise CLIError(f"モジュールを読み込めませんでした: {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module

    try:
        parent = str(path.parent.resolve())
        if parent not in sys.path:
            sys.path.insert(0, parent)
        spec.loader.exec_module(module)
    except Exception as exc:  # pragma: no cover - ログ用の詳細メッセージ
        trace = "".join(traceback.format_exception(exc))
        raise CLIError(
            f"FastAPIアプリケーションの読み込みに失敗しました: {exc}\n{trace}"
        ) from exc

    candidate_names: Iterable[str]
    if app_name:
        candidate_names = [app_name]
    else:
        candidate_names = DEFAULT_APP_NAMES

    for candidate in candidate_names:
        candidate = candidate.strip()
        if not candidate:
            continue
        app_obj = getattr(module, candidate, None)
        if isinstance(app_obj, FastAPI):
            return app_obj

    raise CLIError(
        "FastAPIアプリケーションが見つかりませんでした。'app' などの変数名を確認してください。"
    )


def _execute_request(fastapi_app: FastAPI, config: RequestConfig) -> Dict[str, Any]:
    client = TestClient(fastapi_app)
    response = client.request(
        config.method,
        config.path,
        headers=config.headers,
        params=config.query or None,
        json=config.json_body,
    )

    try:
        body: Any = response.json()
    except json.JSONDecodeError:
        body = response.text

    result: Dict[str, Any] = {
        "status_code": response.status_code,
        "body": body,
    }

    if config.include_headers:
        result["headers"] = dict(response.headers)

    return result


def _emit_json(data: Dict[str, Any]) -> None:
    typer.echo(json.dumps(data, ensure_ascii=False, indent=2))


def _handle_cli_error(exc: Exception) -> None:
    typer.secho(str(exc), fg=typer.colors.RED, err=True)


@app.command()
def request(
    app_file: str = typer.Argument(
        ...,
        help="FastAPIアプリケーションが定義されたPythonファイルへのパス",
    ),
    path: str = typer.Option("/", "--path", "-P", help="リクエスト送信先のパス"),
    method: str = typer.Option("GET", "--method", "-X", help="HTTPメソッド"),
    data: Optional[str] = typer.Option(
        None, "--data", "-d", help="JSON形式のリクエストボディ"
    ),
    header: List[str] = typer.Option(
        [],
        "--header",
        "-H",
        help="追加するHTTPヘッダー (Key: Value)",
    ),
    query: List[str] = typer.Option(
        [],
        "--query",
        "-q",
        help="クエリパラメータ (key=value&foo=bar の形式)",
    ),
    include_headers: bool = typer.Option(
        False, "--include-headers", help="レスポンスヘッダーを出力に含める"
    ),
    app_name: Optional[str] = typer.Option(
        None,
        "--app-name",
        help="FastAPIアプリケーションの変数名 (デフォルトは app/application/fastapi_app)",
    ),
) -> None:
    """FastAPIアプリケーションに対してHTTPリクエストを送信する。"""

    try:
        normalized_method = _validate_method(method)
        normalized_path = _normalize_path(path)
        headers = _parse_headers(header)
        query_params = _parse_query(query)
        json_body = _parse_json(data)

        fastapi_app = load_application(app_file, app_name=app_name)
        config = RequestConfig(
            method=normalized_method,
            path=normalized_path,
            headers=headers,
            query=query_params,
            json_body=json_body,
            include_headers=include_headers,
        )

        result = _execute_request(fastapi_app, config)
        _emit_json(result)
    except CLIError as exc:
        _handle_cli_error(exc)
        raise typer.Exit(code=1) from exc


@app.callback()
def main() -> None:
    """fapi-cliのメインコマンド。"""

    # サブコマンドを提供するだけなので実装は不要
    return None
