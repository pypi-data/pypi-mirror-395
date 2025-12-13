import yaml
from vgscli.testing import CliRunnerTestCase, patch

access_credentials_response = yaml.load(
    open("tests/fixtures/get-access-credentials-response.yaml"), Loader=yaml.FullLoader
)

class GetAccessCredentialsTestCase(CliRunnerTestCase):
    @patch("vgscli.cli.commands.get.create_vault_mgmt_api")
    @patch("vgscli.cli.commands.get.create_account_mgmt_api")
    @patch("vgscli.cli.commands.get.handshake")
    @patch("vgscli.cli.commands.get.token_util")
    def test_get_access_credentials(
        self, token_util, handshake, create_account_mgmt_api, create_vault_mgmt_api
    ):
        mock_account_mgmt = create_account_mgmt_api()
        mock_account_mgmt.vaults.get_by_id.return_value.body = {
            "data": [
                {
                    "links": {
                        "vault_management_api": "https://api.sandbox.verygoodsecurity.com"
                    }
                }
            ]
        }
        mock_vault_mgmt = create_vault_mgmt_api()
        mock_vault_mgmt.credentials.list.return_value.body = access_credentials_response

        result = self.invoke(["--debug", "get", "access-credentials", "--vault", "tntasd123"])

        expected = {
            "apiVersion": "1.0.0",
            "kind": "AccessCredentials",
            "data": access_credentials_response["data"]
        }

        self.assertExitCode(result, 0)
        self.assertEqual(yaml.safe_load(result.output), expected)
