import json
from unittest.mock import Mock

from vgscli.testing import CliRunnerTestCase, patch

get_organizations_response = json.loads(
    open("tests/organizations-list-response.json").read()
)
get_organizations_cmd_output = open("tests/get_organizations_cmd_output.yaml").read()


class GetOrganizationsTestCase(CliRunnerTestCase):
    @patch("vgscli.cli.commands.get.create_account_mgmt_api")
    def test_list_organizations(self, create_account_mgmt_api: Mock) -> None:
        get_service_accounts = create_account_mgmt_api().organizations.list
        get_service_accounts().body = get_organizations_response

        result = self.invoke(["get", "organizations"])

        self.assertOutput(result, get_organizations_cmd_output)
        self.assertExitCode(result, 0)
