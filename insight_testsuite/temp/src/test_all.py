from predict_validate_class_2 import PredictValidate


def test_single(path, test_path):

    """ The function to run a single test case. """

    # define input output file path.
    input_window = path + test_path + 'input/window.txt'
    input_actual = path + test_path + 'input/actual.txt'
    input_predict = path + test_path + 'input/predicted.txt'
    output_model = path + test_path + 'output/comparison_model.txt'
    output_truth = path + test_path + 'output/comparison.txt'
    debug = True

    # read and write output file.
    obj = PredictValidate(input_actual, input_predict, input_window, output_model, debug)
    obj.read_write()

    # check solution.
    red = '\033[91m'
    green = '\033[92m'
    blue = '\033[94m'
    bold = '\033[1m'
    return_flag = True

    with open(output_model, 'r') as f1, open(output_truth, 'r') as f2:
        model = f1.readlines()
        truth = f2.readlines()

    if model != truth:
        if len(model) != len(truth):
            return_flag = False
            print(red + bold + 'could not match length of both files in comparison.')
        else:
            for k in range(len(model)):
                if model[k] != truth[k]:
                    temp_model = model[k].split('|')
                    temp_truth = truth[k].split('|')
                    # try to convert the average error type to float, consider NA case.
                    try:
                        float(temp_model[2])
                        temp_model_float_type = True
                    except ValueError:
                        temp_model_float_type = False
                    try:
                        float(temp_truth[2])
                        temp_truth_float_type = True
                    except ValueError:
                        temp_truth_float_type = False
                    # start inspect on where is unmatched.
                    if temp_model[0] != temp_truth[0] or temp_model[1] != temp_truth[1]:
                        return_flag = False
                        print(red + bold + 'line %d: could not match time start and end window.' % k)
                        break
                    if temp_model[2] != temp_truth[2]:
                        if temp_model_float_type != temp_truth_float_type:
                            return_flag = False
                            print(red + bold + 'line %d: could not match even average error type: '
                                               'one is NA, one is float.' % k)
                            break
                        # if type is the same, they should be both float numbers, if both string, then both == NA.
                        else:
                            # only 2 decimal digits, the tolerance is within 0.01.
                            if abs(float(temp_model[2])-float(temp_truth[2])) >= 0.02:
                                return_flag = False
                                print(red + bold + 'line %d: average error is incorrect, regardless of computational '
                                      'round off error.' % k)
                                break

    # assert check results.
    if return_flag:
        print(blue + bold + "Test" + test_path[5:-1] + ": " + bold + green + "PASS")
    else:
        print(blue + bold + "Test" + test_path[5:-1] + ": " + bold + red + "FAIL")

    return 1


def test_all():

    """ The function to run all test cases. """

    from datetime import datetime

    blue = '\033[94m'
    bold = '\033[1m'
    path = '../insight_testsuite/tests/'

    # run test_1, have round off error. add tolerance.
    test_path = 'test_1/'
    print(blue + bold + test_path[:-1] + ' is a given basic test case.')
    start = datetime.now()
    test_single(path, test_path)
    print datetime.now()-start, " seconds"

    # run test_2
    test_path = 'test_2/'
    print(blue + bold + test_path[:-1] + ' is a shorter basic test case.')
    start = datetime.now()
    test_single(path, test_path)
    print datetime.now() - start, " seconds"

    # run test_3
    test_path = 'test_3/'
    print(blue + bold + test_path[:-1] + ' is a given demo case with variations on window size.')
    start = datetime.now()
    test_single(path, test_path)
    print datetime.now() - start, " seconds"

    # run test_4
    test_path = 'test_4/'
    print(blue + bold + test_path[:-1] + ' is a given demo test case with ugly input data.')
    start = datetime.now()
    test_single(path, test_path)
    print datetime.now() - start, " seconds"

    # run test_5
    test_path = 'test_5/'
    print(blue + bold + test_path[:-1] + ' is a given demo test case.')
    start = datetime.now()
    test_single(path, test_path)
    print datetime.now() - start, " seconds"

    # run test_6
    test_path = 'test_6/'
    print(blue + bold + test_path[:-1] + ' is a given demo test case.')
    start = datetime.now()
    test_single(path, test_path)
    print datetime.now() - start, " seconds"

    return 0


if __name__ == "__main__":
    test_all()
