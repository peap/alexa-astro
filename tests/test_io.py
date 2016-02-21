from unittest import TestCase

from tests.io import CaptureStdout


class CaptureStdoutTestCase(TestCase):
    def test_stdout_capturing(self):
        with CaptureStdout() as stdout:
            print('oh hi')  # NOQA
        self.assertEqual(str(stdout), 'oh hi\n')
