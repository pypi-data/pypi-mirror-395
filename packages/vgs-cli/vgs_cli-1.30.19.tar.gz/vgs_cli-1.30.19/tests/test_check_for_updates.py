import unittest
from unittest.mock import Mock, patch

from vgscli.testing import CliRunnerTestCase


class CheckForUpdatesTestCase(CliRunnerTestCase):

    # noinspection PyUnusedLocal
    @patch("vgscli.vgs.auth.login")
    @patch("vgscli.vgs.check_for_updates")
    def test_login_checks_for_updates(self, check_for_updates: Mock, *args):
        self.invoke(["login"])
        check_for_updates.assert_called()


if __name__ == "__main__":
    unittest.main()
