import time
from orbitals import orbitals
from orbitals import utils


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
        for i in xrange(25):
            suite.addTest(WhizzleGooberTestCase('test_active',
                                                {'name': 'test_%s' % (i + 1)}))
#        suite.addTest(WhizzleGooberTestCase('test2', {'string': 'barrr'}))
        suite.thread_testcases = True
        return suite

    @classmethod
    def setUpClass(cls):
        cls.image = utils.get_image_by_name(cls.get_client(), 'Squeeze')
        cls.flavor = '2'
        print "setup class |%s|" % cls.__name__

    @classmethod
    def tearDownClass(cls):
        print "teardown class |%s|" % cls.__name__

    def setUp(self):
        """
        anything to be run before each test goes here
        """
        s = self.client.servers.create(name=self.parameters['name'],
                              image=self.image.id,
                              flavor=self.flavor)
        self.instance = s
        time.sleep(30)

    def tearDown(self):
        """
        anything to be run after each test goes here
        """
        self.client.servers.delete(self.instance.id)

    def retry_create(self, **kwargs):
        try:
            return self.client.servers.create(**kwargs)
        except Exception as e:
            print e
#            time.sleep(0.500)
#            return self.client.servers.create(**kwargs)

    def test_active(self):
        """
        very simple test
        """
        while True:
            try:
                s = self.client.servers.get(self.instance.id)
            except Exception as e:
                print 'get instance %s. error %s' % (self.instance.name, e)
#                s = self.client.servers.get(self.instance.id)

            if s.status == 'ACTIVE':
                return
            if s.status == 'ERROR':
                raise Exception('Instance |%s| status is in error' %
                                self.instance.id)
            time.sleep(5)

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
        for i in xrange(1000):
            suite.addTest(GadgetTestCase('test1'))
        suite.thread_testcases = True
        return suite

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

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
        for i in xrange(100):
            time.sleep(0)

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
        suites.append(WhizzleGooberTestCase.suite())
#        suites.append(GadgetTestCase.suite())
        suites = orbitals.EventedTestSuite(suites)
        suites.thread_suites = True
        return suites
