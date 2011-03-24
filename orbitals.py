import unittest
import time

import eventlet
eventlet.patcher.monkey_patch(all=True)

pool = eventlet.GreenPool()


class TestCaseHandler(object):
    """
    manages class setup and teardown functions
    """
    class_semaphores = {}
    instantiated_classes = []

    @classmethod
    def setUpClass(cls, c):
        if c not in cls.class_semaphores:
            cls.class_semaphores[c] = eventlet.semaphore.Semaphore()
        with cls.class_semaphores[c]:
            if c not in cls.instantiated_classes:
                cls.instantiated_classes.append(c)
                c.setUpClass()

    @classmethod
    def tearDownClasses(cls):
        for c in cls.instantiated_classes:
            c.tearDownClass()

class EventedTestSuite(unittest.TestSuite):
    """
    extends unittest.TestSuite by adding eventlet thread spawning to
    global pool
    """
    def __init__(self, tests=(), pool=pool):
        """
        extended __init__ to set self.pool to global pool
        """
        self.pool = pool
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
                    self.pool.spawn_n(test, result)
                else:
                    pool.waitall()
                    test(result)
            else:
                # setup class if necessary
                TestCaseHandler.setUpClass(test.__class__)
                if(self.thread_testcases):
                    self.pool.spawn_n(test, result)
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

        pool.waitall()
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

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def __init__(self, testname, parameters=None):
        super(TestCase, self).__init__(testname)
        self.parameters = parameters


class Orbitals(object):
    def __init__(self, test_class):
        EventedTextTestRunner(verbosity=2).run(test_class.suite())
