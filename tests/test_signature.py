import os
from unittest import TestCase

from app.signatures import cert_chain_url_valid, signature_valid

BASE_DIR = os.path.dirname(__file__)

INVALID_URLS = [
    'http://s3.amazonaws.com/echo.api/echo-api-cert.pem',  # (invalid protocol)
    'https://notamazon.com/echo.api/echo-api-cert.pem',  # (invalid hostname)
    'https://s3.amazonaws.com/EcHo.aPi/echo-api-cert.pem',  # (invalid path)
    'https://s3.amazonaws.com/invalid.path/echo-api-cert.pem',  # (invalid path)
    'https://s3.amazonaws.com:563/echo.api/echo-api-cert.pem',  # (invalid port)
]

VALID_URLS = [
    'https://s3.amazonaws.com/echo.api/echo-api-cert.pem',
    'HTTPS://s3.amazonaws.com/echo.api/echo-api-cert.pem',
    'https://S3.amazonaws.com/echo.api/echo-api-cert.pem',
    'HTTPS://s3.amazonaws.COM/echo.api/echo-api-cert.pem',
    'https://s3.amazonaws.com:443/echo.api/echo-api-cert.pem',
    'https://s3.amazonaws.com/echo.api/../echo.api/echo-api-cert.pem',
    'https://s3.amazonaws.com/echo.api/lol/../echo-api-cert.pem',
]


class SignatureCertChainUrlValidationTestCase(TestCase):
    def test_invalid_urls_are_invalid(self):
        for url in INVALID_URLS:
            self.assertFalse(cert_chain_url_valid(url))

    def test_valid_urls_are_valid(self):
        for url in VALID_URLS:
            self.assertTrue(cert_chain_url_valid(url))


class SignatureValidationTestCase(TestCase):
    cert_file = os.path.join(BASE_DIR, 'data', 'echo-api-cert-3.pem')
    request_body_file = os.path.join(BASE_DIR, 'data', 'body.txt')
    signature_file = os.path.join(BASE_DIR, 'data', 'signature.txt')

    def test_cert_validation(self):
        with open(self.cert_file) as f:
            cert_text = f.read().strip()
        with open(self.request_body_file) as f:
            request_body = f.read().strip().encode('utf-8')
        with open(self.signature_file) as f:
            signature = f.read().strip()
        self.assertTrue(signature_valid(signature, cert_text, request_body))
