# waelstow.py
__version__ = '0.12.1'

import contextlib, os, shutil, sys, tempfile, json
from io import StringIO
from unittest import TestCase, TestSuite, TestLoader
from unittest.loader import _FailedTest

# =============================================================================
# Test Suite Discovery & Management
# =============================================================================

def list_tests(suites):
    """Takes a list of suites and returns an iterable of all the tests in
    the suites and their children.

    :param suites:
        A single or an interable of :class:`TestSuite` objects whose contents
        will be listed
    :returns:
        Iterable of :class:`TestCase` objects contained within the suites
    """
    for test in suites:
        if isinstance(test, TestCase):
            yield test
        else:
            for t in list_tests(test):
                yield t


def find_shortcut_tests(suites, shortcut_labels):
    """Takes a suite of tests and returns a list of tests that conform to the
    passed in list of short-cut labels.  A short-cut label begins with a "="
    or an ":" and indicates a partial string contained in either the name of
    the test or the test class.

    Example:

    .. code-block::python

        >>> list_tests(suite)
        [
            test_foo (wrench.test.SomeTest),
            test_foo (wrench.test.AnotherTest),
            test_bar (wrench.test.AnotherTest),
            test_bar (wrench.test.DifferentTest),
        ]
        >>> find_shorcut_tests(suite, ['=foo'])
        [
            test_foo (wrench.test.SomeTest),
            test_foo (wrench.test.AnotherTest),
        ]
        >>> find_shorcut_tests(suite, [':Another'])
        [
            test_foo (wrench.test.AnotherTest),
            test_bar (wrench.test.AnotherTest),
        ]

    :param suites:
        A single or iterable of :class:`TestSuite` objects to create the test
        subset from
    :param shortcut_labels:
        A list of short-cut labels to use to cull the list
    :returns:
        A list of :class:`TestCase` objects
    """
    # strip a leading '=' (or any character) from the front of each label
    labels = [label[1:] for label in shortcut_labels]

    results = []
    for test in list_tests(suites):
        if isinstance(test, _FailedTest):
            # If a test fails to load there is something wrong with the code
            # it imports, put it in the suite so the runner shows the
            # appropriate exception even if it doesn't match the label
            results.append(test)

        name = '%s.%s.%s' % (test.__module__, test.__class__.__name__,
            test._testMethodName)
        for label in labels:
            if label in name:
                results.append(test)

    return results


def discover_tests(start_dir, labels=[], pattern='test*.py'):
    """Discovers tests in a given module filtered by labels.  Supports
    short-cut labels as defined in :func:`find_shortcut_labels`.

    :param start_dir:
        Name of directory to begin looking in
    :param labels:
        Optional list of labels to filter the tests by
    :returns:
        :class:`TestSuite` with tests
    """
    shortcut_labels = []
    full_labels = []
    for label in labels:
        if label.startswith('=') or label.startswith(":"):
            shortcut_labels.append(label)
        else:
            full_labels.append(label)

    if not full_labels and not shortcut_labels:
        # no labels, get everything
        return TestLoader().discover(start_dir, pattern=pattern)

    shortcut_tests = []
    if shortcut_labels:
        suite = TestLoader().discover(start_dir, pattern=pattern)
        shortcut_tests = find_shortcut_tests(suite, shortcut_labels)

    if full_labels:
        suite = TestLoader().loadTestsFromNames(full_labels)
        suite.addTests(shortcut_tests)
    else:
        # only have shortcut labels
        suite = TestSuite(shortcut_tests)

    return suite

# =============================================================================
# Context Managers
# =============================================================================

@contextlib.contextmanager
def replaced_directory(dirname):
    """This ``Context Manager`` is used to move the contents of a directory
    elsewhere temporarily and put them back upon exit.  This allows testing
    code to use the same file directories as normal code without fear of
    damage.

    The name of the temporary directory which contains your files is yielded.

    :param dirname:
        Path name of the directory to be replaced.


    Example:

    .. code-block:: python

        with replaced_directory('/foo/bar/') as rd:
            # "/foo/bar/" has been moved & renamed
            with open('/foo/bar/thing.txt', 'w') as f:
                f.write('stuff')
                f.close()


        # got here? => "/foo/bar/ is now restored and temp has been wiped, 
        # "thing.txt" is gone
    """
    if dirname[-1] == '/':
        dirname = dirname[:-1]

    full_path = os.path.abspath(dirname)
    if not os.path.isdir(full_path):
        raise AttributeError('dir_name must be a directory')

    base, name = os.path.split(full_path)

    # create a temporary directory, move provided dir into it and recreate the
    # directory for the user
    tempdir = tempfile.mkdtemp()
    shutil.move(full_path, tempdir)
    os.mkdir(full_path)
    try:
        yield tempdir

    finally:
        # done context, undo everything
        shutil.rmtree(full_path)
        moved = os.path.join(tempdir, name)
        shutil.move(moved, base)
        shutil.rmtree(tempdir)


@contextlib.contextmanager
def capture_stdout():
    """This ``Context Manager`` redirects STDOUT to a ``StringIO`` objects
    which is returned from the ``Context``.  On exit STDOUT is restored.

    Example:

    .. code-block:: python

        with capture_stdout() as capture:
            print('foo')

        # got here? => capture.getvalue() will now have "foo\\n"
    """
    stdout = sys.stdout
    try:
        capture_out = StringIO()
        sys.stdout = capture_out
        yield capture_out
    finally:
        sys.stdout = stdout


@contextlib.contextmanager
def capture_stderr():
    """This ``Context Manager`` redirects STDERR to a ``StringIO`` objects
    which is returned from the ``Context``.  On exit STDERR is restored.

    Example:

    .. code-block:: python

        with capture_stderr() as capture:
            print('foo')

        # got here? => capture.getvalue() will now have "foo\\n"
    """
    stderr = sys.stderr
    try:
        capture_out = StringIO()
        sys.stderr = capture_out
        yield capture_out
    finally:
        sys.stderr = stderr


class noted_raise:
    """This ``Context Manager`` is used to annotate an exception raised within
    its block. Sometimes when testing you might have a loop with variables, if
    an assert fails in the loop you'd like to see more of the context. This
    context manager allows you to define a message format based on local
    variables and if there is an exception it will add info the exception's
    message.

    If you're using a version of Python that supports ``Exception.add_note()``
    (Python >=3.11), your formatted message is added as a note. If you are
    not, it assumes the first argument to the ``Exception`` is the message and
    appends text to it.

    :param message: The message string to append in the case of an exception.
        This string is passed to ``str.format()`` using local variables as the
        context. Anything local variable you have defined will be available as
        a named value in the message string.

    .. code-block:: python

        with noted_raise("Counter:{counter}"):
            for counter in range(1, 10):
                self.assertTrue(counter < 5)

    The above example will result in ``AssertionEror`` with either a note that
    containing " Counter:5", or the exceptions message string having the same
    appended to the end.
    """
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is None:
            # No exception, do nothing
            return

        # Exited context manager with exception, use the locals from the stack
        # frame as context for the message
        text = " " + self.message.format(**exc_tb.tb_frame.f_locals)

        if hasattr(exc_value, "add_note"):
            # Version of Python being run has the Exception.add_note feature,
            # used it to add the info
            exc_value.add_note(text)
        else:
            # For Python's without Exception.add_note(), (3.10 and below) need
            # to modify the exceptions message, assume that's the first arg
            # (which it usually is)
            exc_value.args = (exc_value.args[0] + text, ) + exc_value.args[1:]

# =============================================================================
# Misc
# =============================================================================

def pprint(data):
    """Alternative to `pprint.PrettyPrinter()` that uses `json.dumps()` for
    sorting and displaying data.

    :param data: item to print to STDOUT.  The item must be json serializable!
    """
    print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
