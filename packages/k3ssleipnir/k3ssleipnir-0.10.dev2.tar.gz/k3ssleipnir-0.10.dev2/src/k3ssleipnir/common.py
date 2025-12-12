import os
import ssl
import socket
import datetime as dt

from k3ssleipnir import logger


def check_if_credentials_is_a_file(credentials: str | None) -> bool:
    result = True
    try:
        if credentials is None:
            result = False
        elif os.path.exists(credentials) is True:
            with open(credentials, "r") as f:
                f.read(1)
            result = True
        else:
            result = False
    except:
        result = False
    logger.info("Supplied credentials is a file: {}".format(result))
    return result


class Dummy:
    def __init__(self, values: dict = {}) -> None:
        self.values = values

    def _generic_handler(self, method_name, *args, **kwargs):
        if method_name in self.values:
            return self.values[method_name]
        return None

    def __getattr__(self, name):
        # Called when an attribute (or method) is accessed that doesn't exist on the instance.
        return lambda *args, **kwargs: self._generic_handler(name, *args, **kwargs)


def verify_ssl_certificate(hostname: str, port: int = 443, timeout: int = 10) -> bool:
    validation_passed = False
    if "://" in hostname:
        hostname = hostname.split("://")[1].split("/")[0]
    if "/" in hostname:
        hostname = hostname.split("/")[0]
    if ":" in hostname:
        elements = hostname.split(":")
        hostname = elements[0]
        port = int(elements[1])
    try:
        context = ssl.create_default_context()
        sock = socket.create_connection((hostname, port), timeout=timeout)
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            der_cert = ssock.getpeercert(True)
            if der_cert is None:
                return False
            ssl.DER_cert_to_PEM_cert(der_cert)
            cert_details = ssock.getpeercert()
            not_before_str = cert_details.get("notBefore")
            not_after_str = cert_details.get("notAfter")
            date_format = "%b %d %H:%M:%S %Y GMT"
            not_after = dt.datetime.strptime(not_after_str, date_format)

            logger.info(" Success: Retrieved certificate for {}".format(hostname))
            logger.debug(
                "   [{}] Subject: {}".format(hostname, cert_details.get("subject"))
            )
            logger.debug(
                "   [{}] Issuer: {}".format(hostname, cert_details.get("issuer"))
            )
            logger.debug("   [{}] Valid From: {}".format(hostname, not_before_str))
            logger.debug("   [{}] Valid Until: {}".format(hostname, not_after_str))

            # Simple validity check
            if dt.datetime.now() > not_after:
                logger.error("Certificate has EXPIRED!")
            else:
                validation_passed = True

    except socket.timeout:
        logger.error("Connection to {} timed out.".format(hostname))
        validation_passed = False
    except ConnectionRefusedError:
        logger.error("Connection to {}:{} refused.".format(hostname, port))
        validation_passed = False
    except ssl.SSLError as e:
        logger.error("SSL/TLS Error during handshake: {}".format(e))
        validation_passed = False
    except Exception as e:
        logger.error("An unexpected error occurred: {}".format(e))
        validation_passed = False
    return validation_passed
