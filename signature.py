"""
Check signatures of incoming requests, to ensure they come from Alexa.

See: https://developer.amazon.com/appsandservices/solutions/alexa/alexa-skills-kit/docs/developing-an-alexa-skill-as-a-web-service#verifying-the-signature-certificate-url
"""
from base64 import b64decode
from hashlib import sha1
from urllib.parse import urlparse

from url_normalize import url_normalize

CERTS = {}


def cert_chain_url_valid(url):
    """
    Ensure that the provided URL for the certificate chain is valid, by checking that:
    * it's HTTPS
    * the host is s3.amazonaws.com
    * the port, if specified, is 443
    * the path starts with '/echo.api/'
    """
    normalized = url_normalize(url)
    parsed = urlparse(normalized)
    url_checks = {
        'scheme': parsed.scheme == 'https',
        'hostname': parsed.hostname == 's3.amazonaws.com',
        'port': parsed.port in (443, None),
        'path': parsed.path.startswith('/echo.api/'),
    }
    all_checks_pass = all(url_checks.values())
    # TODO: log attributes of failing URLs
    return all_checks_pass


def signature_valid(signature, cert_chain_url, data):
    # check cert_chain_url
    if not cert_chain_url_valid(cert_chain_url):
        return False

    # get cert
    normalized_url = url_normalize(cert_chain_url)
    # ...

    # decode given hash
    given_hash = b64decode(signature)
    # TODO: decrypt with extracted public key
    expected_hash = sha1()
    expected_hash.update(data)
    expected_digest = expected_hash.digest()
    return True
    # return given_digest == expected_digest
