import unittest
from pathlib import Path
from unittest import mock

from click.testing import CliRunner
from parameterized import parameterized

from vgscli.vgs import cli


class ConfigFileTestCase(unittest.TestCase):
    EXPECTED_IDP = "okta"

    # noinspection PyPep8Naming
    # noinspection PyUnusedLocal
    @mock.patch("vgscli.vgs.check_for_updates")
    @mock.patch("vgscli.vgs.auth.login")
    @mock.patch("vgscli.config_file.configobj.ConfigObj")
    def test_default_config_file(self, ConfigObj, login, *args):
        ConfigObj.return_value = {"login": {"idp": self.EXPECTED_IDP}}

        result = CliRunner().invoke(cli, ["login"])
        self.assertEqual(0, result.exit_code)

        config = Path.home().joinpath(".vgs", "config").__str__()
        self.assertEqual(config, ConfigObj.call_args.args[0])

        self.assertEqual(self.EXPECTED_IDP, login.call_args.kwargs["idp"])

    # noinspection PyUnusedLocal
    @parameterized.expand(
        [
            ["./tests/test_config", EXPECTED_IDP],
            ["./tests/ExJG7k8EtkU", None],
        ]
    )
    @mock.patch("vgscli.vgs.check_for_updates")
    @mock.patch("vgscli.vgs.auth.login")
    def test_config_option(self, config, idp, login, *args):
        result = CliRunner().invoke(cli, ["login", "--config", config])
        self.assertEqual(0, result.exit_code)
        self.assertEqual(idp, login.call_args.kwargs["idp"])


if __name__ == "__main__":
    unittest.main()
