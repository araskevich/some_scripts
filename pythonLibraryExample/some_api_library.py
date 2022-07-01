""" Some API Python module.
    Module works with python version 2 and 3.
    No printing from this module, use logging.info etc

cat <<EOF> requirements.txt
requests==2.23.0
requests-toolbelt==0.9.1
EOF

pip3 install -r requirements.txt
   or
pip2 install -r requirements.txt
"""

import requests
from requests.auth import HTTPBasicAuth 
from requests_toolbelt import MultipartEncoder
import json
import yaml
import sys
import re
import os

import warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

import logging

# create logger
logger = logging.getLogger('some_api_library')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# 'application' code
# logger.debug('debug message')
# logger.info('info message')
# logger.warn('warn message')
# logger.error('error message')
# logger.critical('critical message')

logger.info('I\'m running under python %s' %(sys.version[0:5]))
global python_version
python_version = sys.version[0:1]


class Environment:
    """ Class Environment described single some enviroment:

        Attributes:
         - location_name: type str, 
         - componentOne_download_path: type str,
         - componentOne_upload_path: type str,
         - componentTwo_download_path: type str,
         - componentTwo_upload_path: type str,
         - componentThree_download_path: type str,
         - componentThree_upload_path: type str,
         - some_path: type str, path to environment common layer
         - service_name: type list, list of services; supported componentOne, componentTwo, componentThree
         - login: type str, login to some api
         - password: type str, password to some api

        Methods:
         - __init__: method for initiate Environment, create inventory json; create local directories: download_path, upload_path
         - __del__: method is called when your object is finally destroyed.
         - show_inventory: show inventory json, used for library work, which generate for particular Environment, can be limited by regex
         - show_difference: show difference between local_path (download_path) and remote_path (upload_path), can be limited by regex
         - bulk_download: method is used for download policy file from someApi, can be limited by regex
         - bulk_upload: method is used for upload policy file to someApi, can be limited by regex
    """

    def __init__(self, location_name, componentOne_download_path, componentOne_upload_path, componentTwo_download_path, componentTwo_upload_path, componentThree_download_path, componentThree_upload_path, some_path, service_name_list, login, password):
        """ __init__: method for initiate Environment, create inventory json; create local directories: download_path, upload_path """
      
        assert type(location_name) == str, "Require type str for variable"
        assert type(componentOne_download_path) == str, "Require type str for variable"
        assert type(componentOne_upload_path) == str, "Require type str for variable"
        assert type(componentTwo_download_path) == str, "Require type str for variable"
        assert type(componentTwo_upload_path) == str, "Require type str for variable"
        assert type(componentThree_download_path) == str, "Require type str for variable"
        assert type(componentThree_upload_path) == str, "Require type str for variable"
        assert type(some_path) == str, "Require type str for variable"
        assert type(service_name_list) == list, "Require type list for variable"
        assert type(login) == str, "Require type str for variable"
        assert type(password) == str, "Require type str for variable"
               

        def get_environment_info(some_path, service_name_list):
            # link = "https://some.stage.example.com/environment-api/api/Stage/ENV01/"

            service_pool = []

            link = some_path
            response = requests.get(link, verify=False, timeout=30)
            logger.info(" ".join(["get_environment_info", self.some_path, "Status_code:", str(response.status_code)]))
            data = json.loads(response.text)
            data_parsed = data['pod']['group_list']
            for i in range(len(data_parsed)):
                if data_parsed[i]['service_name'] in service_name_list:
                    service_node = {}
                    service_name = data_parsed[i]['service_name']
                    service_group_number = data_parsed[i]['number']
                    service_group_list = [data_parsed[i]['service_list'][j]['name'] for j in range(len(data_parsed[i]['service_list']))]
                    service_group = service_name.upper() + str(service_group_number)

                    service_node.update({"service_name": service_name})
                    service_node.update({"service_group": service_group})

                    if service_name == "componentOne":
                        some_link_to_download_policy = some_path.replace("/api/", "/variable/") + service_group + '/?format=json&name=componentOne.Policy'
                        some_link_to_upload_policy = some_path.replace("/api/", "/upload-variable/") + service_group + '/'
                        # local_path_to_download_policy = local_path
                        # local_path_to_upload_policy = 
                        service_policy_name = service_group_list[0][:14] + 'x_policy.json'
 
                    elif service_name == "componentTwo":
                        some_link_to_download_policy = some_path.replace("/api/", "/variable/") + service_group + '/?format=json&name=componentTwo.Configuration'
                        some_link_to_upload_policy = some_path.replace("/api/", "/upload-variable/") + service_group + '/'
                        service_policy_name = service_group_list[0][:14] + 'x_policy.json'

                    elif service_name == "componentThree":
                        some_link_to_download_policy = some_path.replace("/api/", "/variable/") + service_group + '/?format=json&name=componentThree.Policy'
                        some_link_to_upload_policy = some_path.replace("/api/", "/upload-variable/") + service_group + '/'
                        service_policy_name = service_group_list[0][:14] + 'x_policy.yaml'

                    else:
                        logger.critical("Service_name: %s not supported!" % service_name)                         

                    service_node.update({"some_link_to_download_policy": some_link_to_download_policy})
                    service_node.update({"some_link_to_upload_policy": some_link_to_upload_policy})
                    service_node.update({"service_policy_name": service_policy_name})
                    service_node.update({"service_group_list": service_group_list})

                    service_pool.append((service_node))

            return service_pool

        def verify_path(path):
            global python_version

            if os.path.isdir(path):
                logger.info("Path exists: %s" %path)
            else:
                logger.warn("Path not exists: %s" %path)
                if python_version == '2':
                    os.makedirs(path, 420) # 420 equivalent of 0644, python 2
                    python = '2'
                elif python_version == '3':
                    os.makedirs(path, 0o644) # 0o644 equivalent of 0644, python 3
                    python = '3'
                else:
                    logger.critical("Supported python 2 and 3 version")
                    python = 'NONE'
                verify_path(path)
                logger.warn("Path created: %s, permission: %s, python: %s" %(path, '0644', python))


        logger.info("Initing %s" %(location_name))
        self.location_name              = location_name
        # self.local_path               = local_path
        # self.componentOne_local_path  = componentOne_local_path

        self.componentOne_download_path    = componentOne_download_path
        self.componentOne_upload_path      = componentOne_upload_path
        self.componentTwo_download_path    = componentTwo_download_path
        self.componentTwo_upload_path      = componentTwo_upload_path
        self.componentThree_download_path  = componentThree_download_path
        self.componentThree_upload_path    = componentThree_upload_path

        self.some_path          = some_path
        self.service_name_list  = service_name_list
        self.login              = login
        self.password           = password
        self.service_pool       = get_environment_info(some_path, service_name_list)

        for path in [componentOne_download_path, componentOne_upload_path, componentTwo_download_path, componentTwo_upload_path, componentThree_download_path, componentThree_upload_path]:
            verify_path(path)

        logger.info("Inited %s" %(location_name))
        logger.info(" ".join([location_name, componentOne_download_path, componentOne_upload_path, componentTwo_download_path, componentTwo_upload_path,
                              componentThree_download_path, componentThree_upload_path, some_path, str(service_name_list), login]))

      
    def __del__(self):
        """ __del__: method is called when your object is finally destroyed. """

        logger.info("%s removed." % (self.location_name))


    def show_inventory(self, limit = '.*'):
        """ show_inventory: show inventory json, used for library work, which generate for particular Environment, can be limited by regex """

        assert type(limit) == str, "Require type str for variable"

        new_service_pool = []
        service_pool = self.service_pool
        for service_node in range(len(service_pool)):
            for node in range(len(service_pool[service_node]['service_group_list'])):
                if re.match(r'.*' + r'%s' % str(limit).lower(), service_pool[service_node]['service_group_list'][node]) and service_pool[service_node] not in new_service_pool:
                    new_service_pool.append(service_pool[service_node])
        logger.info(" ".join(["show_inventory", self.login, json.dumps(new_service_pool, indent = 4, sort_keys = False)]))
        return new_service_pool


    def show_difference(self, limit = '.*'):
        """ show_difference: show difference between local_path (download_path) and remote_path (upload_path), can be limited by regex """

        assert type(limit) == str, "Require type str for variable"

        def difference_for_dictionary(difference_pool, local_file_value, remote_file_value):
            if type(local_file_value) == dict:
                # if len(local_file_value.keys()) != len(remote_file_value.keys()):

                if local_file_value.items() != remote_file_value.items():
                    for key, value in local_file_value.items():
                        try:
                            if local_file_value[key] != remote_file_value[key]:
                                difference_for_dictionary(difference_pool, local_file_value[key], remote_file_value[key])
                        except:
                            logger.info("difference_for_dictionary: missmatch_with_remote_key: %s" %key)
                            difference_pool.append((key, "missmatch_with_remote_key"))
                            logger.info("difference_for_dictionary: difference_pool: %s" %difference_pool)
            elif type(local_file_value) == list:
                # if len(local_file_value) != len(remote_file_value):

                if local_file_value != remote_file_value:
                    # TODO add try/expect for list range missmatch_with_remote_key
                    for i in range(len(local_file_value)):
                        if local_file_value[i] != remote_file_value[i]:
                            difference_for_dictionary(difference_pool, local_file_value[i], remote_file_value[i])
            elif type(local_file_value) == str or type(local_file_value) == int:
                difference_pool.append((local_file_value, remote_file_value))
            else:
                logger.info("difference_for_dictionary: Something unexpected was recived: %s " % local_file_value)
                difference_for_dictionary(difference_pool, str(local_file_value), str(remote_file_value))


        logger.info(" ".join(["show_difference", "limit: %s" %limit , self.login]))
        # self.bulk_download(limit)
        service_pool = self.show_inventory(limit)
        service_pool_difference = {}

        for service_node in range(len(service_pool)):
            service_name = service_pool[service_node]['service_name']
            service_policy_name = service_pool[service_node]['service_policy_name']
            if service_name == "componentOne":
                local_path  = self.componentOne_upload_path
                remote_path = self.componentOne_download_path
            elif service_name == "componentTwo":
                local_path  = self.componentTwo_upload_path
                remote_path = self.componentTwo_download_path
            elif service_name == "componentThree":
                local_path  = self.componentThree_upload_path
                remote_path = self.componentThree_download_path
            else:
                logger.critical("Service_name: %s not supported!" % service_name)

            # local_file  = map(lambda x: x.strip(), list(open(local_path + service_policy_name)))
            # remote_file = map(lambda x: x.strip(), list(open(remote_path + service_policy_name)))
            # difference_list  = list(zip(local_file, remote_file))

            local_file  = open(local_path + service_policy_name).read()
            remote_file = open(remote_path + service_policy_name).read()

            if service_name in ["componentTwo", "componentOne"]:
                local_file_value  = json.loads(local_file)
                remote_file_value = json.loads(remote_file)
            elif service_name == "componentThree":
                local_file_value  = yaml.load(local_file, Loader=yaml.BaseLoader)
                remote_file_value = yaml.load(remote_file, Loader=yaml.BaseLoader)
                # local_file_value  = yaml.load(local_file, Loader=yaml.FullLoader)
                # remote_file_value = yaml.load(remote_file, Loader=yaml.FullLoader)
            else:
                logger.critical("Service_name: %s not supported!" % service_name)

            difference_pool = []
            difference_for_dictionary(difference_pool, local_file_value, remote_file_value)
            logger.info("difference_for_dictionary: end_difference_pool: %s" %difference_pool)
            difference_total = {}

            # for line in range(len(difference_list)):
            #     if difference_list[line][0] != difference_list[line][1]:
            #         difference_total.update({"string %s" %line: [difference_list[line][0], difference_list[line][1]]})

            for line in range(len(local_file.split("\n"))):
                for i in range(len(difference_pool)):
                    if str(difference_pool[i][0]) in [item.strip('":') for item in "".join(local_file.split("\n")[line]).strip(' ,').split()]:
                        difference_total.update({"string %s" %(line + 1): [difference_pool[i][0], difference_pool[i][1]]})

            if difference_total == {}:
                difference_total.update({"NONE": "NONE"})
            service_pool_difference.update({service_policy_name : [difference_total]})
            logger.info(" ".join(["show_difference", local_path + service_policy_name, remote_path + service_policy_name, self.login, json.dumps(difference_total, indent = 4, sort_keys = True)]))
        logger.info(" ".join(["show_difference", "limit: %s" %limit, self.login, json.dumps(service_pool_difference, indent = 4, sort_keys = False)]))
        return service_pool_difference


    def bulk_download(self, limit = '.*'):
        """ bulk_download: method is used for download policy file from someApi, can be limited by regex """

        assert type(limit) == str, "Require type str for variable"

        def download_variable_from_some(some_path, local_path, service_name, login, password):
            # link = "https://some.stage.example.com/environment-api/variable/Stage/ENV01/componentOne3/?format=json&name=componentOne.Policy
            link = some_path
            response = requests.get(link, verify=False, timeout=30, auth=HTTPBasicAuth(login, password))
            logger.info(" ".join(["download_variable_from_some", self.login, some_path, local_path, service_name, "Status_code:", str(response.status_code)]))

            if service_name == "componentOne":
                policy = json.loads(response.text)["componentOne.Policy"]
            elif service_name == "componentTwo":
                policy = json.loads(response.text)["componentTwo.Configuration"]
            elif service_name == "componentThree":
                policy = json.loads(response.text)["componentThree.Policy"]
            else:
                logger.critical("Service_name: %s not supported!" % service_name)

            f = open(local_path, 'w+')
            f.write(str(policy))
            f.close

        logger.info("Starting download %s, limit: %s" %(self.location_name, limit))
        service_pool = self.show_inventory(limit)
        login        = self.login
        password     = self.password

        for service_node in range(len(service_pool)):
            service_name = service_pool[service_node]['service_name']
            some_link_to_download_policy = service_pool[service_node]['some_link_to_download_policy']
            service_policy_name = service_pool[service_node]['service_policy_name']

            if service_name == "componentOne":
                local_path = self.componentOne_download_path
            elif service_name == "componentTwo":
                local_path = self.componentTwo_download_path
            elif service_name == "componentThree":
                local_path = self.componentThree_download_path
            else:
                logger.critical("Service_name: %s not supported!" % service_name)

            logger.info(" ".join(["bulk_download", "limit: %s " %limit, some_link_to_download_policy, local_path + service_policy_name, service_name, login]))
            download_variable_from_some(some_link_to_download_policy, local_path + service_policy_name, service_name, login, password)

        logger.info("Completed download %s" %(self.location_name))


    def bulk_upload(self, limit = '.*'):
        """ bulk_upload: method is used for upload policy file to some api, can be limited by regex """

        assert type(limit) == str, "Require type str for variable"

        def upload_variable_to_some(some_path, local_path, service_name, login, password):
            # link = "https://some.stage.example.com/environment-api/upload-variable/Stage/ENV01/componentOne3/"
            link = some_path
            filename = local_path.split('/')[-1:][0]

            if service_name == "componentOne":
                policy = "componentOne.Policy"
            elif service_name == "componentTwo":
                policy = "componentTwo.Configuration"
            elif service_name == "componentThree":
                policy = "componentThree.Policy"
            else:
                logger.critical("Service_name: %s not supported!" % service_name)

            data = MultipartEncoder(
                   fields={'name': policy,
                            'file': (filename, open(local_path, 'rb'), 'text/plain')}
                   )
            headers={'Content-Type': data.content_type}

            response = requests.post(link, data = data, headers=headers, verify=False, timeout=30, auth=HTTPBasicAuth(login, password))
            logger.info(" ".join(["upload_variable_to_some", self.login, some_path, local_path, service_name, "Status_code:", str(response.status_code)]))
            logger.info(" ".join(["response.text", response.text]))

        logger.info("Starting upload %s, limit: %s" %(self.location_name, limit))
 
        difference_with_remote = self.show_difference(limit)

        service_pool = self.show_inventory(limit)
        login        = self.login
        password     = self.password

        for service_node in range(len(service_pool)):
            service_name = service_pool[service_node]['service_name']
            some_link_to_upload_policy = service_pool[service_node]['some_link_to_upload_policy']
            service_policy_name = service_pool[service_node]['service_policy_name']

            if service_name == "componentOne":
                local_path = self.componentOne_upload_path
            elif service_name == "componentTwo":
                local_path = self.componentTwo_upload_path
            elif service_name == "componentThree":
                local_path = self.componentThree_upload_path
            else:
                logger.critical("Service_name: %s not supported!" % service_name)

            logger.info(" ".join(["bulk_upload", "limit: %s " %limit, some_link_to_upload_policy, local_path + service_policy_name, service_name, login]))
            upload_variable_to_some(some_link_to_upload_policy, local_path + service_policy_name, service_name, login, password)

        logger.info("Completed upload %s" %(self.location_name))
        return difference_with_remote

if __name__ == '__main__':
    logger.info("I'm some_api_library.py")
