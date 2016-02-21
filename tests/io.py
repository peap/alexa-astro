import sys
from io import StringIO


class CaptureStdout():
    """
    Capture STDOUT as self.value when used as a context manager.

    Example:
        class PrintingTestCase(TestCase):
            def test_printing(self):
                with CaptureStdout() as stdout:
                    print('oh hi')
                self.assertEqual(str(stdout), 'oh hi\n')
    """

    def __init__(self):
        self.value = ''
        self.old_stdout = None

    def __str__(self):
        return self.value

    def __enter__(self):
        self.old_stdout = sys.stdout
        sys.stdout = StringIO()
        return self

    def __exit__(self, *exc_info):
        self.value = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = self.old_stdout
