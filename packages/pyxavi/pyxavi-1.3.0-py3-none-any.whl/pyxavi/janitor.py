import requests
import socket


class Janitor:
    """Class that wraps up the API to report to Janitor

    Find Janitor at:
        https://github.com/XaviArnaus/janitor

    Parameters:
    - `remote_url` [str, mandatory] host and port where to deliver
        the messages. ie: `http://localhost:5000`
    - `hostname` [str, optional] the string that will identify the
        messages sender. If none comes it will discover the hostname
        of the machine.

    :Authors:
        Xavier Arnaus <xavi@arnaus.net>

    """

    class MessageType:
        """Class that identifies the message types for every message sent.

        Values here are directly harcoded from the ones set in the Janitor package

        :Authors:
            Xavier Arnaus <xavi@arnaus.net>

        """

        NONE = "none"
        INFO = "info"
        WARNING = "warning"
        ERROR = "error"
        ALARM = "alarm"

    _remote_url: str = None
    _hostname: str = None

    def __init__(self, remote_url: str, hostname: str = None) -> None:
        self._remote_url = remote_url

        if hostname is None:
            self._hostname = self._get_hostname()
        else:
            self._hostname = hostname

    def _get_hostname(self) -> str:
        return socket.gethostname()

    def _send_message(self, params: dict) -> int:
        r = requests.post(f"{self._remote_url}/message", data=params)
        return r.status_code

    def log(self, message: str, summary: str = None) -> int:
        params = {
            "hostname": self._hostname,
            "message": message,
            "message_type": self.MessageType.NONE
        }
        if summary is not None:
            params["summary"] = summary

        return self._send_message(params)

    def info(self, message: str, summary: str = None) -> int:
        params = {
            "hostname": self._hostname,
            "message": message,
            "message_type": self.MessageType.INFO
        }
        if summary is not None:
            params["summary"] = summary

        return self._send_message(params)

    def warning(self, message: str, summary: str = None) -> int:
        params = {
            "hostname": self._hostname,
            "message": message,
            "message_type": self.MessageType.WARNING
        }
        if summary is not None:
            params["summary"] = summary

        return self._send_message(params)

    def error(self, message: str, summary: str = None) -> int:
        params = {
            "hostname": self._hostname,
            "message": message,
            "message_type": self.MessageType.ERROR
        }
        if summary is not None:
            params["summary"] = summary

        return self._send_message(params)

    def alarm(self, message: str, summary: str = None) -> int:
        params = {
            "hostname": self._hostname,
            "message": message,
            "message_type": self.MessageType.ALARM
        }
        if summary is not None:
            params["summary"] = summary

        return self._send_message(params)
