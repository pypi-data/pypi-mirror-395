import json
from unittest.mock import Mock

from vgscli.testing import CliRunnerTestCase, patch

import yaml

generate_access_credentials_response = json.loads(
    open("tests/credentials-post-response.json").read()
)


class GenerateAccessCredentialsTestCase(CliRunnerTestCase):
    ENVIRONMENT = "SANDBOX"
    ORGANIZATION_ID = "AC6mGNNRecR7K5N7AjX5niz4"
    TENANT_ID = "tntbysbk3rg"

    @patch("vgscli.cli.commands.generate.create_vault_mgmt_api")
    @patch("vgscli.cli.commands.generate.create_account_mgmt_api")
    def test_generate_access_credentials(
        self,
        create_account_mgmt_api: Mock,
        create_vault_mgmt_api: Mock,
    ) -> None:
        get_by_id = create_account_mgmt_api().vaults.get_by_id
        get_by_id().body = {
            "data": [
                {
                    "type": "vaults",
                    "id": self.ORGANIZATION_ID,
                    "attributes": {
                        "identifier": self.TENANT_ID,
                        "environment": self.ENVIRONMENT,
                        "updated_at": "2020-06-05T11:28:50.477Z",
                        "name": "Test",
                        "created_at": "2020-06-05T11:28:50.477Z",
                    },
                    "relationships": {
                        "organization": {
                            "links": {
                                "self": "https://accounts.verygoodsecurity.io/vaults/VLTc2RDF2hYquyDMrqFESMafD/relationships/organization",
                                "related": "https://accounts.verygoodsecurity.io/vaults/VLTc2RDF2hYquyDMrqFESMafD/organization",
                            },
                            "data": {
                                "type": "organizations",
                                "id": "ACckkyWvZJwbPdWn1hmr1vHC",
                            },
                        }
                    },
                    "links": {
                        "self": "https://accounts.verygoodsecurity.io/vaults/VLTc2RDF2hYquyDMrqFESMafD",
                        "reverse_proxy": "https://tntzcynqtfv.sandbox.verygoodproxy.io",
                        "forward_proxy": "https://USERNAME:PASSWORD@tntzcynqtfv.sandbox.verygoodproxy.io:8080",
                        "vault_management_api": "https://api.verygoodsecurity.com",
                        "vault_api": "https://tntzcynqtfv.sandbox.verygoodvault.com",
                    },
                }
            ]
        }
        create_vault_mgmt_api().credentials.create().body = (
            generate_access_credentials_response
        )

        result = self.invoke(
            ["generate", "access-credentials", "--vault", self.TENANT_ID]
        )

        output = yaml.full_load(result.output)

        self.assertEqual("1.0.0", output["apiVersion"])
        self.assertEqual("AccessCredentials", output["kind"])
        self.assertEqual("USnwVaX2SZdaaTbKa8VHVGaG", output["data"]["id"])
        self.assertEqual("credentials", output["data"]["type"])

        self.assertEqual("USnwVaX2SZdaaTbKa8VHVGaG", output["data"]["attributes"]["id"])
        self.assertEqual(
            "USnwVaX2SZdaaTbKa8VHVGaG", output["data"]["attributes"]["key"]
        )
        self.assertEqual(
            "d5933456-d954-447f-8897-43706ecad127a",
            output["data"]["attributes"]["secret"],
        )
        self.assertEqual(True, output["data"]["attributes"]["active"])

        self.assertEqual(3, len(output))
        self.assertEqual(3, len(output["data"]))
        self.assertEqual(5, len(output["data"]["attributes"]))

    def test_generate_access_credentials_fails_on_missing_vault_id(self) -> None:
        expected_output = "Error: Option '--vault' requires an argument.\n"

        result = self.invoke(["generate", "access-credentials", "--vault"])

        self.assertExitCode(result, 2)
        self.assertOutput(result, expected_output)

    def test_generate_access_credentials_fails_on_missing_vault_argument(self) -> None:
        expected_output = (
            "Usage: cli generate access-credentials [OPTIONS]\n"
            "Try 'cli generate access-credentials --help' for help.\n\n"
            "Error: Missing option '--vault' / '-V'.\n"
        )

        result = self.invoke(["generate", "access-credentials"])

        self.assertExitCode(result, 2)
        self.assertOutput(result, expected_output)
