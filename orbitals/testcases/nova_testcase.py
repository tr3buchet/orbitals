import time
from orbitals import orbitals
from orbitals import utils


class BuildActiveDelete(orbitals.TestCase):

    @staticmethod
    def suite():
        """
        define the suite of tests to be run
        """
        suite = orbitals.EventedTestSuite()
        for i in xrange(25):
            suite.addTest(BuildActiveDelete('instance_active',
                                            {'name': 'test_%s' % (i + 1)}))
        suite.thread_testcases = True
        return suite

    @classmethod
    def setUpClass(cls):
        # determine image and flavor to use
        cls.image = utils.get_image_by_name(cls.get_client(), 'Squeeze')
        cls.flavor = '2'

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # build/store instance
        s = self.client.servers.create(name=self.parameters['name'],
                              image=self.image.id,
                              flavor=self.flavor)
        self.instance = s
        time.sleep(10)

    def tearDown(self):
        # delete the instance
        self.client.servers.delete(self.instance.id)

    def instance_active(self):
        # poll self.instance until status become 'ACTIVE'
        while True:
            s = self.client.servers.get(self.instance.id)

            if s.status == 'ACTIVE':
                return
            if s.status == 'ERROR':
                raise Exception('Instance |%s| status is in error' %
                                self.instance.id)
            time.sleep(1)
