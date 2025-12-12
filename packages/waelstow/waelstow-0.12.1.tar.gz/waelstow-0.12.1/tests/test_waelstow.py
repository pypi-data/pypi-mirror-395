import os, shutil, tempfile, sys
from unittest import TestCase

from waelstow import (list_tests, discover_tests, capture_stdout,
    capture_stderr, replaced_directory, pprint, noted_raise)

# =============================================================================

class WaelstowTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extras = os.path.join(os.path.dirname(os.path.dirname(__file__)),
            'extras')

        cls.good_dir = os.path.abspath(os.path.join(cls.extras, 'good_tests'))

        cls.good_cases = {
            'a1' :'tests_a.A1TestCase.test_method_a1',
            'a1c':'tests_a.A1TestCase.test_method_common',
            'a2' :'tests_a.A2TestCase.test_method_a2',
            'a2c':'tests_a.A2TestCase.test_method_common',
            'b'  :'tests_b.BTestCase.test_method_b',
            'bc' :'tests_b.BTestCase.test_method_common',
            'cc' :'tests_c.CTestCase.test_method_common',
        }

    # -----------------------------------------------------------
    # Test Case Discovery

    def assert_test_strings(self, case, keys, tests):
        values = [case[key] for key in keys]
        names = [test.id() for test in tests]
        self.assertEqual(set(values), set(names))

    def test_list_tests(self):
        suite = discover_tests(self.good_dir)
        tests = list(list_tests(suite))
        self.assert_test_strings(self.good_cases, self.good_cases.keys(), tests)

    def _check_shortcuts(self, expected, labels):
        suite = discover_tests(self.good_dir, labels=labels)
        tests = list_tests(suite)
        self.assert_test_strings(self.good_cases, expected, tests)

    def test_shortcuts(self):
        # -- find all
        self._check_shortcuts(['a1', 'a1c', 'a2', 'a2c', 'b', 'bc', 'cc'], [])

        # -- test shortcuts
        labels = ['=common', ]
        self._check_shortcuts(['a1c', 'a2c', 'bc', 'cc'], labels)

        labels = ['=method_a', ':method_b']
        self._check_shortcuts(['a1', 'a2', 'b',], labels)

        labels = ['=A1Test']
        self._check_shortcuts(['a1', 'a1c', ], labels)

        # -- test full labels
        labels = [
            'tests_a.A1TestCase.test_method_a1',
            'tests_b.BTestCase.test_method_b',
        ]
        self._check_shortcuts(['a1', 'b', ], labels)

        # -- test mix
        labels = ['=A1TestCase', 'tests_b.BTestCase.test_method_b', ]
        self._check_shortcuts(['a1','a1c', 'b', ], labels)

    def test_discover_pattern(self):
        # check the use of a non-default file name containing test cases
        suite = discover_tests(self.good_dir, [], 'others.py')
        tests = list(list_tests(suite))
        self.assertEqual(1, len(tests))
        self.assertEqual('others.OtherTestCase.test_method_common',
            tests[0].id())

    def test_bad_file(self):
        # check that discovered tests that don't compile are found properly
        # (they used to be ignored)
        bad_dir = os.path.abspath(os.path.join(self.extras, 'bad_tests'))
        suite = discover_tests(bad_dir, [])

        expected = [
            'tests_d.DTestCase.test_method_common',
            'unittest.loader._FailedTest.tests_f',
        ]

        expected = set(expected)

        tests = set([test.id() for test in list_tests(suite)])
        self.assertEqual(expected, tests)

        # Do it again with the shortcut finder, failed test should still be
        # found so it throws an exception when run
        suite = discover_tests(bad_dir, ["=foo"])
        expected = set([
            'unittest.loader._FailedTest.tests_f',
        ])

        tests = set([test.id() for test in list_tests(suite)])
        self.assertEqual(expected, tests)

    # -----------------------------------------------------------
    # Test Utilities

    def test_replace_dir(self):
        # create a temp directory and put something in it which is to be
        # replaced
        test_dir = tempfile.mkdtemp()
        orig_file = os.path.join(test_dir, 'a.txt')
        replace_file = os.path.join(test_dir, 'b.txt')

        with open(orig_file, 'w') as f:
            f.write('foo')

        # test not a dir handling
        with self.assertRaises(AttributeError):
            # call context manager by hand as putting it in a "with" will
            # result in unreachable code which blows our testing coverage
            rd = replaced_directory(orig_file)
            rd.__enter__()

        # replace_directory should handle trailing slashes
        test_dir += '/'

        created_td = ''
        with replaced_directory(test_dir) as td:
            created_td = td

            # put something in the replaced directory
            with open(replace_file, 'w') as f:
                f.write('bar')

            # original should be moved out of path, replaced should exist
            self.assertFalse(os.path.exists(orig_file))
            self.assertTrue(os.path.exists(replace_file))

        # original should be back, replaced should be gone
        self.assertTrue(os.path.exists(orig_file))
        self.assertFalse(os.path.exists(replace_file))
        self.assertFalse(os.path.exists(created_td))

        # -- test failure still cleans up
        try:
            with replaced_directory(test_dir) as td:
                created_td = td
                raise RuntimeError()
        except:
            pass

        self.assertTrue(os.path.exists(orig_file))
        self.assertFalse(os.path.exists(created_td))

        # -- cleanup testcase
        shutil.rmtree(test_dir)

    def test_capture_stdout(self):
        with capture_stdout() as capture:
            sys.stdout.write('foo\n')

        self.assertEqual(capture.getvalue(), 'foo\n')

    def test_capture_stderr(self):
        with capture_stderr() as capture:
            sys.stderr.write('foo\n')

        self.assertEqual(capture.getvalue(), 'foo\n')

    def test_pprint(self):
        d = {
            'foo':'bar',
            'thing':3,
        }

        expected = """{\n    "foo": "bar",\n    "thing": 3\n}\n"""

        with capture_stdout() as output:
            pprint(d)

        self.assertEqual(expected, output.getvalue())

    def test_noted_raise(self):
        # Test exiting context manager without an exception
        with noted_raise("Message"):
            self.assertTrue(True)

        with self.assertRaises(Exception) as ex:
            value = 1
            with noted_raise("Value={value}"):
                value += 21
                raise ValueError("A Value Error")

        ex = ex.exception
        if hasattr(ex, "add_note"):
            self.assertEqual(ex.__notes__, [" Value=22"])
        else:
            self.assertEqual(str(ex), "A Value Error Value=22")
