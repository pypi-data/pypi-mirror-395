import json
from unittest.mock import Mock

from vgscli.testing import CliRunnerTestCase, patch

get_service_accounts_response = json.loads(
    open("tests/get_service_accounts_response.json").read()
)
get_service_accounts_cmd_output = open(
    "tests/get_service_accounts_cmd_output.yaml"
).read()


class GetServiceAccountsTestCase(CliRunnerTestCase):
    @patch("vgscli.cli.commands.get.create_account_mgmt_api")
    def test_get_service_accounts(self, create_account_mgmt_api: Mock) -> None:
        get_service_accounts = create_account_mgmt_api().service_accounts.get
        get_service_accounts().body = get_service_accounts_response
        org_id = "ACsL3CLHYm8pvrXTD6kEME45"

        result = self.invoke(["get", "service-accounts", "-O", org_id])

        self.assertOutput(result, get_service_accounts_cmd_output)
        self.assertExitCode(result, 0)

        call_args = get_service_accounts.call_args
        self.assertEqual(org_id, call_args[0][0])
