from unittest.mock import MagicMock

import yaml
from vgscli.testing import CliRunnerTestCase, patch


class ApplyVaultResourcesTestCase(CliRunnerTestCase):

    TENANT_ID = "tntbysbk3rg"

    @patch("vgscli.cli.commands.apply.create_vaults_api")
    @patch("vgscli.cli.commands.apply.handshake")
    @patch("vgscli.cli.commands.apply.token_util")
    def test_apply_multiple_vault_resources(
        self, token_util, handshake, create_vaults_api
    ):
        expected_output = "mft.vgs.io/v1beta"

        with open("./tests/fixtures/route-response.yaml") as file:
            # we stored as yaml but api returns json
            jsonified_route_response = yaml.load(file, Loader=yaml.FullLoader)
            create_vaults_api.return_value.routes.update.return_value = MagicMock(
                body=jsonified_route_response
            )

        with open("./tests/fixtures/vault-resources.yaml") as file:
            result = self.invoke(
                [
                    "--debug",
                    "apply",
                    "vault-resources",
                    "-V",
                    self.TENANT_ID,
                    "-f",
                    file.name,
                ]
            )

        print(result.output)
        self.assertOutputContains(result, expected_output)
        self.assertExitCode(result, 0)

        handshake.assert_called()
        # token_util.assert_called()
        create_vaults_api.assert_called()
        create_vaults_api.return_value.routes.update.assert_called()

        assert (
            create_vaults_api.return_value.routes.update.call_args.args[0]
            == "7478d3b7-beef-cafe-97e6-347f8d8c28b0"
        )
        assert (
            "destination_override_endpoint"
            in create_vaults_api.return_value.routes.update.call_args.kwargs["body"][
                "data"
            ]["attributes"]
        )

    def test_invalid_type(self):
        invalid_resources_and_errors = [
            ("vault-resources-invalid-sftp-route.yaml", "Failed to validate vault.vgs.io/v1beta SftpRoute my-sftp-route"),
            ("vault-resources-invalid-mft-cluster.yaml", "Failed to validate mft.vgs.io/v1beta MftCluster"),
            # ("vault-resources-invalid-mft-route.yaml", "Failed to validate mft.vgs.io/v1beta MftRoute"),
            ("vault-resources-invalid-mft-sla.yaml", "Failed to validate mft.vgs.io/v1beta MftSla"),
        ]
        for resource, expected_output in invalid_resources_and_errors:
            with open(f"./tests/fixtures/{resource}") as file:
                result = self.invoke(
                    ["apply", "vault-resources", "-V", self.TENANT_ID, "-f", file.name]
                )

            self.assertExitCode(result, 2)
            self.assertOutputContains(result, expected_output)
