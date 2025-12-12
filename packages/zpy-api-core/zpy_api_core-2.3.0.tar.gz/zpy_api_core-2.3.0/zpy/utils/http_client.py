from enum import Enum
from typing import Any, List, Optional, Tuple, Callable, Dict, Union
from requests import post, Response, get, patch, delete, put
from zpy.logger import zL, ZLogger
from datetime import timedelta


class HLevels(Enum):
    URL = 1
    HEADERS = 2
    PARAMS = 3
    PAYLOAD = 4

    @staticmethod
    def all():
        return [HLevels.URL, HLevels.HEADERS, HLevels.PARAMS, HLevels.PAYLOAD]

    @staticmethod
    def url_and_body():
        return [HLevels.URL, HLevels.PAYLOAD]


def zhl_write(text: str, value: Any, logger: ZLogger = None):
    def wrapper():
        if value is not None:
            if not logger:
                zL.i(f"{text} {value}")
                return
            logger.info(f"{text} {value}")

    return wrapper


class ZHttp:
    """HTTP Wrapper


    Raises:
        ValueError: [description]
    """

    global_options: dict = {"BASE_URL": None, "LOG_OPTIONS": None}

    @staticmethod
    def setup(base: str, log_options: List[HLevels] = None) -> None:
        ZHttp.global_options["BASE_URL"] = base
        ZHttp.global_options["LOG_OPTIONS"] = log_options

    @staticmethod
    def __prepare_request__(
            url, path, params, headers, data, json, log_options, logger: ZLogger = None, method: str = 'POST'
    ) -> Tuple[str, List[HLevels], dict]:
        final_url: str = ZHttp.global_options["BASE_URL"]
        if url is not None and path is not None:
            final_url = f"{url}{path}"
        if url is not None and path is None:
            final_url = url
        if url is None and path is not None:
            final_url = f"{final_url}{path}"

        if final_url is None:
            raise ValueError("URL not configured!")

        real_log_options = ZHttp.global_options["LOG_OPTIONS"]
        metadata = {
            "url": final_url,
            "method": method,
            "params": params,
            "headers": headers,
            "body": data if json is None else json
        }
        try:
            data_to_log: Dict[HLevels, Callable] = {
                HLevels.URL: zhl_write(f"Start HTTP [{method}] -", final_url, logger),
                HLevels.PARAMS: zhl_write(f"Params:", params, logger),
                HLevels.HEADERS: zhl_write(f"Headers:", headers, logger),
                HLevels.PAYLOAD: zhl_write(f"Body:", data if json is None else json, logger)
            }

            if log_options is not None and len(log_options) > 0:
                real_log_options = log_options

            if not real_log_options:
                return final_url, real_log_options, metadata

            for i in real_log_options:
                writer = data_to_log.get(i, None)
                if writer:
                    writer()
        except Exception as e:
            ZHttp.__log_exception__(logger, "An error occurred while logging http request.")
        full_metadata = {
            'request': metadata,
            'response': {},
            'error': None
        }
        return final_url, real_log_options, full_metadata

    @staticmethod
    def __log_exception__(logger: ZLogger = None, msg: str = "The http request failed..."):
        if not logger:
            zL.ex(msg)
            return
        logger.info(msg)

    @staticmethod
    def __logging_response__(
            result: Response, final_url, log_response_headers, real_log_options, logger: ZLogger = None
    ) -> dict:
        if not real_log_options:
            return {}
        parsed = None
        raw_body = None
        try:
            zhl_write(f"Response raw body:", result.content, logger)()
            raw_body = result.content
            parsed = result.json()
        except Exception as e:
            zhl_write(f"ZHttp Error", f"Fail when read raw response content: {e}", logger)()

        elapsed_time = str(timedelta(seconds=result.elapsed.total_seconds()))
        response_headers = dict(
            zip(result.headers.keys(), result.headers.values())) if log_response_headers is True else None
        metadata = {
            "elapsed": elapsed_time,
            "body": raw_body if parsed is None else parsed,
            "status": result.status_code,
            "headers": response_headers
        }
        response_logs: Dict[HLevels, Callable] = {
            HLevels.URL: zhl_write(f"End HTTP [POST] - {elapsed_time} - {result.status_code}", final_url, logger),
            HLevels.HEADERS: zhl_write(
                f"Response Headers:",
                response_headers,
                logger
            ),
            HLevels.PAYLOAD: zhl_write(f"Response Body:", parsed, logger)
        }
        for i in real_log_options:
            writer = response_logs.get(i, None)
            if writer:
                writer()
        return metadata

    @staticmethod
    def get(
            url: Optional[str] = None,
            path: Optional[str] = None,
            params: Any = None,
            data: Any = None,
            headers: Any = None,
            cookies: Any = None,
            files: Any = None,
            auth: Any = None,
            timeout: Any = None,
            allow_redirects: bool = None,
            proxies: Any = None,
            hooks: Any = None,
            stream: Any = None,
            verify: Any = None,
            cert: Any = None,
            json: Any = None,
            log_options: List[HLevels] = None,
            log_response_headers: bool = False,
            control_failure: bool = False,
            logger: ZLogger = None,
            wrap_in_zhttp: bool = False
    ) -> Optional[Union[Response, 'ZHttpResponse']]:
        final_url, real_log_level, request_meta = ZHttp.__prepare_request__(
            url, path, params, headers, data, json, log_options, logger
        )
        try:
            result: Response = get(
                url=final_url,
                json=json,
                data=data,
                params=params,
                headers=headers,
                cookies=cookies,
                files=files,
                auth=auth,
                timeout=timeout,
                allow_redirects=allow_redirects,
                proxies=proxies,
                hooks=hooks,
                stream=stream,
                verify=verify,
                cert=cert,
            )
            if real_log_level is not None:
                response_metadata = ZHttp.__logging_response__(
                    result, final_url, log_response_headers, real_log_level, logger
                )
                request_meta['response'] = response_metadata
            if wrap_in_zhttp is True:
                return ZHttpResponse.of(result, request_meta)
            return result
        except Exception as e:
            ZHttp.__log_exception__(logger)
            if control_failure is False:
                raise e
            if wrap_in_zhttp is True:
                request_meta['error'] = str(e)
                return ZHttpResponse.of(None, request_meta)
        return None

    @staticmethod
    def post(
            url: Optional[str] = None,
            path: Optional[str] = None,
            params: Any = None,
            data: Any = None,
            headers: Any = None,
            cookies: Any = None,
            files: Any = None,
            auth: Any = None,
            timeout: Any = None,
            allow_redirects: bool = None,
            proxies: Any = None,
            hooks: Any = None,
            stream: Any = None,
            verify: Any = None,
            cert: Any = None,
            json: Any = None,
            log_options: List[HLevels] = None,
            log_response_headers: bool = False,
            control_failure: bool = False,
            logger: ZLogger = None,
            wrap_in_zhttp: bool = False
    ) -> Optional[Union[Response, 'ZHttpResponse']]:
        final_url, real_log_level, request_meta = ZHttp.__prepare_request__(
            url, path, params, headers, data, json, log_options, logger
        )
        try:
            result: Response = post(
                url=final_url,
                json=json,
                data=data,
                params=params,
                headers=headers,
                cookies=cookies,
                files=files,
                auth=auth,
                timeout=timeout,
                allow_redirects=allow_redirects,
                proxies=proxies,
                hooks=hooks,
                stream=stream,
                verify=verify,
                cert=cert,
            )
            if real_log_level is not None:
                response_metadata = ZHttp.__logging_response__(
                    result, final_url, log_response_headers, real_log_level, logger
                )
                request_meta['response'] = response_metadata
            if wrap_in_zhttp is True:
                return ZHttpResponse.of(result, request_meta)
            return result
        except Exception as e:
            ZHttp.__log_exception__(logger)
            if control_failure is False:
                raise e
            if wrap_in_zhttp is True:
                request_meta['error'] = str(e)
                return ZHttpResponse.of(None, request_meta)
        return None

    @staticmethod
    def put(
            url: Optional[str] = None,
            path: Optional[str] = None,
            params: Any = None,
            data: Any = None,
            headers: Any = None,
            cookies: Any = None,
            files: Any = None,
            auth: Any = None,
            timeout: Any = None,
            allow_redirects: bool = None,
            proxies: Any = None,
            hooks: Any = None,
            stream: Any = None,
            verify: Any = None,
            cert: Any = None,
            json: Any = None,
            log_options: List[HLevels] = None,
            log_response_headers: bool = False,
            control_failure: bool = False,
            logger: ZLogger = None,
            wrap_in_zhttp: bool = False
    ) -> Optional[Union[Response, 'ZHttpResponse']]:
        final_url, real_log_level, request_meta = ZHttp.__prepare_request__(
            url, path, params, headers, data, json, log_options, logger
        )
        try:
            result: Response = put(
                url=final_url,
                json=json,
                data=data,
                params=params,
                headers=headers,
                cookies=cookies,
                files=files,
                auth=auth,
                timeout=timeout,
                allow_redirects=allow_redirects,
                proxies=proxies,
                hooks=hooks,
                stream=stream,
                verify=verify,
                cert=cert,
            )
            if real_log_level is not None:
                response_metadata = ZHttp.__logging_response__(
                    result, final_url, log_response_headers, real_log_level, logger
                )
                request_meta['response'] = response_metadata
            if wrap_in_zhttp is True:
                return ZHttpResponse.of(result, request_meta)
            return result
        except Exception as e:
            ZHttp.__log_exception__(logger)
            if control_failure is False:
                raise e
            if wrap_in_zhttp is True:
                request_meta['error'] = str(e)
                return ZHttpResponse.of(None, request_meta)
        return None

    @staticmethod
    def patch(
            url: Optional[str] = None,
            path: Optional[str] = None,
            params: Any = None,
            data: Any = None,
            headers: Any = None,
            cookies: Any = None,
            files: Any = None,
            auth: Any = None,
            timeout: Any = None,
            allow_redirects: bool = None,
            proxies: Any = None,
            hooks: Any = None,
            stream: Any = None,
            verify: Any = None,
            cert: Any = None,
            json: Any = None,
            log_options: List[HLevels] = None,
            log_response_headers: bool = False,
            control_failure: bool = False,
            logger: ZLogger = None,
            wrap_in_zhttp: bool = False
    ) -> Optional[Union[Response, 'ZHttpResponse']]:
        final_url, real_log_level, request_meta = ZHttp.__prepare_request__(
            url, path, params, headers, data, json, log_options, logger
        )
        try:
            result: Response = patch(
                url=final_url,
                json=json,
                data=data,
                params=params,
                headers=headers,
                cookies=cookies,
                files=files,
                auth=auth,
                timeout=timeout,
                allow_redirects=allow_redirects,
                proxies=proxies,
                hooks=hooks,
                stream=stream,
                verify=verify,
                cert=cert,
            )
            if real_log_level is not None:
                response_meta = ZHttp.__logging_response__(
                    result, final_url, log_response_headers, real_log_level, logger
                )
                request_meta['response'] = response_meta
            if wrap_in_zhttp is True:
                return ZHttpResponse.of(result, request_meta)
            return result
        except Exception as e:
            ZHttp.__log_exception__(logger)
            if control_failure is False:
                raise e
            if wrap_in_zhttp is True:
                request_meta['error'] = str(e)
                return ZHttpResponse.of(None, request_meta)
        return None

    @staticmethod
    def delete(
            url: Optional[str] = None,
            path: Optional[str] = None,
            params: Any = None,
            data: Any = None,
            headers: Any = None,
            cookies: Any = None,
            files: Any = None,
            auth: Any = None,
            timeout: Any = None,
            allow_redirects: bool = None,
            proxies: Any = None,
            hooks: Any = None,
            stream: Any = None,
            verify: Any = None,
            cert: Any = None,
            json: Any = None,
            log_options: List[HLevels] = None,
            log_response_headers: bool = False,
            control_failure: bool = False,
            logger: ZLogger = None,
            wrap_in_zhttp: bool = False,
    ) -> Optional[Union[Response, 'ZHttpResponse']]:
        final_url, real_log_level, request_meta = ZHttp.__prepare_request__(
            url, path, params, headers, data, json, log_options, logger
        )
        try:
            result: Response = delete(
                url=final_url,
                json=json,
                data=data,
                params=params,
                headers=headers,
                cookies=cookies,
                files=files,
                auth=auth,
                timeout=timeout,
                allow_redirects=allow_redirects,
                proxies=proxies,
                hooks=hooks,
                stream=stream,
                verify=verify,
                cert=cert,
            )
            if real_log_level is not None:
                response_meta = ZHttp.__logging_response__(
                    result, final_url, log_response_headers, real_log_level, logger
                )
                request_meta['response'] = response_meta
            if wrap_in_zhttp is True:
                return ZHttpResponse.of(result, request_meta)
            return result
        except Exception as e:
            ZHttp.__log_exception__(logger)
            if control_failure is False:
                raise e
            if wrap_in_zhttp is True:
                request_meta['error'] = str(e)
                return ZHttpResponse.of(None, request_meta)
        return None


class ZHttpResponse(object):
    """
    Wrapper
    """

    @classmethod
    def of(cls, response: Response, metadata: dict = None):
        return cls(response, metadata)

    def __init__(self, response: Response, metadata: dict = None):
        self.raw = response
        self.metadata = metadata

    def json(self) -> dict:
        return self.raw.json()

    def meta(self) -> dict:
        return self.metadata

    def status_is(self, status: int) -> bool:
        return False if self.raw is None else self.raw.status_code == status

    def status_is_and(self, status: int, action: Callable[[Response], Optional[Any]]) -> Optional[Any]:
        """

        @param status:
        @param action:
        @return:
        """
        if self.raw is not None and self.raw.status_code == status:
            return action(self.raw)
        return None

    def is_ok(self) -> bool:
        """

        @return: http status response is success
        """
        return False if self.raw is None else self.raw.ok
