import unittest
from tempfile import NamedTemporaryFile
from textwrap import dedent
from unittest.mock import Mock

import yaml
from vgscli.testing import CliRunnerTestCase, patch


class ApplyVaultTestCase(CliRunnerTestCase):
    NAME = "Very Good Vault"
    ENVIRONMENT = "SANDBOX"
    ORGANIZATION_ID = "AC6mGNNRecR7K5N7AjX5niz4"

    USERNAME = "US8LFTG62bfyGBVR9377rmFD"
    PASSWORD = "6e820e34-3653-4f90-b5a1-2ea5b720af07"

    TENANT_ID = "tntbysbk3rg"

    def test_apply_vault_fails_on_ambiguous_organization_id(self) -> None:
        expected_output = (
            f"Ambiguous organization ID. "
            f"Run the command with '--organization={self.ORGANIZATION_ID}' to resolve.\n"
        )

        with NamedTemporaryFile("w") as file:
            file.write(
                dedent(
                    f"""
                apiVersion: 1.0.0
                kind: Vault
                data:
                  name: {self.NAME}
                  environment: {self.ENVIRONMENT}
                  organizationId: {self.ORGANIZATION_ID}
            """
                )
            )
            file.flush()

            result = self.invoke(
                ["apply", "vault", "-O", "ACq9AiipVS8rnhvQgMZ9Jjr9", "-f", file.name]
            )

            self.assertExitCode(result, 2)
            self.assertOutput(result, expected_output)

    def test_apply_vault_fails_on_missing_organization_id(self) -> None:
        expected_output = (
            "Missing organization ID. Pass the '--organization' option to resolve.\n"
        )

        with NamedTemporaryFile("w") as file:
            file.write(
                dedent(
                    f"""
                apiVersion: 1.0.0
                kind: Vault
                data:
                  name: {self.NAME}
                  environment: {self.ENVIRONMENT}
            """
                )
            )
            file.flush()

            result = self.invoke(["apply", "vault", "-f", file.name])

            self.assertExitCode(result, 2)
            self.assertOutput(result, expected_output)

    @patch("vgscli.cli.commands.apply.create_vault_mgmt_api")
    @patch("vgscli.cli.commands.apply.create_account_mgmt_api")
    def test_apply_vault_uses_organization_id_from_file(
        self,
        create_account_mgmt_api: Mock,
        create_vault_mgmt_api: Mock,
    ) -> None:
        create_or_update = create_account_mgmt_api().vaults.create_or_update

        create_or_update().body = {
            "data": {
                "attributes": {  # Return relevant attributes only
                    "credentials": {"key": self.USERNAME, "secret": self.PASSWORD},
                    "identifier": self.TENANT_ID,
                },
                "links": {"vault_management_api": "https://api.verygoodsecurity.io"},
            }
        }

        create_vault_mgmt_api().vaults.retrieve().body = {
            "data": {"attributes": {"state": "PROVISIONED"}}
        }

        with NamedTemporaryFile("w") as file:
            file.write(
                dedent(
                    f"""
                apiVersion: 1.0.0
                kind: Vault
                data:
                  name: {self.NAME}
                  environment: {self.ENVIRONMENT}
                  organizationId: {self.ORGANIZATION_ID}
            """
                )
            )
            file.flush()

            self.invoke(["apply", "vault", "-f", file.name])

        create_or_update.assert_called_with(
            body={
                "data": {
                    "attributes": {"name": self.NAME, "environment": self.ENVIRONMENT},
                    "type": "vaults",
                    "relationships": {
                        "organization": {
                            "data": {
                                "type": "organizations",
                                "id": self.ORGANIZATION_ID,
                            }
                        }
                    },
                }
            }
        )

    @patch("vgscli.cli.commands.apply.create_vault_mgmt_api")
    @patch("vgscli.cli.commands.apply.create_account_mgmt_api")
    def test_apply_vault_uses_organization_id_from_option(
        self,
        create_account_mgmt_api: Mock,
        create_vault_mgmt_api: Mock,
    ) -> None:
        create_or_update = create_account_mgmt_api().vaults.create_or_update

        create_or_update().body = {
            "data": {
                "attributes": {  # Return relevant attributes only
                    "credentials": {"key": self.USERNAME, "secret": self.PASSWORD},
                    "identifier": self.TENANT_ID,
                },
                "links": {"vault_management_api": "https://api.verygoodsecurity.io"},
            }
        }
        create_vault_mgmt_api().vaults.retrieve().body = {
            "data": {"attributes": {"state": "PROVISIONED"}}
        }

        with NamedTemporaryFile("w") as file:
            file.write(
                dedent(
                    f"""
                apiVersion: 1.0.0
                kind: Vault
                data:
                  name: {self.NAME}
                  environment: {self.ENVIRONMENT}
            """
                )
            )
            file.flush()

            self.invoke(["apply", "vault", "-O", self.ORGANIZATION_ID, "-f", file.name])

        create_or_update.assert_called_with(
            body={
                "data": {
                    "attributes": {"name": self.NAME, "environment": self.ENVIRONMENT},
                    "type": "vaults",
                    "relationships": {
                        "organization": {
                            "data": {
                                "type": "organizations",
                                "id": self.ORGANIZATION_ID,
                            }
                        }
                    },
                }
            }
        )

    # noinspection PyUnusedLocal
    @patch("time.sleep", return_value=None)
    @patch("vgscli.cli.commands.apply.create_vault_mgmt_api")
    @patch("vgscli.cli.commands.apply.create_account_mgmt_api")
    def test_apply_vault_waits_for_provisioning(
        self,
        create_account_mgmt_api: Mock,
        create_vault_mgmt_api: Mock,
        *args,  # Unused mocks
    ) -> None:
        create_account_mgmt_api().vaults.create_or_update().body = {
            "data": {
                "attributes": {  # Return relevant attributes only
                    "credentials": {"key": self.USERNAME, "secret": self.PASSWORD},
                    "identifier": self.TENANT_ID,
                },
                "links": {"vault_management_api": "https://api.verygoodsecurity.io"},
            }
        }

        retrieve = create_vault_mgmt_api().vaults.retrieve

        retrieve.side_effect = [
            Mock(body={"data": {"attributes": {"state": "PROVISIONING"}}}),
            Mock(body={"data": {"attributes": {"state": "PROVISIONING"}}}),
            Mock(body={"data": {"attributes": {"state": "PROVISIONED"}}}),
        ]

        with NamedTemporaryFile("w") as file:
            file.write(
                dedent(
                    f"""
                apiVersion: 1.0.0
                kind: Vault
                data:
                  name: {self.NAME}
                  environment: {self.ENVIRONMENT}
                  organizationId: {self.ORGANIZATION_ID}
            """
                )
            )
            file.flush()

            self.invoke(["apply", "vault", "-f", file.name])

        retrieve.assert_called_with(
            self.TENANT_ID, headers={"VGS-Tenant": self.TENANT_ID}
        )
        self.assertEqual(3, retrieve.call_count)

    @patch("vgscli.cli.commands.apply.create_vault_mgmt_api")
    @patch("vgscli.cli.commands.apply.create_account_mgmt_api")
    def test_apply_vault_formats_output(
        self, create_account_mgmt_api: Mock, create_vault_mgmt_api: Mock
    ) -> None:
        create_or_update = create_account_mgmt_api().vaults.create_or_update

        create_or_update().body = {
            "data": {
                "attributes": {  # Return relevant attributes only
                    "credentials": {"key": self.USERNAME, "secret": self.PASSWORD},
                    "identifier": self.TENANT_ID,
                },
                "links": {"vault_management_api": "https://api.verygoodsecurity.io"},
            }
        }

        create_vault_mgmt_api().vaults.retrieve().body = {
            "data": {"attributes": {"state": "PROVISIONED"}}
        }

        with NamedTemporaryFile("w") as file:
            file.write(
                dedent(
                    f"""
                apiVersion: 1.0.0
                kind: Vault
                data:
                  name: {self.NAME}
                  environment: {self.ENVIRONMENT}
                  organizationId: {self.ORGANIZATION_ID}
            """
                )
            )
            file.flush()

            result = self.invoke(["apply", "vault", "-f", file.name])

            self.assertExitCode(result, 0)

            output = yaml.full_load(result.output)

            self.assertEqual("1.0.0", output["apiVersion"])
            self.assertEqual("Vault", output["kind"])

            self.assertEqual(self.TENANT_ID, output["data"]["id"])

            self.assertEqual(self.USERNAME, output["data"]["credentials"]["username"])
            self.assertEqual(self.PASSWORD, output["data"]["credentials"]["password"])

            self.assertEqual(self.NAME, output["data"]["name"])
            self.assertEqual(self.ENVIRONMENT, output["data"]["environment"])
            self.assertEqual(self.ORGANIZATION_ID, output["data"]["organizationId"])

            self.assertEqual(3, len(output))
            self.assertEqual(5, len(output["data"]))
            self.assertEqual(2, len(output["data"]["credentials"]))


if __name__ == "__main__":
    unittest.main()
