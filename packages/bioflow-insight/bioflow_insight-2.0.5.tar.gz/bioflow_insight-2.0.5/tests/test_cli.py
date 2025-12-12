import pathlib
import unittest
from tempfile import TemporaryDirectory

from bioflow_insight_cli.main import cli


class TestCall(unittest.TestCase):
    def test_cli_works(self):
        cli("./wf_test/main.nf", render_graphs=False)
        cli("./wf_test/main.nf", render_graphs=True)

    def test_cli_output_considered(self):
        with TemporaryDirectory() as my_temp_dir:
            my_results = pathlib.Path(my_temp_dir) / "my_results"
            self.assertFalse(my_results.exists())
            cli("./wf_test/main.nf", render_graphs=False, output_dir=str(my_results))
            self.assertTrue(my_results.exists(), "Results should be there, output_dir not taken into account")

    def test_with_illegal_path_char_in_name(self):
        with TemporaryDirectory() as my_temp_dir:
            my_results = pathlib.Path(my_temp_dir) / "my_results"
            cli(
                "./wf_test/main.nf",
                render_graphs=False,
                output_dir=str(my_results),
                name="https://github.com/blabla/toto:qsd!qsd%#sqdqsd"
            )


