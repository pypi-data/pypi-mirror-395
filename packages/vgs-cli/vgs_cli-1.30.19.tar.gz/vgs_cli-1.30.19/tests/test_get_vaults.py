import json
from unittest.mock import Mock

from vgscli.testing import CliRunnerTestCase, patch

get_organizations_response = json.loads(open("tests/vaults-list-response.json").read())
get_service_accounts_cmd_output = open("tests/get_vaults_cmd_output.yaml").read()


class GetVaultsTestCase(CliRunnerTestCase):
    @patch("vgscli.cli.commands.get.create_account_mgmt_api")
    def test_list_vaults(self, create_account_mgmt_api: Mock) -> None:
        get_service_accounts = create_account_mgmt_api().vaults.list
        get_service_accounts().body = get_organizations_response

        result = self.invoke(["get", "vaults"])

        self.assertOutput(result, get_service_accounts_cmd_output)
        self.assertExitCode(result, 0)
