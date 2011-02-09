import time
import orbitals
import cloudservers
cs = cloudservers.CloudServers('admin', 'admin', 'http://localhost:8774/v1.0/')


class CreateInstance(orbitals.TestCase):
    """
    Tests creating an instance

    """

    @staticmethod
    def suite():
        """
        define the suite of tests to be run

        """
        suite = orbitals.EventedTestSuite()
        suite.addTest(CreateInstance('create_instance',
                                     {'flavor': '1', 'image':'2'}))
        suite.addTest(CreateInstance('create_instance',
                                     {'flavvor': '1', 'image':'2'}))
        suite.addTest(CreateInstance('test2', {'string': 'barrr'}))
        suite.thread_testcases = False
        return suite

    def setUp(self):
        """
        anything to be run before each test goes here

        """
        pass

    def create_instance(self):
        """
        tests creating an instance
        flavor and image are expected to be set in self.parameter

        """
        self.assert_parameters('flavor', 'image')
        flavor = self.parameters['flavor']
        image = self.parameters['image']
        print "YAY"
        instance = cs.servers.create('stupid', image, flavor)
#        instance.wait_for_status('active', timer='create')
#        self.assert_no_errors(instance)
#        instance.destroy()
#        s.destroy()
#        self.assert_no_errors(instance)


    def test2(self):
        """
        very simple test

        """
        print "test2 arg |%s|" % self.parameters
        time.sleep(3)
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
        time.sleep(3)
        print "done"

    def test2(self):
        """
        very simple test

        """
        print "test2 arg |%s|" % self.parameters
        time.sleep(3)
        print "done"
