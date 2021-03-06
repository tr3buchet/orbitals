import time
import unittest

from gevent import monkey
from gevent import pool
from gevent import coros
monkey.patch_time()


pool = pool.Group()


class TestCaseHandler(object):
    """
    manages class setup and teardown functions
    """
    class_semaphores = {}
    instantiated_classes = []

    @classmethod
    def setUpClass(cls, c):
        """
        idea here is to only run the setup for a testcase class once
        even if there are multiple occurrences of the class in a suite

        the semaphore is to make sure that any other testcases of
        the same class which could have been called in parallel will
        wait for the class setup to finish before running any tests
        """
        try:
            cls.class_semaphores[c].acquire()
        except KeyError:
            cls.class_semaphores[c] = coros.Semaphore()

        if c not in cls.instantiated_classes:
            cls.instantiated_classes.append(c)
            c.setUpClass()

        cls.class_semaphores[c].release()

    @classmethod
    def tearDownClasses(cls):
        for c in cls.instantiated_classes:
            c.tearDownClass()


class EventedTestSuite(unittest.TestSuite):
    """
    extends unittest.TestSuite by adding gevent thread spawning to
    global pool
    """
    def __init__(self, tests=(), pool=pool):
        """
        extended __init__ to set self.pool to global pool
        """
        unittest.TestSuite.__init__(self, tests)
        self.thread_suites = False
        self.thread_testcases = False

    def run(self, result):
        """
        extend run to spawn threads
        """
        for test in self._tests:
            if isinstance(test, EventedTestSuite):
                if(self.thread_suites):
                    pool.spawn(test, result)
                else:
                    pool.join()
                    test(result)
            else:
                # setup class if necessary
                TestCaseHandler.setUpClass(test.__class__)
                if(self.thread_testcases):
                    pool.spawn(test, result)
                else:
                    test(result)


class EventedTextTestRunner(unittest.TextTestRunner):
    """
    extend unittest.TextTestRunner by having run wait for the threads in
    global pool to finish before tabulating test results
    """
    def run(self, test, pool=pool):
        """
        extend run to wait for global pool to finish
        """
        result = self._makeResult()
        startTime = time.time()
        test(result)

        pool.join()
        TestCaseHandler.tearDownClasses()

        stopTime = time.time()
        timeTaken = stopTime - startTime
        result.printErrors()
        self.stream.writeln(result.separator2)
        run = result.testsRun
        self.stream.writeln("Ran %d test%s in %.3fs" %
                            (run, run != 1 and "s" or "", timeTaken))
        self.stream.writeln()
        if not result.wasSuccessful():
            self.stream.write("FAILED (")
            failed, errored = map(len, (result.failures, result.errors))
            if failed:
                self.stream.write("failures=%d" % failed)
            if errored:
                if failed:
                    self.stream.write(", ")
                self.stream.write("errors=%d" % errored)
            self.stream.writeln(")")
        else:
            self.stream.writeln("OK")
        return result


class TestCase(unittest.TestCase):
    """
    extend unittest.TestCase in order to pass parameters to tests
    """

    get_client = None

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def __init__(self, testname, parameters=None):
        super(TestCase, self).__init__(testname)
        self.client = self.get_client()
        self.parameters = parameters

    def assert_parameters(self, *parameters):
        for p in parameters:
            self.assertTrue(p in self.parameters)


class Orbitals(object):
    def __init__(self, test_class):
        EventedTextTestRunner(verbosity=0).run(test_class.suite())
