import time
from orbitals import Orbitals, TestCase, EventedTestSuite
import orbitals_testcase

class StressTest(TestCase):
    """
    Stress test for hitting nova hard and watching what happens

    """

    @staticmethod
    def suite():
        """
        define the suite of tests to be run

        """
        suites = []
        suites.append(orbitals_testcase.CreateInstance.suite())
        suites.append(orbitals_testcase.GadgetTestCase.suite())
        suites = EventedTestSuite(suites)
        suites.thread_suites = False
        return suites


main = Orbitals(StressTest)
