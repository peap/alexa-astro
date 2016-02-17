from unittest import TestCase

from signature import cert_chain_url_valid

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
