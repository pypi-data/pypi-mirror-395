import datetime
import json
import os
import sys
import time
import traceback
from typing import Any, Dict, Optional

import requests
import requests.auth
import yaml
from pushover import Pushover

VERSION = '0.1.1'
STATE_REFRESH_INTERVAL = 60

class Tracing:

    _last_report: float | None = None
    _last_state_refresh: float | None = None
    _state: Dict[str, Any] = {}

    def __init__(self, context: Any, max_interval: int = 60) -> None:
        self.log("initialising tracing")

        self.start_time: float = time.time()

        timestamp: str = datetime.datetime.fromtimestamp(self.start_time).strftime('%Y-%m-%d %H:%M:%S')
        self.log(f"start time: {timestamp}")

        self.function_name: str

        if type(context) is str:
            self.function_name = context
        else:
            self.function_name = context.function_name

        if os.path.exists('/etc/tracing.yaml'):
            config: Dict[str, str] = yaml.safe_load(open('/etc/tracing.yaml').read())

            os.environ['TRACING_ENDPOINT'] = config['endpoint']
            os.environ['TRACING_PUSHOVER_USER'] = config['pushover_user']
            os.environ['TRACING_PUSHOVER_APP'] = config['pushover_app']

            if 'username' in config and 'password' in config:
                os.environ['TRACING_USERNAME'] = config['username']
                os.environ['TRACING_PASSWORD'] = config['password']

        self.endpoint: str = os.environ['TRACING_ENDPOINT']

        self.log(f"tracing endpoint: {self.endpoint}")

        self.auth: Optional[requests.auth.HTTPBasicAuth]

        if 'TRACING_USERNAME' in os.environ and 'TRACING_PASSWORD' in os.environ:
            self.auth = requests.auth.HTTPBasicAuth(
                os.environ['TRACING_USERNAME'],
                os.environ['TRACING_PASSWORD']
            )
        else:
            self.auth = None

        self.pushover: Pushover = Pushover(os.environ['TRACING_PUSHOVER_USER'], api_token=os.environ['TRACING_PUSHOVER_APP'])

        self.proxies: Dict[str, str]

        if 'SOCKS5_PROXY' in os.environ:
            self.proxies = {'https': f"socks5h://{os.environ['SOCKS5_PROXY']}"}
            self.log(f"using proxy: {os.environ['SOCKS5_PROXY']}")
        else:
            self.proxies = {}
            self.log("not using proxy")

        self.max_interval: int = max_interval


    def log(self, message: str) -> None:
        if 'DEBUG' in os.environ:
            sys.stdout.write(message + "\n")
            sys.stdout.flush()


    def get_state(self) -> Dict[str, Any]:
        self.log(f"getting state for function: {self.function_name}")

        for i in range(0, 5):
            try:
                resp: requests.Response = requests.get(
                    f"{self.endpoint}/tracing/{self.function_name}",
                    timeout=10,
                    auth=self.auth,
                    proxies=self.proxies
                )

                data: Dict[str, Any] = json.loads(resp.text)

                self.log(f"state returned: {data}")

                return data

            except Exception:
                pass

        return {}


    def success(self) -> None:
        timestamp: int = int(time.time())
        runtime: float = time.time() - self.start_time

        if Tracing._last_state_refresh is None or (time.time() - Tracing._last_state_refresh) > STATE_REFRESH_INTERVAL:
            Tracing._state = self.get_state()
            Tracing._last_state_refresh = time.time()

        if 'success' in Tracing._state and not Tracing._state['success']:
            self.pushover.send('resolved', self.function_name)

        if 'success' not in Tracing._state or not Tracing._state['success'] or Tracing._last_report is None or (time.time() - Tracing._last_report) \
            > self.max_interval:

            try:
                self.send_state(True, timestamp, runtime)
                Tracing._last_report = time.time()
                Tracing._state['success'] = True
            except Exception as e:
                sys.stderr.write(f"failed to send metrics: {str(e)}\n")
                sys.stderr.flush()

                raise e


    def send_state(self, success: bool, timestamp: int, runtime: float) -> None:
        self.log("emitting state:\n")
        self.log(f"success: {int(success)}\n")
        self.log(f"runtime: {runtime:.2f} seconds\n")

        for i in range(0, 5):
            try:
                resp: requests.Response = requests.post(
                    f"{self.endpoint}/tracing/{self.function_name}",
                    json={
                        'success': success,
                        'key': self.function_name,
                        'timestamp': timestamp,
                        'runtime': runtime,
                        'version': VERSION,
                    },
                    headers={
                        'Content-Type': 'application/json'
                    },
                    timeout=10,
                    auth=self.auth,
                    proxies=self.proxies
                )

                self.log(f"state response: {resp.status_code} - {resp.text}")

                if resp.status_code == 200:
                    break

            except Exception as e:
                self.log(f"error sending data: {e}")
                time.sleep(1)


    def failure(self) -> None:
        timestamp: int = int(time.time())
        runtime: float = time.time() - self.start_time

        if Tracing._last_state_refresh is None or (time.time() - Tracing._last_state_refresh) > STATE_REFRESH_INTERVAL:
            Tracing._state = self.get_state()
            Tracing._last_state_refresh = time.time()

        exc_type, exc_value, exc_traceback = sys.exc_info()

        data: Dict[str, Any] = {
            'success': False,
            'key': self.function_name,
            'timestamp': timestamp,
            'runtime': runtime,
            'version': VERSION,
            'exception_type': str(exc_type.__name__) if exc_type else 'Unknown',
            'exception_message': str(exc_value),
        }

        report = False

        if 'exception_type' not in Tracing._state or 'exception_message' not in Tracing._state or data['exception_type'] != Tracing._state['exception_type'] \
            or data['exception_message'] != Tracing._state['exception_message']:

            trace_identifier: str = f"{self.function_name}_{int(time.time() * 1000000)}"

            content: str = f"Function: {self.function_name}\n"
            content += f"Runtime: {runtime:.2f} seconds\n"
            content += f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            content += traceback.format_exc()

            url: str = f"{self.endpoint}/trace/{self.function_name}/{trace_identifier}"

            exception: str = traceback.format_exception_only(*sys.exc_info()[:2])[-1].strip()

            self.pushover.send(exception, title=self.function_name, url=url)

            data['trace_identifier'] = trace_identifier
            data['trace'] = content

            report = True

        if 'success' in Tracing._state and not Tracing._state['success'] and not report:
            return

        if report:
            for i in range(0, 5):
                try:
                    resp: requests.Response = requests.post(
                        f"{self.endpoint}/tracing/{self.function_name}",
                        json=data,
                        headers={
                            'Content-Type': 'application/json'
                        },
                        timeout=10,
                        auth=self.auth,
                        proxies=self.proxies
                    )

                    if resp.status_code == 200:
                        Tracing._state['success'] = False
                        break

                except Exception:
                    pass
