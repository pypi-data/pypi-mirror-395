import json
from unittest.mock import Mock

from vgscli.testing import CliRunnerTestCase, patch

import yaml

get_access_credentials_response = json.loads(
    open("tests/credentials-list-response.json").read()
)


class GetAccessCredentialsTestCase(CliRunnerTestCase):
    ENVIRONMENT = "SANDBOX"
    ORGANIZATION_ID = "AC6mGNNRecR7K5N7AjX5niz4"
    TENANT_ID = "tntbysbk3rg"

    @patch("vgscli.cli.commands.get.create_vault_mgmt_api")
    @patch("vgscli.cli.commands.get.create_account_mgmt_api")
    def test_get_access_credentials(
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
        create_vault_mgmt_api().credentials.list().body = (
            get_access_credentials_response
        )

        result = self.invoke(["get", "access-credentials", "--vault", self.TENANT_ID])

        output = yaml.full_load(result.output)

        self.assertEqual("1.0.0", output["apiVersion"])
        self.assertEqual("AccessCredentials", output["kind"])

        self.assertEqual("US4UA9WyixEWggURgvNiogc1", output["data"][0]["id"])
        self.assertEqual("credentials", output["data"][0]["type"])
        self.assertEqual(None, output["data"][0]["attributes"]["access"])
        self.assertEqual(True, output["data"][0]["attributes"]["active"])
        self.assertEqual(
            "US4UA9WyixEWggURgvNiogc1", output["data"][0]["attributes"]["id"]
        )

        self.assertEqual("USs29XfjPAtMQn3nikcBMuqF", output["data"][1]["id"])
        self.assertEqual("credentials", output["data"][1]["type"])
        self.assertEqual(None, output["data"][1]["attributes"]["access"])
        self.assertEqual(True, output["data"][1]["attributes"]["active"])
        self.assertEqual(
            "USs29XfjPAtMQn3nikcBMuqF", output["data"][1]["attributes"]["id"]
        )

        self.assertEqual(3, len(output))
        self.assertEqual(2, len(output["data"]))
        self.assertEqual(5, len(output["data"][0]["attributes"]))
