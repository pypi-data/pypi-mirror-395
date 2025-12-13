import unittest
from unittest.mock import patch, MagicMock

from click.testing import CliRunner
from vgscli.click_extensions import Config
from vgs.sdk.serializers import dump_yaml, dump_json
from vgscli.vgs import operations_logs


@patch("vgscli.vgs.handshake")
@patch("vgscli.vgs.token_util.get_access_token")
@patch("vgscli.vgs.create_audits_api")
@patch("vgscli.vgs.fetch_operations_logs")
class OperationsLogsOutputTestCase(unittest.TestCase):
    def test_operations_logs_json_output_ok(self, mock_fetch_operations_logs, *args):
        # Arrange
        mock_fetch_operations_logs.return_value = {"test_key": "test_value"}
        params = [
            "--vault",
            "tntbnqdfizv",
            "--request",
            "3f2ab1258a87bc03f18d41a71cf317ee",
            "-o",
            "json",
        ]
        expected_output = (
            dump_json({"version": 1, "data": {"test_key": "test_value"}}) + "\n"
        )

        # Act
        runner = CliRunner()
        result = runner.invoke(operations_logs, params, obj=Config(False, "production"))

        # Assert
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            expected_output,
            result.output,
            f"Unexpected console output format.\n Expected: {expected_output}\nActual:{result.output}",
        )

    def test_operations_default_yaml_output_ok(self, fetch_operations_logs, *args):
        # Arrange
        fetch_operations_logs.return_value = {"test_key": "test_value"}
        params = [
            "--vault",
            "tntbnqdfizv",
            "--request",
            "3f2ab1258a87bc03f18d41a71cf317ee",
        ]
        expected_output = (
            dump_yaml({"version": 1, "data": {"test_key": "test_value"}}) + "\n"
        )

        # Act
        runner = CliRunner()
        result = runner.invoke(operations_logs, params, obj=Config(False, "production"))

        # Assert
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            expected_output,
            result.output,
            f"Unexpected console output format.\n Expected: {expected_output}\nActual:{result.output}",
        )

    def test_operations_yaml_output_ok(self, fetch_operations_logs, *args):
        # Arrange
        fetch_operations_logs.return_value = {"test_key": "test_value"}
        params = [
            "--vault",
            "tntbnqdfizv",
            "--request",
            "3f2ab1258a87bc03f18d41a71cf317ee",
            "-o",
            "yaml",
        ]
        expected_output = (
            dump_yaml({"version": 1, "data": {"test_key": "test_value"}}) + "\n"
        )

        # Act
        runner = CliRunner()
        result = runner.invoke(operations_logs, params, obj=Config(False, "production"))

        # Assert
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            expected_output,
            result.output,
            f"Unexpected console output format.\n Expected: {expected_output}\nActual:{result.output}",
        )

    @patch("vgscli.vgs.OperationLogsQueryConfig", autospec=True)
    def test_operations_config_composition_with_request_ok(
        self, mock_config, fetch_operations_logs, *args
    ):
        # Arrange
        fetch_operations_logs.return_value = {"test_key": "test_value"}
        vault = "tntbnqdfizv"
        trace_id = "test_trace"
        params = ["--vault", vault, "--request", trace_id]

        # Act
        runner = CliRunner()
        result = runner.invoke(operations_logs, params, obj=Config(False, "production"))

        # Assert
        actual_vault = mock_config.call_args[0][0]
        actual_trace_id = mock_config.call_args[1]["trace_id"]
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(
            vault,
            actual_vault,
            f"Unexpected vault value in query config\n Expected: {vault}\nActual:{actual_vault}",
        )
        self.assertEqual(
            trace_id,
            actual_trace_id,
            f"Unexpected vault value in query config\n Expected: {trace_id}\nActual:{actual_trace_id}",
        )


if __name__ == "__main__":
    unittest.main()
