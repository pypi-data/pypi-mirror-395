import unittest

from simple_rest_client.api import API

from vgscli.click_extensions import Config
from vgscli.audits_api import create_api, OperationLogsQueryConfig


class Context:
    def __init__(self, cfg):
        self.obj = cfg


class OperationsApiTestCase(unittest.TestCase):
    def test_create_operations_audit_api(self):
        # Arrange
        operations_logs_list_action_resource = "op-pipeline-logs"
        ctx = Context(Config(True, "prod"))
        vault = "tntbnqdfizv"
        token = "test_token"

        # Act
        api: API = create_api(ctx, vault, ctx.obj.env, token)

        # Assert
        self.assertTrue(
            hasattr(api, "operations_logs"),
            'API object MUST contain "operations_logs" attribute',
        )
        self.assertTrue(
            api.operations_logs.actions.get("list"),
            '"operations_logs" API attribute MUST support "list" action',
        )
        self.assertEqual(
            api.operations_logs.actions.get("list").get("url"),
            operations_logs_list_action_resource,
            f"Incorrect operations_logs list action URL.\n"
            f"Expected:{operations_logs_list_action_resource}"
            f'Actual:{api.operations_logs.actions.get("list").get("url")}',
        )


class OperationLogsQueryConfigTestCase(unittest.TestCase):
    def test_operation_logs_query_config_with_defaults_to_query_params_ok(self):
        # Arrange
        vault = "tntbnqdfizv"
        trace_id = "trace_id"
        expected_query_params = {
            "filter[tenant_id]": vault,
            "filter[trace_id]": trace_id,
            "page[size]": 1000,
        }

        # Act
        oplqc = OperationLogsQueryConfig(vault, trace_id)

        # Assert
        self.assertDictEqual(
            expected_query_params,
            oplqc.to_query_params(),
            f"Incorrect query params\n"
            f"Actual: {oplqc.to_query_params()}"
            f"Expected: {expected_query_params}\n",
        )

    def test_operation_logs_query_config_no_defaults_to_query_params_ok(self):
        # Arrange
        vault = "tntbnqdfizv"
        page_size = 100
        trace_id = "trace_id"
        expected_query_params = {
            "filter[tenant_id]": vault,
            "page[size]": page_size,
            "filter[trace_id]": trace_id,
        }

        # Act
        oplqc = OperationLogsQueryConfig(vault, trace_id, page_size)

        # Assert
        self.assertDictEqual(
            expected_query_params,
            oplqc.to_query_params(),
            f"Incorrect query params\n"
            f"Actual: {oplqc.to_query_params()}"
            f"Expected: {expected_query_params}\n",
        )
