import requests
import ipaddress
import logging

EXTERNAL_SERVICE_IPv4 = {
    "ipfy IPv4": "https://api.ipify.org",
    "ident.me IPv4": "https://v4.ident.me/",
    "dnsomatic IPv4": "http://myip.dnsomatic.com",
}

EXTERNAL_SERVICE_IPv6 = {
    "ident.me IPv6": "https://v6.ident.me/",
}


class Network:

    @staticmethod
    def is_valid_ipv4(address: str) -> bool:
        # https://stackoverflow.com/a/11264379/1973860
        try:
            host_bytes = address.split('.')
            valid = [int(b) for b in host_bytes]
            valid = [b for b in valid if b >= 0 and b <= 255]
            return len(host_bytes) == 4 and len(valid) == 4
        except Exception:
            return False

    @staticmethod
    def is_valid_ipv6(address: str) -> bool:
        # https://codereview.stackexchange.com/a/192732
        try:
            _ = ipaddress.IPv6Address(address)
            return True
        except ipaddress.AddressValueError:
            return False

    @staticmethod
    def _call(endpoint: str) -> str:
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.text
        else:
            raise RuntimeError(
                f"{endpoint} answered with an error -> " +
                f"{response.status_code}: {response.reason}"
            )

    @staticmethod
    def get_external_ipv4(logger: logging = None) -> str:
        address = None
        for name, url in EXTERNAL_SERVICE_IPv4.items():
            try:
                if logger is not None:
                    logger.debug(f"Getting external IP from {name}")
                address = Network._call(endpoint=url)
                break
            except RuntimeError as e:
                if logger is not None:
                    logger.warning(str(e))
                continue

        if Network.is_valid_ipv4(address=address):
            if logger is not None:
                logger.debug(f"External IP: {address}")
            return address
        else:
            if logger is not None:
                logger.error("The content from the external service is not a valid IPv4")

    @staticmethod
    def get_external_ipv6(logger: logging = None) -> str:
        address = None
        for name, url in EXTERNAL_SERVICE_IPv6.items():
            try:
                if logger is not None:
                    logger.debug(f"Getting external IP from {name}")
                address = Network._call(endpoint=url)
                break
            except RuntimeError as e:
                if logger is not None:
                    logger.warning(str(e))
                continue

        if Network.is_valid_ipv6(address=address):
            if logger is not None:
                logger.debug(f"External IP: {address}")
            return address
        else:
            if logger is not None:
                logger.error("The content from the external service is not a valid IPv6")
