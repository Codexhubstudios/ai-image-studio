import json
import urllib.request

WORKER_URL = "https://ai-image-worker.vultra-server.workers.dev/?format=json"


def _json_response(status, body):
    data = json.dumps(body).encode("utf-8")
    headers = [
        ("Content-Type", "application/json"),
        ("Content-Length", str(len(data))),
        ("Access-Control-Allow-Origin", "*"),
        ("Access-Control-Allow-Headers", "Content-Type"),
        ("Access-Control-Allow-Methods", "GET, POST, OPTIONS"),
    ]
    return status, headers, data


def handle_request(method, raw_body):
    try:
        if method == "OPTIONS":
            return _json_response(200, {"status": "ok"})

        if method == "GET":
            return _json_response(200, {
                "service": "ai-image-studio api proxy",
                "usage": 'POST {"prompt": "a cyberpunk cat", "steps": 4}',
            })

        payload = json.loads(raw_body or "{}")
        prompt = payload.get("prompt")
        if not prompt:
            return _json_response(400, {"error": "Missing 'prompt'"})

        out_payload = json.dumps({
            "prompt": str(prompt)[:2000],
            "steps": int(payload.get("steps", 4)),
        }).encode()

        req = urllib.request.Request(
            WORKER_URL, data=out_payload, method="POST",
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req, timeout=90) as resp:
            result = json.loads(resp.read().decode())

        return _json_response(200, {
            "image": result.get("image"),
            "mime": result.get("mime", "image/jpeg"),
        })
    except Exception as e:
        return _json_response(500, {"error": str(e)})


def app(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET")
    try:
        length = int(environ.get("CONTENT_LENGTH") or 0)
    except (TypeError, ValueError):
        length = 0
    raw_body = environ["wsgi.input"].read(length).decode("utf-8", "replace") if length else ""
    status, headers, data = handle_request(method, raw_body)
    start_response(f"{status} OK", headers)
    return [data]
