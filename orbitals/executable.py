import argparse
import functools
import imp
import os

from novaclient import client
#from novaclient import utils
import orbitals
from supernova import supernova
from supernova import executable as sexe


def run_orbitals():

    sn = supernova.SuperNova()
    sexe.check_supernova_conf(sn)

    # get arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', action=sexe._ListAction,
                        help='list configured environments')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='show debug output (overrides NOVACLIENT_DEBUG)')
    parser.add_argument('env',
                        help='environment to run tests against, '
                             'from ~/.supernova')
    parser.add_argument('testcase',
                        help='orbitals testcase to run')
    args = parser.parse_args()

    # set up the supernova object from args
    sexe.setup_supernova_env(sn, args.env)

    # get testcase class from testcase arg
    testcase = args.testcase.split('.')
    module_name = '.'.join(testcase[:-1])
    testcase_class_name = testcase[-1]
    try:
        module = __import__(module_name, fromlist=[''])
    except ImportError:
        res = imp.find_module(module_name, [os.getcwd()])
        module = imp.load_module(module_name, *res)
    print 'Running test suite from |%s| as defined in |%s|' % \
          (testcase_class_name, module.__file__)
    print 'on environment |%s|' % args.env

    # retrieve the test class config novaclient and start tests
    testclass = getattr(module, testcase_class_name)
    f = functools.partial(get_client, sn.prep_nova_creds(), args.debug)
    testclass.get_client = f
    testclass = orbitals.Orbitals(testclass)


def get_client(creds, debug=None):

    def to_bool(v):
        if v == '1':
            return True
        return False

    # translate .supernova env variables to client arg variables
    key_translate = {'NOVA_USERNAME': 'username',
                     'NOVA_API_KEY': 'api_key',
                     'NOVA_PROJECT_ID': 'project_id',
                     'NOVA_URL': 'auth_url',
                     'NOVA_REGION_NAME': 'region_name',
                     'NOVA_SERVICE_NAME': 'service_name',
                     'NOVA_VERSION': 'version',
                     'NOVACLIENT_INSECURE': 'insecure',
                     'NOVACLIENT_DEBUG': 'http_log_debug',
                     'NOVA_RAX_AUTH': 'nova_rax_auth',
                     'OS_NO_CACHE': 'no_cache'}

    # put the args to the client together
    client_args = {}
    for k, v in creds:
        client_args[key_translate[k]] = v

    # clean up the args
    if debug is not None:
        client_args['http_log_debug'] = debug
    elif 'http_log_debug' in client_args:
        client_args['http_log_debug'] = to_bool(client_args['http_log_debug'])
    if 'insecure' in client_args:
        client_args['insecure'] = to_bool(client_args['insecure'])
    if 'no_cache' in client_args:
        client_args['no_cache'] = to_bool(client_args['no_cache'])
    if 'nova_rax_auth' in client_args:
        if to_bool(client_args['nova_rax_auth']):
            os.environ.update({'NOVA_RAX_AUTH': '1'})
        del client_args['nova_rax_auth']

    return client.Client(**client_args)
