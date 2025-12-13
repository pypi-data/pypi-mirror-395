import unittest

from spotcrates.cli import parse_cmdline, playlist_sets, CommandLookup


class ArgparseTestCase(unittest.TestCase):
    def test_no_command(self):
        with self.assertRaises(SystemExit) as cm:
            parse_cmdline([])

        self.assertEqual(cm.exception.code, 2)

    def test_command(self):
        args, result_code = parse_cmdline(["test-command"])
        self.assertEqual(0, result_code)
        self.assertEqual("test-command", args.command)
        self.assertFalse(args.randomize)

    def test_random_before(self):
        args, result_code = parse_cmdline(["-r", "test-command"])
        self.assertEqual(0, result_code)
        self.assertEqual("test-command", args.command)
        self.assertTrue(args.randomize)

    def test_random_after(self):
        args, result_code = parse_cmdline(["test-command", "-r"])
        self.assertEqual(0, result_code)
        self.assertEqual("test-command", args.command)
        self.assertTrue(args.randomize)

    def test_random_after_1arg(self):
        args, result_code = parse_cmdline(["test-command", "arg1", "-r"])
        self.assertEqual(0, result_code)
        self.assertEqual("test-command", args.command)
        self.assertTrue(args.randomize)
        self.assertSequenceEqual(["arg1"], args.arguments)

    def test_random_after_2args(self):
        args, result_code = parse_cmdline(["test-command", "arg1", "arg2", "-r"])
        self.assertEqual(0, result_code)
        self.assertEqual("test-command", args.command)
        self.assertTrue(args.randomize)
        self.assertSequenceEqual(["arg1", "arg2"], args.arguments)

    def test_random_after_3args(self):
        args, result_code = parse_cmdline(["test-command", "arg1", "arg2", "arg3", "-r"])
        self.assertEqual(0, result_code)
        self.assertEqual("test-command", args.command)
        self.assertTrue(args.randomize)
        self.assertSequenceEqual(["arg1", "arg2", "arg3"], args.arguments)

    def test_randomize_all_command(self):
        args, result_code = parse_cmdline(["randomize-all"])
        self.assertEqual(0, result_code)
        self.assertEqual("randomize-all", args.command)
        self.assertFalse(args.randomize)
        self.assertSequenceEqual([], args.arguments)

    def test_randomize_command_with_args(self):
        args, result_code = parse_cmdline(["randomize", "playlist1", "playlist2"])
        self.assertEqual(0, result_code)
        self.assertEqual("randomize", args.command)
        self.assertSequenceEqual(["playlist1", "playlist2"], args.arguments)


class CommandLookupTestCase(unittest.TestCase):
    def setUp(self):
        self.lookup = CommandLookup()

    def test_randomize(self):
        self.assertEqual("randomize", self.lookup.find("r"))

    def test_randomize_full(self):
        self.assertEqual("randomize", self.lookup.find("randomize"))

    def test_randomize_all_prefix(self):
        self.assertEqual("randomize-all", self.lookup.find("randomize-a"))

    def test_randomize_all_full(self):
        self.assertEqual("randomize-all", self.lookup.find("randomize-all"))

    def test_copy(self):
        self.assertEqual("copy", self.lookup.find("cop"))

    def test_commands(self):
        self.assertEqual("commands", self.lookup.find("com"))

    def test_daily(self):
        self.assertEqual("daily", self.lookup.find("d"))

    def test_init_config(self):
        self.assertEqual("init-config", self.lookup.find("i"))

    def test_list_playlists(self):
        self.assertEqual("list-playlists", self.lookup.find("l"))

    def test_subscriptions(self):
        self.assertEqual("subscriptions", self.lookup.find("s"))


# playlist_sets


def test_playlist_sets():
    assert playlist_sets("a,b,c") == ["a", "b", "c"]


def test_playlist_sets_pipes():
    assert playlist_sets("a|b|c") == ["a", "b", "c"]


def test_playlist_sets_pipes_and_commas():
    assert playlist_sets("a|b,c") == ["a", "b", "c"]


def test_playlist_sets_blank():
    assert playlist_sets("") == [""]


def test_playlist_sets_none():
    assert playlist_sets(None) == [""]
