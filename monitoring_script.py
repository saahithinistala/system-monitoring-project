from datetime import datetime
import subprocess
import requests

class Monitoring:
    def __init__(self, log):
        self.log = log

    def _log_and_print(self, message):
        with open(self.log, "a") as file:
            file.write(f"{message}\n")
            print(message)

    def disk_usage(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cmd = ["ssh", "your_username@your_server", "df -h | awk '$9 ~ /^\/System/ {print $5, $9}'"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        message = f"\n{timestamp}: DISK USAGE"
        self._log_and_print(message)

        for output in result.stdout.splitlines():
            parts = output.split(" ", 1)
            capacity = int(parts[0].replace("%", ''))
            mount = parts[1]

            if capacity < 70:
                message = f"{mount}: {capacity}% -> Normal"
                self._log_and_print(message)
            elif 70 <= capacity <= 80:
                message = f"{mount}: {capacity}% -> WARNING -- Start Watching"
                self._log_and_print(message)
            elif 80 <= capacity <= 90:
                message = f"{mount}: {capacity}% -> HIGH -- Needs attention"
                self._log_and_print(message)
            elif capacity > 90:
                message = f"{mount}: {capacity}% -> CRITICAL -- Needs immediate action"
                self._log_and_print(message)

    def service_status(self, service):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cmd = ["ssh", "your_username@your_server", f"ps aux | grep {service} | grep -v grep| wc -l"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        message = f"\n{timestamp}: SERVICE STATUS"
        self._log_and_print(message)

        output = result.stdout.strip()
        if int(output) > 0:
            message = f"{service} -> RUNNING"
            self._log_and_print(message)
        else:
            message = f"{service} -> NOT RUNNING"
            self._log_and_print(message)

    def log_error_detection(self, app_log):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"\n{timestamp}: LOG ERROR DETECTION"
        self._log_and_print(message)

        with open(app_log, "r") as application_log:
            lines = application_log.readlines()

            error_list = []
            failed_list = []
            critical_list = []
            for data in lines:
                parts = data.strip().split(" ", 3)
                if len(parts) < 4:
                    continue

                keyword = parts[2]
                if keyword == "ERROR":
                    error_list.append(data)
                elif keyword == "FAILED":
                    failed_list.append(data)
                elif keyword == "CRITICAL":
                    critical_list.append(data)

            message = f"Source log file: {app_log}"
            self._log_and_print(message)

            message = "Keyword searched: ERROR"
            self._log_and_print(message)
            for err_data in error_list:
                message = f"{err_data.strip()}"
                self._log_and_print(message)
            message = f"Total Matches: {len(error_list)}"
            self._log_and_print(message)

            message = "Keyword searched: FAILED"
            self._log_and_print(message)
            for err_data in failed_list:
                message = f"{err_data.strip()}"
                self._log_and_print(message)
            message = f"Total Matches: {len(failed_list)}"
            self._log_and_print(message)

            message = "Keyword searched: CRITICAL"
            self._log_and_print(message)
            for err_data in critical_list:
                message = f"{err_data.strip()}"
                self._log_and_print(message)
            message = f"Total Matches: {len(critical_list)}"
            self._log_and_print(message)

    def api_health_check(self, api_url):
        error_messages = {
            "Failed to resolve": "DNS Failure",
            "timed out": "Timeout",
            "Connection refused": "Connection Error",
            "Invalid URL": "Invalid API URL",
            "SSL": "SSL Issue"
        }
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"\n{timestamp}: API HEALTH CHECK"
        self._log_and_print(message)

        try:
            result = requests.get(api_url, timeout=5)
            if 200 <= result.status_code < 300:
                message = f"URL: {api_url}\nAPI Health: Healthy\nStatus Code: {result.status_code}\nStatus: Reachable"
            elif result.status_code >= 400:
                message = f"URL: {api_url}\nAPI Health: Unhealthy\nStatus Code: {result.status_code}\nStatus: Reachable"
            elif 300 <= result.status_code < 400:
                message = f"URL: {api_url}\nWARNING!!\nAPI Health: Unhealthy\nStatus Code: {result.status_code}\nStatus: Reachable"
            else:
                message = f"URL: {api_url}\nAPI Health: Unhealthy\nStatus Code: {result.status_code}\nStatus: Reachable"

            self._log_and_print(message)

        except requests.exceptions.RequestException as url_exception:
            reason = "API Request Failed"
            for error, error_reason in error_messages.items():
                if error in str(url_exception):
                    reason = error_reason
                    break
            message = f"URL: {api_url}\nAPI Health: Unhealthy\nReason: {reason}\nStatus: Not Reachable"
            self._log_and_print(message)

