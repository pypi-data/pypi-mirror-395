from typing import cast, Dict, Iterable
from pathlib import Path
from .build import get_api_config
import os


SUPPORTED_METHODS: Iterable[str] = ("get", "post", "put", "patch", "delete", "head")

def generate_fastapi_routes_from_openapi_path(endpoint_def: Dict) -> str:
    blocks = []

    dir_name = endpoint_def.get("name", "unknown")
    openapi_paths = cast(dict, endpoint_def.get("definition", {}))
    for path, methods in openapi_paths.items():
        if not isinstance(methods, dict):
            continue

        for method, _spec in methods.items():
            m = method.lower()
            if m not in SUPPORTED_METHODS:
                continue  # ignora options u otros no soportados

            handler_name = f"{dir_name}_handler"
            http_method = m.upper()

            block = f'''@router.{m}("{path}")
async def {dir_name}(request: Request, response: Response):
    event = await build_event_from_request(request)
    res = {handler_name}(event, MockContext())
    response.status_code = get_status_code(res)
    return get_body(res)
'''
            blocks.append(block)

    return "\n\n".join(blocks)


def build_local_api(lambdas_path: Path, base_path: Path):
    endpoints_config = []
    
    import_lambdas, endpoint_list = get_api_config(lambdas_path)
    
    for ep in endpoint_list:
        endpoints_config.append(generate_fastapi_routes_from_openapi_path(ep))


    output_file_str = """from fastapi import APIRouter
from fastapi import Request
from fastapi import Body, Header, Query, Response
from core_http.utils import get_body, get_status_code
import json
import base64
import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict, List, Any, cast

class MockContext:
    def __init__(self):
        self.function_name = "role_users_report"
        self.memory_limit_in_mb = 50
        self.invoked_function_arn = "arn:aws:lambda:aws-region-1:123456789012:function:role_users_report"
        self.aws_request_id = str(uuid.uuid4())

async def build_event_from_request(request: Request) -> Dict[str, Any]:
    path_parameters = request.path_params
    body_bytes = await request.body()
    try:
        body_str = body_bytes.decode('utf-8') if body_bytes else None
    except UnicodeDecodeError:
        body_str = base64.b64encode(body_bytes).decode('utf-8') if body_bytes else None

    is_base64_encoded = False  # Cambia a True si decides codificar el body en base64

    headers = dict(request.headers)
    cookies = request.cookies

    query_params = dict(request.query_params)

    return {{
        "version": "2.0",
        "routeKey": "$default",
        "rawPath": request.url.path,
        "rawQueryString": request.url.query,
        "cookies": list(cookies.values()) if cookies else [],
        "headers": headers,
        "queryStringParameters": query_params if query_params else None,
        "requestContext": {{
            "accountId": "123456789012",
            "apiId": "api-id",
            "authentication": {{
                "clientCert": {{
                    "clientCertPem": "CERT_CONTENT",
                    "subjectDN": "www.example.com",
                    "issuerDN": "Example issuer",
                    "serialNumber": "a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1",
                    "validity": {{
                        "notBefore": "May 28 12:30:02 2019 GMT",
                        "notAfter": "Aug  5 09:36:04 2021 GMT"
                    }}
                }}
            }},
            "authorizer": {{
                "jwt": {{
                    "claims": {{
                        "claim1": "value1",
                        "claim2": "value2"
                    }},
                    "scopes": [
                        "scope1",
                        "scope2"
                    ]
                }}
            }},
            "domainName": "id.execute-api.us-east-1.amazonaws.com",
            "domainPrefix": "id",
            "http": {{
                "method": request.method,
                "path": request.url.path,
                "protocol": request.scope.get("http_version", "HTTP/1.1"),
                "sourceIp": request.client.host if request.client else "127.0.0.1",
                "userAgent": headers.get("user-agent", "")
            }},
            "requestId": str(uuid.uuid4()),
            "routeKey": "$default",
            "stage": "$default",
            "time": datetime.utcnow().strftime("%d/%b/%Y:%H:%M:%S +0000"),
            "timeEpoch": int(datetime.utcnow().timestamp() * 1000)
        }},
        "body": body_str,
        "pathParameters": path_parameters,
        "isBase64Encoded": is_base64_encoded
    }}

{IMPORT_LAMBDAS}

router = APIRouter()

{IMPORT_ENDPOINTS}
    """.format(
        IMPORT_LAMBDAS="\n".join(import_lambdas),
        IMPORT_ENDPOINTS="\n".join(endpoints_config)
    )

    output_path = base_path / "src/api_local/router.py"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w+", encoding="utf-8") as f:
        f.write(output_file_str)
