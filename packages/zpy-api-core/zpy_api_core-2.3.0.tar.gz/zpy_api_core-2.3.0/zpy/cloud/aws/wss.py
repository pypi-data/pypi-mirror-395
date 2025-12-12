from dataclasses import dataclass
from typing import Optional, Mapping, Any, Callable
from json import loads as json_loads
import json
import logging
import traceback

def ok(body: dict, status_code: int = 200) -> dict:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def error(message: str, status_code: int = 400) -> dict:
    return ok({"ok": False, "error": message}, status_code)


# Custom exceptions
class ValidationError(Exception): ...


class AuthError(Exception): ...


class NotFoundError(Exception): ...


@dataclass(frozen=True)
class WSRequestContext:
    connection_id: str
    domain_name: str
    stage: str
    route_key: str
    event_type: str


@dataclass(frozen=True)
class WSApiEvent:
    raw: Mapping[str, Any]
    ctx: WSRequestContext
    query: Mapping[str, str]
    headers: Mapping[str, str]
    body: Optional[str] = None

    @staticmethod
    def from_event(event: Mapping[str, Any]) -> "WSApiEvent":
        rc = event.get("requestContext", {})
        q = event.get("queryStringParameters") or {}
        h = event.get("headers") or {}
        is_base64 = event.get("isBase64Encoded", False)
        raw_body = event.get("body", None)
        body = json_loads(raw_body) if raw_body else None

        if is_base64 and (b := event.get("body")):
            import base64

            b = base64.b64decode(b).decode("utf-8")
            body = json_loads(b) if b else None
        return WSApiEvent(
            raw=event,
            ctx=WSRequestContext(
                connection_id=rc.get("connectionId", ""),
                domain_name=rc.get("domainName", ""),
                stage=rc.get("stage", ""),
                route_key=rc.get("routeKey", ""),
                event_type=rc.get("eventType", ""),
            ),
            query=q,
            headers=h,
            body=body,
        )

    def get_query(self, name: str, default: Optional[str] = None) -> Optional[str]:
        v = self.query.get(name)
        return v if v is not None else default

    def get_header(self, name: str, default: Optional[str] = None) -> Optional[str]:
        v = self.headers.get(name)
        return v if v is not None else default

    def get_body(self) -> Optional[Any]:
        return self.body

    def to_dict(self) -> Mapping[str, Any]:
        return {
            "ctx": {
                "connection_id": self.ctx.connection_id,
                "domain_name": self.ctx.domain_name,
                "stage": self.ctx.stage,
            },
            "query": self.query,
            "headers": self.headers,
            "route": self.ctx.route_key,
            "event": self.ctx.event_type,
            "body": self.body,
        }


class WebSocketEventHandler:

    def __init__(
        self,
        on_connect: Optional[Callable[[WSApiEvent, Any], dict]] = None,
        on_disconnect: Optional[Callable[[WSApiEvent, Any], dict]] = None,
        on_message: Optional[Callable[[WSApiEvent, Any], dict]] = None,
    ):
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        self.on_message = on_message
        self.logger = logging.getLogger(__name__)

    def handle(self, event: dict[str, Any], context=None) -> dict:
        try:
            ws_event = WSApiEvent.from_event(event)
            result = None
            if ws_event.ctx.event_type == "CONNECT" and self.on_connect:
                result = self.on_connect(ws_event, context)
            elif ws_event.ctx.event_type == "DISCONNECT" and self.on_disconnect:
                result = self.on_disconnect(ws_event, context)
            elif ws_event.ctx.event_type == "MESSAGE" and self.on_message:
                result = self.on_message(ws_event, context)
            else:
                raise ValueError(f"Unhandled event type: {ws_event.ctx.event_type}")
            return ok(result, 200)
        except ValidationError as ve:
            self.logger.warning(f"Validation error: {ve}", exc_info=True)
            return error(str(ve), 400)
        except AuthError as ae:
            self.logger.warning(f"Auth error: {ae}", exc_info=True)
            return error(str(ae), 401)
        except Exception as ex:
            self.logger.exception(f"Internal error: {ex}", exc_info=True)
            return error("Internal error", 500)
