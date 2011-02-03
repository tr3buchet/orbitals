import time
import orbitals


class WhizzleGooberTestCase(orbitals.TestCase):
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

    def setUp(self):
        """
        anything to be run before each test goes here

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


class GadgetTestCase(orbitals.TestCase):
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

    def setUp(self):
        """
        anything to be run before each test goes here

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


class UberTestCase(orbitals.TestCase):
    """
    extend the orbitals.TestCase to create an orbitals test case
    in this example this is a super TestCase which uses other test
    cases

    """

    @staticmethod
    def suite():
        """
        define the suite of tests to be run

        """
        suites = []
        suites.append(WhizzleGooberTestCase.suite())
        suites.append(GadgetTestCase.suite())
        suites = orbitals.EventedTestSuite(suites)
        suites.thread_suites = False
        return suites


main = orbitals.Orbitals(UberTestCase)
