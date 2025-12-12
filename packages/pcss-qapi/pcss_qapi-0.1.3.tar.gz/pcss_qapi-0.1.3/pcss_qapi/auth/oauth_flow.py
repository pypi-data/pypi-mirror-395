"""OAuth authorization management"""
import time
import base64
import json
from typing import Any
import requests


def _print_nothing(width):
    print("".join(' ' for _ in range(width)), end='\r')


def _print_formatted_time(time_seconds):
    spinner = "⣾⣽⣻⢿⡿⣟⣯⣷"

    minutes_left = time_seconds // 60
    seconds_left = time_seconds % 60

    minutes_string = f'{minutes_left} minutes'
    seconds_string = f'{seconds_left} seconds'

    s = f"""{spinner[time_seconds % len(spinner)]} Waiting... {" ".join([minutes_string if minutes_left else "",
                                                                         seconds_string])} remaining to complete authorization."""
    print(s, end='\r')
    return len(s)


def _show_error(error_type: str | None, last_printed_line_len: int):
    if error_type == "authorization_pending":
        pass
    else:
        error_message = {
            'slow_down': '⏳ Server requested slower polling. Increasing interval.',
            'access_denied': '❌ Access was denied by user.',
            None: '❌ Failed to parse polling error response.'
        }.get(error_type, '❌ Failed to parse polling error response.')

        _print_nothing(last_printed_line_len)
        print(error_message)


def _decode_jwt_payload(token):
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        padded = parts[1] + "=" * (-len(parts[1]) % 4)
        decoded_bytes = base64.urlsafe_b64decode(padded)
        return json.loads(decoded_bytes)
    except Exception:  # pylint:disable = broad-exception-caught
        return None


class OAuthManager:
    """Token handler"""

    def __init__(self, client_id, issuer, min_ttl) -> None:
        self.client_id = client_id
        self.issuer = issuer
        self.min_ttl = min_ttl

        self.token_endpoint: str | None = None
        self.device_endpoint: str | None = None

        self._try_get_urls()

    def _try_get_urls(self) -> bool:
        success = False
        try:
            discovery_url = f"{self.issuer}/.well-known/openid-configuration"
            discovery = requests.get(discovery_url, timeout=5).json()
            self.token_endpoint = discovery["token_endpoint"]
            self.device_endpoint = discovery["device_authorization_endpoint"]
            success = True
        except requests.exceptions.ConnectionError:
            pass
        return success

    def is_token_valid(self, token):
        """Check if token will be valid for more than self.min_ttl seconds."""
        payload = _decode_jwt_payload(token)
        if not payload or "exp" not in payload:
            return False
        exp = payload["exp"]
        return (exp - int(time.time())) >= self.min_ttl

    def get_refreshed_tokens(self, refresh_token) -> tuple[str | None, str | None]:
        """Get new access and refresh tokens fr"""
        if (self.token_endpoint is None or self.device_endpoint is None) and not self._try_get_urls():
            raise RuntimeError("Authentication server inaccessible")

        resp = requests.post(
            self.token_endpoint,
            data={
                "grant_type": "refresh_token",
                "client_id": self.client_id,
                "refresh_token": refresh_token
            },
            timeout=20)
        if resp.ok:
            data = resp.json()
            return data.get("access_token"), data.get("refresh_token")

        # print(f"⚠️ Refresh grant failed (HTTP {resp.status_code}): {resp.text}")
        return None, None

    def _get_device_flow_data(self) -> dict[str, Any]:
        response = requests.post(
            self.device_endpoint,
            data={
                "client_id": self.client_id
            },
            timeout=20)
        if not response.ok:
            try:
                error_data = response.json()
                error = error_data.get("error", "unknown_error")
                description = error_data.get("error_description", "No description.")
            except Exception:  # pylint:disable = broad-exception-caught
                error = "unknown_error"
                description = response.text
            raise RuntimeError(f"Device Authorization Error: {error} — {description}")  # pylint:disable = broad-exception-raised

        if 'application/json' not in response.headers.get('content-type', ''):
            raise ValueError("Invalid device flow response.")

        data = response.json()
        required_fields = ["verification_uri_complete", "device_code", "expires_in"]
        if not all(field in data for field in required_fields):
            raise ValueError("Missing expected fields in device flow response.")  # pylint:disable = broad-exception-raised

        return data

    def _poll_auth_server(self, device_code) -> tuple[str | None, str | None, str | None]:
        poll = requests.post(
            self.token_endpoint,
            data={
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "device_code": device_code,
                "client_id": self.client_id
            },
            timeout=20)
        if poll.status_code == 200:
            t = poll.json()
            return t.get("access_token"), t.get("refresh_token"), None
        if poll.status_code == 400:
            err = None
            try:
                err = poll.json().get("error")
            except requests.JSONDecodeError:
                pass
            return None, None, err
        return None, None, None

    def get_device_flow_tokens(self) -> tuple[str | None, str | None]:  # pylint:disable = too-many-statements,too-many-locals
        """Get new access and refresh tokens from device flow."""
        if (self.token_endpoint is None or self.device_endpoint is None) and not self._try_get_urls():
            raise RuntimeError("Authentication server inaccessible")

        data = self._get_device_flow_data()

        print("\n🔐 Authorize Access")
        print("----------------------------------------")
        print("You are about to be redirected to an authorization server.")
        print("There, you will be asked to grant access permissions.")
        print("This allows the system to act on your behalf using delegated access.")
        print("Please confirm only if you trust this application.")
        print(f"➡️  Click to authorize: {data['verification_uri_complete']}")
        print()

        device_code = data["device_code"]
        interval = data.get("interval", 5)
        expires_in = data["expires_in"]

        sleep_time = 1
        interval_count = 0

        last_printed_line_len = 0
        while expires_in > 0:
            if interval_count < 0:
                interval_count = interval

                access_token, refresh_token, error_type = self._poll_auth_server(device_code)

                if access_token is not None and refresh_token is not None:
                    _print_nothing(last_printed_line_len)
                    print("✅ Access granted.")
                    return access_token, refresh_token

                _show_error(error_type, last_printed_line_len)

                if error_type == 'slow_down':
                    interval += 1
                elif error_type != 'authorization_pending':
                    return None, None

            expires_in -= sleep_time
            interval_count -= sleep_time
            last_printed_line_len = _print_formatted_time(expires_in)
            time.sleep(sleep_time)

        print("\n❌ Timeout: Authorization not completed in time.")
        return None, None
