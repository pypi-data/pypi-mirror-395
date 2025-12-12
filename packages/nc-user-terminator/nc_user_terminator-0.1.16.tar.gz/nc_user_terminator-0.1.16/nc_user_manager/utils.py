import json
import urllib.parse
import urllib.request
import urllib.error
from typing import Optional, Dict, Any


def request(
    method: str,
    url: str,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    json_body: Optional[dict] = None,
    form_body: Optional[dict] = None,
) -> dict:
    """
    发送 HTTP 请求并返回统一结果，不抛异常
    返回格式:
    {
        "status": int,           # HTTP 状态码
        "success": bool,         # 是否成功 (2xx)
        "body": dict or str,     # JSON解析后的body, 或原始body
        "error": Optional[str]   # 错误信息
    }
    """
    # 拼接 GET 参数
    if params:
        query = urllib.parse.urlencode(params)
        url = f"{url}?{query}"

    data = None

    # JSON 请求
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        if headers is None:
            headers = {}
        headers["Content-Type"] = "application/json"

    # Form 表单请求
    if form_body is not None:
        data = urllib.parse.urlencode(form_body).encode("utf-8")
        headers = headers or {}
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    req = urllib.request.Request(url, method=method.upper(), data=data)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)

    result = {
        "status": 0,
        "success": False,
        "message": None,
        "error": None
    }

    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode()
            if not body:
                return {}
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                result["status"] = 200
                result["success"] = False
                result["message"] = body
                result["error"] = "Invalid JSON response"
                return result
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else None
        result["status"] = e.code
        try:
            result["message"] = json.loads(body) if body else None
        except json.JSONDecodeError:
            result["message"] = body
        result["error"] = "HTTPError"
        result["success"] = False
    except urllib.error.URLError as e:
        result["status"] = 0
        result["message"] = None
        result["error"] = f"NetworkError: {e.reason}"
        result["success"] = False

    return result
