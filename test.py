from test import *


if __name__ == '__main__':

    start_all_test()

    pass_test = 0
    number_test = 1

    for test_ in DEFINED_TEST:
        header_test(number_test, test_)
        number_test += 1

        try:
            result_test = eval(test_)()
            print(TEST_PASS)
            pass_test += 1
        except Exception as e:
            no_pass_test(e)

        print('----------\n\n')

    footer_all_test(pass_test, len(DEFINED_TEST))

