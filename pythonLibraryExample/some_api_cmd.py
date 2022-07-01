from some_api_library import Environment
# import getpass # only for python 3
import sys
import json

import logging

# create logger
logger = logging.getLogger('some_api_cmd')
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


def main():
    if sys.version[0] == '3':
        import getpass
        login = str(input('SomeApi_Login: '))
        password = getpass.getpass('SomeApi_Password: ')
    elif sys.version[0] == '2':
        login = str(raw_input('SomeApi_Login: '))
        password = str(raw_input('SomeApi_Password: ')) # unsecure, getpass don't support python2
    else:
        logger.critical('python vertion %s  not supported' % (sys.version[0:5])) 


    # Environment(location, local_path, some_path, service_name, login, password)

    # TO DO functin verify that local_path exists, if not create it.
    # import os
    # print(os.path.isdir("/home/el"))
    # print(os.path.exists("/home/el/myfile.txt"))


# Create directory
# dirName = 'tempDir'
# 
# try:
#     # Create target Directory
#     os.mkdir(dirName)
#     print("Directory " , dirName ,  " Created ") 
# except FileExistsError:
#     print("Directory " , dirName ,  " already exists")


#  (location, componentOne_download_path, componentOne_upload_path, componentTwo_download_path, componentTwo_upload_path, componentThree_download_path, componentThree_upload_path, some_path, service_name, login, password)

    MAIN_PROJECT_PATH = '/root/some_api_configuration_manager/'
    TEMP_PROJECT_PATH = '/tmp/some_api_library/'

    ENV01 = Environment( location_name                = 'ENV01',
                         componentOne_download_path   = TEMP_PROJECT_PATH + 'ENV01/componentOne/Configuration/',
                         componentOne_upload_path     = MAIN_PROJECT_PATH + 'ENV01/componentOne/Configuration/',
                         componentTwo_download_path   = TEMP_PROJECT_PATH + 'ENV01/componentTwo/Configuration/',
                         componentTwo_upload_path     = MAIN_PROJECT_PATH + 'ENV01/componentTwo/Configuration/',
                         componentThree_download_path = TEMP_PROJECT_PATH + 'ENV01/componentThree/Configuration/',
                         componentThree_upload_path   = MAIN_PROJECT_PATH + 'ENV01/componentThree/Configuration/',
                         some_path                     = 'https://some.stage.example.com/environment-api/api/Stage/ENV01/',
                         service_name_list            = ['componentOne', 'componentTwo', 'componentThree'],
                         login                        = login,
                         password                     = password
                       )

    '''

    ENV02 = Environment( location_name                = 'ENV02',
                         componentOne_download_path   = TEMP_PROJECT_PATH + 'ENV02/componentOne/Configuration/',
                         componentOne_upload_path     = MAIN_PROJECT_PATH + 'ENV02/componentOne/Configuration/',
                         componentTwo_download_path   = TEMP_PROJECT_PATH + 'ENV02/componentTwo/Configuration/',
                         componentTwo_upload_path     = MAIN_PROJECT_PATH + 'ENV02/componentTwo/Configuration/',
                         componentThree_download_path = TEMP_PROJECT_PATH + 'ENV02/componentThree/Configuration/',
                         componentThree_upload_path   = MAIN_PROJECT_PATH + 'ENV02/componentThree/Configuration/',
                         some_path                     = 'https://some.stage.example.com/environment-api/api/Stage/ENV02/',
                         service_name_list            = ['componentOne', 'componentTwo', 'componentThree'],
                         login                        = login,
                         password                     = password
                       )
    '''

    '''

    ENV03 = Environment( location_name                = 'ENV03',
                         componentOne_download_path   = TEMP_PROJECT_PATH + 'ENV03/componentOne/Configuration/',
                         componentOne_upload_path     = MAIN_PROJECT_PATH + 'ENV03/componentOne/Configuration/',
                         componentTwo_download_path   = TEMP_PROJECT_PATH + 'ENV03/componentTwo/Configuration/',
                         componentTwo_upload_path     = MAIN_PROJECT_PATH + 'ENV03/componentTwo/Configuration/',
                         componentThree_download_path = TEMP_PROJECT_PATH + 'ENV03/componentThree/Configuration/',
                         componentThree_upload_path   = MAIN_PROJECT_PATH + 'ENV03/componentThree/Configuration/',
                         some_path                     = https://some.pro.example.com/environment-api/api/Production/ENV03/',
                         service_name_list            = ['componentOne', 'componentTwo', 'componentThree'],
                         login                        = login,
                         password                     = password
                       )
    '''

    test_inventory = ENV01.show_inventory()
    logger.info(" ".join(['test_inventory:', json.dumps(test_inventory, indent = 4, sort_keys = False)]))

    # test_inventory2 = ENV01.show_inventory('env01-stage-(componentOne|componentTwo)2')
    # logger.info(" ".join(['test_inventory:', json.dumps(test_inventory2, indent = 4, sort_keys = False)]))

    # test_inventory3 = ENV01.show_inventory('env01-stage-(componentOne|componentTwo)[15]')
    # logger.info(" ".join(['test_inventory:', json.dumps(test_inventory3, indent = 4, sort_keys = False)]))

    ENV01.bulk_download()
    # ENV02.bulk_download(limit = 'env02-stage-(componentOne|componentTwo)0')
    # ENV01.show_difference(limit = '(env01-stage-(componentOne|componentTwo)0|env01-stage-componentThree4)')

    # difference_with_remote = ENV01.show_difference(limit = 'env01-stage-componentOne[15]')
    # logger.info(" ".join(['difference_with_remote:', json.dumps(difference_with_remote, indent = 4, sort_keys = False)]))


if __name__ == '__main__':
    logger.info("I'm some_api_cmd.py")
    main()
