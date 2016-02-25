from unittest import TestCase

from flake8.engine import get_style_guide

from app import settings
from tests.io import capture_stdout


class Flake8ConformanceTestCase(TestCase):
    def test_flake8_conformance(self):
        with capture_stdout() as captor:
            flake8_style = get_style_guide(paths=[settings.BASE_DIR])
            report = flake8_style.check_files()
        if report.total_errors > 0:
            self.fail(
                'Got some flake8 errors:\n{0}'.format(captor['value']),
            )
