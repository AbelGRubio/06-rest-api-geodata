from .tests_basedatos import *
from .tests_endpoints import *


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


TEST_PASS = f'{bcolors.OKGREEN}The test was ok!!{bcolors.ENDC}'
TEST_NO_PASS = f'{bcolors.FAIL}The test has a problem!{bcolors.ENDC}'

DEFINED_TEST = [var_name for var_name in dir() if 'test_' in var_name]


def start_all_test():
    print('\n\n{}{}Starting test!!{}\n\n'.format(
        bcolors.BOLD,
        bcolors.WARNING, bcolors.ENDC))


def header_test(number_test: int, test_: str):
    print('{}{}--> {}Doing test number {}: {}{}'.format(
        bcolors.BOLD,
        bcolors.OKBLUE, bcolors.UNDERLINE,
        number_test,
        test_, bcolors.ENDC))


def no_pass_test(error_message: Exception):
    print(TEST_NO_PASS)
    print(f'{bcolors.FAIL}Reason: {error_message}{bcolors.ENDC}')


def footer_all_test(
        total_pass_test: int, total_test: int):
    print('{}{}Total pass test {} over {}!!{}'.format(
        bcolors.BOLD,
        bcolors.WARNING, total_pass_test,
        total_test, bcolors.ENDC))
    print("Deleting database dev")

