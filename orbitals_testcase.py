import unittest
import time
from orbitals import EventedTestSuite
from orbitals import EventedTextTestRunner

class WhizzleGooberTestCase(unittest.TestCase):
    """
    extend the unittest.TestCase in order to use eventlet
    and allow for passing parameters to tests

    """

    def __init__(self, testname, s):
        super(WhizzleGooberTestCase, self).__init__(testname)
        self.s = s

    @staticmethod
    def suite():
        """
        define the suite of tests to be run

        """
        suite = EventedTestSuite()
        # add the tests giving each a parameter
        # (can easily be adapted to a set of parameters)
        suite.addTest(WhizzleGooberTestCase("test1","arrr"))
        suite.addTest(WhizzleGooberTestCase("test2","barrr"))
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
        print "test1 arg |%s|" % self.s
        time.sleep(5)
        print "done"

    def test2(self):
        """
        very simple test

        """
        print "test2 arg |%s|" % self.s
        time.sleep(5)
        print "done"


if __name__ == '__main__':

    # create the suite
    suite = WhizzleGooberTestCase.suite()

    # define whether we thread testcases
    suite.thread_testcases = False

    # generate the list of suites to be run
    # this is an arbitrary example
    suites = []
    some_list = ["hello","world","eva","orbitals","doctor","ellingham"]
    for i in range(len(some_list)/2):
        suites.append(suite)

    # turn suites into a super suite (suite containing suites)
    suites = EventedTestSuite(suites)

    # define whether we thread the suites
    suites.thread_suites = True

    # kick off the tests
    EventedTextTestRunner(verbosity=2).run(suites)
