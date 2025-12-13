from tempfile import NamedTemporaryFile
from textwrap import dedent
from unittest.mock import Mock

from vgscli.testing import CliRunnerTestCase, patch


class ApplyServiceAccountTestCase(CliRunnerTestCase):
    @patch("vgscli.cli.commands.apply.create_account_mgmt_api")
    def test_apply_service_accounts_with_annotations(
        self, create_account_mgmt_api: Mock
    ) -> None:
        create_service_account = create_account_mgmt_api().service_accounts.create
        create_service_account().body = {
            "data": {
                "attributes": {
                    "client_id": "ACtTmnC6Vo-vgs-cli-5S6x8",
                    "client_secret": "cc91674d-eb8b-42e3-a428-5bdd93641d33",
                }
            }
        }

        with NamedTemporaryFile("w") as file:
            file.write(
                dedent(
                    """
                apiVersion: 1.0.0
                kind: ServiceAccount
                data:
                  annotations:
                    "vgs.io/vault-id": "tnthlp1rehx"
                  name: route-reader
                  scopes:
                    - name: routes:read
            """
                )
            )
            file.flush()

            result = self.invoke(
                [
                    "apply",
                    "service-account",
                    "-O",
                    "AC6mGNNRecR7K5N7AjX5niz4",
                    "-f",
                    file.name,
                ]
            )
            self.assertExitCode(result, 0)

        payload = create_service_account.call_args.kwargs["body"]

        expected_annotations = {"vgs.io/vault-id": "tnthlp1rehx"}
        self.assertEqual(
            expected_annotations, payload["data"]["attributes"]["annotations"]
        )
