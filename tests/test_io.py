from unittest import TestCase

from tests.io import capture_stdout


class CaptureStdoutTestCase(TestCase):
    def test_stdout_capturing(self):
        with capture_stdout() as captor:
            print('oh hi')  # NOQA
        self.assertEqual(captor['value'], 'oh hi\n')
