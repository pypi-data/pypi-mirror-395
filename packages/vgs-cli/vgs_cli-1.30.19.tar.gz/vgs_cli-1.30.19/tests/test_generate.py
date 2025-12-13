import io

import yaml
from vgscli.cli_utils import validate_multi_yaml
from vgscli.testing import CliRunnerTestCase


class GenerateVaultTestCase(CliRunnerTestCase):
    def test_generate(self):
        result = self.invoke(["generate", "vault"])

        self.assertExitCode(result, 0)

        output = yaml.full_load(result.output)

        self.assertEqual(3, len(output))
        self.assertEqual("1.0.0", output["apiVersion"])
        self.assertEqual("Vault", output["kind"])

        data = output["data"]

        self.assertEqual(3, len(data))
        self.assertEqual("Very Good Vault", data["name"])
        self.assertEqual("SANDBOX", data["environment"])
        self.assertEqual("AC6mGNNRecR7K5N7AjX5niz4", data["organizationId"])


class GenerateMFTRouteTestCase(CliRunnerTestCase):
    def test_generate(self):
        result = self.invoke(["--debug", "generate", "mft-route"])

        self.assertExitCode(result, 0)

        output = yaml.full_load(result.output)

        fp = io.StringIO()
        fp.write(result.output)

        validate_multi_yaml(output, "validation-schemas/vault-resources.yaml")

        self.assertEqual("mft.vgs.io/v1beta", output["apiVersion"])
        self.assertEqual("MftRoute", output["kind"])


class GenerateHttpRouteTestCase(CliRunnerTestCase):
    def test_generate(self):
        result = self.invoke(["generate", "http-route"])

        self.assertExitCode(result, 0)

        output = yaml.full_load(result.output)

        fp = io.StringIO()
        fp.write(result.output)

        validate_multi_yaml(output, "validation-schemas/vault-resources.yaml")

        self.assertEqual("vault.vgs.io/v1", output["apiVersion"])
        self.assertEqual("HttpRoute", output["kind"])
