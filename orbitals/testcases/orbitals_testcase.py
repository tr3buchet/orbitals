import time
from orbitals import orbitals


class UberTestCase(orbitals.TestCase):
    """
    extend the orbitals.TestCase to create an orbitals test case
    in this example we have a suite of suites

    Note that if this is the main test case class being run by orbitals,
    if it will be using suites from other classes, a suite of suites,
    those classes need to subclass this one in order to inherit the
    get_client callback attribute from the main test case.
    """

    @staticmethod
    def suite():
        """
        define the suite of tests to be run
        """
        suites = []
        suites.append(WhizzleGooberTestCase.suite())
        suites.append(WhizzleGooberTestCase.suite())
        suites.append(GadgetTestCase.suite())
        suites = orbitals.EventedTestSuite(suites)
        suites.thread_suites = True
        return suites


class WhizzleGooberTestCase(UberTestCase):
    """
    extend the orbitals.TestCase to create an orbitals test case
    """

    @staticmethod
    def suite():
        """
        define the suite of tests to be run
        """
        suite = orbitals.EventedTestSuite()
        # add the tests giving each a parameter
        # (can easily be adapted to a set of parameters)
        suite.addTest(WhizzleGooberTestCase('test1', {'string': 'arrr'}))
        suite.addTest(WhizzleGooberTestCase('test2', {'string': 'barrr'}))
        suite.thread_testcases = False
        return suite

    @classmethod
    def setUpClass(cls):
        cls.something = "yeargh!"
        cls.something_else = "blorb"
        time.sleep(15)
        print "setup class |%s|" % cls.__name__

    @classmethod
    def tearDownClass(cls):
        print "teardown class |%s|" % cls.__name__

    def setUp(self):
        """
        anything to be run before each test goes here
        """
        print "\nbefore test"

    def tearDown(self):
        """
        anything to be run after each test goes here
        """
        print "after test"

    def test1(self):
        """
        very simple test
        """
        # example of using something from setUpClass
        if(self.something):
            self.something = "works!"
        print "test1 arg |%s|" % self.parameters
        time.sleep(5)
        print "done"

    def test2(self):
        """
        very simple test
        """
        print "test2 arg |%s|" % self.parameters
        time.sleep(5)
        print "done"


class GadgetTestCase(UberTestCase):
    """
    extend the orbitals.TestCase to create an orbitals test case
    """

    @staticmethod
    def suite():
        """
        define the suite of tests to be run
        """
        suite = orbitals.EventedTestSuite()
        # add the tests giving each a parameter
        # (can easily be adapted to a set of parameters)
        suite.addTest(GadgetTestCase('test1', {'string': 'xarrr'}))
        suite.addTest(GadgetTestCase('test2', {'string': 'xbarrr'}))
        suite.thread_testcases = True
        return suite

    @classmethod
    def setUpClass(cls):
        cls.something = "yeargh!"
        cls.something_else = "blorb"
        time.sleep(5)
        print "setup class |%s|" % cls.__name__

    @classmethod
    def tearDownClass(cls):
        print "teardown class |%s|" % cls.__name__

    def setUp(self):
        """
        anything to be run before each test goes here
        """
        pass

    def tearDown(self):
        """
        anything to be run after each test goes here
        """
        pass

    def test1(self):
        """
        very simple test
        """
        print "test1 arg |%s|" % self.parameters
        time.sleep(5)
        print "done"

    def test2(self):
        """
        very simple test
        """
        print "test2 arg |%s|" % self.parameters
        time.sleep(5)
        print "done"
