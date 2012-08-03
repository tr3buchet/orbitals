import argparse
import os

from novaclient import client
#from novaclient import utils
import orbitals
from supernova import supernova
from supernova import executable as sexe
try:
    import importlib
except ImportError:
    pass


def run_orbitals():

    sn = supernova.SuperNova()
    sexe.check_supernova_conf(sn)

    # get arguments
    # optparse in case i want to add more options later
    parser = argparse.ArgumentParser('some stuff')
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
    print args

#sexe.setup_supernova_env(sn, args.env)

#    nc = get_client(sn.prep_nova_creds(), args.debug)
    #client.authenticate()

    #create_server(image_uuid='06c6a986-de1f-42e2-9670-dea1869f6525')
#    list_servers(nc)

    testcase = args.testcase.split('.')
    module_name = '.'.join(testcase[:-1])
    testcase_class = testcase[-1]
    print 'module_name -> |%s|' % module_name
    print 'testcase_class -> |%s|' % testcase_class
    try:
        module = importlib.import_module(module_name)
    except NameError:
        module = __import__(module_name, fromlist=[''])

    orbitals.Orbitals(getattr(module, testcase_class))


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

run_orbitals()
