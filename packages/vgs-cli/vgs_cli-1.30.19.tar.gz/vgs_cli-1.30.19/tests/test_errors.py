import unittest

from click.exceptions import Abort, Exit

from vgscli.errors import handle_errors


@handle_errors()
def raise_error(error):
    raise error


class HandleErrorsTestCase(unittest.TestCase):
    def test_abort(self):
        expected = Abort()

        with self.assertRaises(Abort) as actual:
            raise_error(expected)

        self.assertEqual(expected, actual.exception)

    def test_exit(self):
        expected = Exit(1)

        with self.assertRaises(Exit) as actual:
            raise_error(expected)

        self.assertEqual(expected, actual.exception)


if __name__ == "__main__":
    unittest.main()
