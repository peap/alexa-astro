import sys
from contextlib import contextmanager
from io import StringIO


@contextmanager
def capture_stdout():
    """
    Capture STDOUT. Captured data is available in the returned dictionary's
    "value" key.

    Example:
        class PrintingTestCase(TestCase):
            def test_printing(self):
                with capture_stdout() as captor:
                    print('oh hi')
                self.assertEqual(stdout['value'], 'oh hi\n')
    """
    old_stdout = sys.stdout
    captor = {'stdout': StringIO(), 'value': None}
    sys.stdout = captor['stdout']
    try:
        yield captor
    finally:
        captor['value'] = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = old_stdout
