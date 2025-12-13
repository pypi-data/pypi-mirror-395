from unittest.mock import Mock

import yaml
from vgscli.testing import CliRunnerTestCase, patch

list_routes_response = yaml.load(
    open("tests/fixtures/list-routes-response.yaml"), Loader=yaml.FullLoader
)
list_routes_output = open("tests/fixtures/list-routes-response-output.yaml").read()
list_routes_legacy_output = open(
    "tests/fixtures/list-routes-response-legacy-output.yaml"
).read()


class GetHttpRoutesTestCase(CliRunnerTestCase):
    @patch("vgscli.cli.commands.get.create_vault_mgmt_api_routes")
    @patch("vgscli.cli.commands.get.handshake")
    @patch("vgscli.cli.commands.get.token_util")
    def test_get(self, token_util, handshake, create_vault_mgmt_api):
        list_routes = create_vault_mgmt_api().routes.list
        list_routes().body = list_routes_response

        result = self.invoke(["--debug", "get", "http-routes", "--vault", "tntasd123"])
        self.maxDiff = None
        print(result.output)
        self.assertExitCode(result, 0)
        self.assertEqual(result.output.strip(), list_routes_output.strip())


class GetRoutesTestCase(CliRunnerTestCase):
    @patch("vgscli.cli.commands.get.create_vault_mgmt_api_routes")
    @patch("vgscli.cli.commands.get.handshake")
    @patch("vgscli.cli.commands.get.token_util")
    def test_get(self, token_util, handshake, create_vault_mgmt_api):
        list_routes = create_vault_mgmt_api().routes.list
        list_routes().body = list_routes_response

        result = self.invoke(["--debug", "get", "routes", "--vault", "tntasd123"])
        self.maxDiff = None
        print(result.output)
        self.assertExitCode(result, 0)
        self.assertEqual(result.output.strip(), list_routes_legacy_output.strip())
