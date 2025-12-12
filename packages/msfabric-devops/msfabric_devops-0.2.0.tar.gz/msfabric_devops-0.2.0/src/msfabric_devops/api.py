from . import config
import time
import json
import requests

def invoke_fabric_api_request(
    uri,
    token=None,
    method="GET",
    body=None,
    content_type="application/json; charset=utf-8",
    timeout_sec=240,
    retry_count=0,
    api_url=config.API_URL
):
    headers = {
        "Content-Type": content_type,
        "Authorization": f"Bearer {token}"
    }

    if not api_url:
        raise ValueError("api_url must be specified")

    request_url = f"{api_url.rstrip('/')}/{uri.lstrip('/')}"

    try:
        response = requests.request(
            method=method.upper(),
            url=request_url,
            headers=headers,
            json=body if isinstance(body, (dict, list)) else None,
            data=None if isinstance(body, (dict, list)) else body,
            timeout=timeout_sec
        )

        # Handle Long-Running Operation (202)
        if response.status_code == 202:
            while True:
                async_url = response.headers.get("Location")
                if not async_url:
                    raise Exception("LRO response has no Location header")
                print("LRO - Waiting for request to complete in service.")
                time.sleep(5)
                lro_response = requests.get(async_url, headers=headers)
                lro_content = lro_response.json()
                status = lro_content.get("status", "").lower()

                if status in ["succeeded", "failed"]:
                    if status == "succeeded":
                        result_url = lro_response.headers.get("Location")
                        if result_url:
                            response = requests.get(result_url, headers=headers)
                        else:
                            return None  # LRO has no result
                    else:
                        error = lro_content.get("error")
                        if error:
                            raise Exception(f"LRO API Error: {error.get('errorCode')} - {error.get('message')}")
                    break

        # Parse JSON response
        if response.content:
            content_bytes = response.content
            content_text = content_bytes[3:].decode("utf-8") if content_bytes.startswith(b'\xef\xbb\xbf') else response.text
            json_result = json.loads(content_text)

            # ✅ Raise if API returned an error in JSON
            if isinstance(json_result, dict) and "errorCode" in json_result:
                raise Exception(f"API Error: {json_result['errorCode']} - {json_result.get('message')}")

            # Return value if present
            if isinstance(json_result, dict) and "value" in json_result:
                json_result = json_result["value"]

            return json_result

    except requests.exceptions.RequestException as ex:
        response = getattr(ex, 'response', None)

        # Handle throttling (429)
        if response and response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            retry_after_seconds = int(retry_after) + 5 if retry_after and retry_after.isdigit() else 60
            print(f"Too many requests (429). Sleeping {retry_after_seconds}s.")
            time.sleep(retry_after_seconds)
            if retry_count < 3:
                return invoke_fabric_api_request(
                    uri=uri,
                    token=token,
                    method=method,
                    body=body,
                    content_type=content_type,
                    timeout_sec=timeout_sec,
                    retry_count=retry_count + 1,
                    api_url=api_url
                )
            else:
                raise Exception(f"Exceeded max retries after 429")
        else:
            raise Exception(str(ex))
