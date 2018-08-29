class PredictValidate:
    """
    This is a class for calculating average error between predicted and actual stock prices.
    """

    def __init__(self, input_actual, input_predict, input_window, output, debug):
        """
        The constructor for PredictValidate class: To initialize a dictionary for saving all input data.

        Data structure Description:
        key:'stockID' ==>  value: nested_list[2][num_hour];
        nested_list[0,:] represents actual price for this stock at this hour;
        nested_list[1,:] represents predicted price for this stock at this hour.

        Parameters:
        :param input_actual: full path to input file actual.txt;
        :param input_predict: full path to input file predicted.txt;
        :param input_window: full path to input file window.txt;
        :param output: full path to output file comparison.txt.
        :param debug: bool for debug.
        """

        # Define data attributes.
        self.input_actual = input_actual
        self.input_predict = input_predict
        self.input_window = input_window
        self.output = output
        self.DEBUG = debug

        # Define several attributes for later use.
        self.start_hour = 1
        self.end_hour = 1
        self.num_hour = 1
        self.num_stock = 1
        self.window_size = 1
        self.data_structure = {}

        # Initialization.
        self._get_init()

    def _get_init(self):
        """
        The function to initialize dictionary.

        Assumption:
            actual.txt should start with a non-empty line with first field filled with integer.
            start_hour will read from line 0 in the file.
        """

        # 1st scan the actual.txt: obtain starting hour, ending hour, entire stock ID list.
        stock_id = []
        temp = []
        with open(self.input_actual, 'r') as f1:
            for i, this_line in enumerate(f1):
                temp = this_line.split('|')

                # check if there will be IndexError.
                if len(temp) < 2:
                    continue

                # check if temp[1] is empty. empty string will not fill into stock id.
                if not temp[1].strip():
                    continue

                # check if the time hour is in a valid format.
                try:
                    int(temp[0])
                except ValueError:
                    continue
                temp[0] = int(temp[0])  # for hour.

                # check if the stock id is in a valid format.
                try:
                    str(temp[1])
                except ValueError:
                    continue
                temp[1] = str(temp[1])  # for stock ID.

                # read in start_hour.
                if i == 0:
                    self.start_hour = temp[0]

                # read in all stock id.
                if temp[1] not in stock_id:
                    stock_id.append(temp[1])

        self.end_hour = temp[0]
        self.num_hour = self.end_hour - self.start_hour + 1
        self.num_stock = len(stock_id)

        # 1st scan the window.txt: obtain the window size.
        with open(self.input_window, 'r') as f2:
            for this_line in f2:
                self.window_size = int(this_line)

        # Initialize dictionary with all values setting to nested_list of NaN.
        for key in stock_id:
            self.data_structure[key] = []
            for i in range(2):
                self.data_structure[key].append([None]*self.num_hour)

        return self

    def _get_average_error_inside_window(self, window_start_index, window_end_index):
        """
        This is an object internal function, in order to calculate average error of all stocks in any given window

        Parameters:
        :param window_start_index: current start index in the nested list.
        :param window_end_index: current start index in the nested list.

        Returns:
        :return average_error: average error in this window.
        """

        temp_sum = 0.0
        temp_num = 0
        for value in self.data_structure.values():
            for i in range(window_start_index, window_end_index + 1):
                if value[0][i] is not None and value[1][i] is not None:
                    temp_sum += abs(value[0][i] - value[1][i])
                    temp_num += 1

        # case 1: there is no valid pair exist in this time window. return 'NA'.
        if temp_num == 0:
            average_error = 'NA'
        # case 2: there is some pairs valid, so we can give a float number as average error.
        else:
            average_error = temp_sum / temp_num

        return average_error

    def _read_single_stock_price_file(self, filename):

        """ The function to read in a single stock price input file. """

        # check which file to read. Can only use this function for two different kinds of file.
        if "actual" in filename:
            file_index = 0
            file_name = "actual.txt"
        elif "predict" in filename:
            file_index = 1
            file_name = 'predicted.txt'
        else:
            print('can not read in this file: ' + filename)
            return self

        # file reading into an pre-initialized dictionary.
        with open(filename, 'r') as f:
            for i, this_line in enumerate(f):
                temp = this_line.split('|')
                if len(temp) != 3:
                    print(file_name + ' line %d: read in an incomplete or over complete lines. '
                          'WILL ignore this whole line.' % (i + 1))
                    continue
                else:
                    # check if the time hour is in a valid format.
                    try:
                        int(temp[0])
                    except ValueError:
                        print(file_name + ' line %d: read in invalid time hour. '
                                          'WILL ignore this whole line.' % (i + 1))
                        continue
                    hour = int(temp[0])  # for hour.

                    # check if the stock id is in a valid format.
                    try:
                        str(temp[1])
                    except ValueError:
                        print(file_name + ' line %d: read in invalid stock id. '
                                          'WILL ignore this whole line.' % (i + 1))
                        continue
                    key = str(temp[1])  # for stock ID.

                    # check if the stock price is in a valid format.
                    try:
                        float(temp[2])
                    except ValueError:
                        print(file_name + ' line %d: read in invalid stock price. '
                              'WILL ignore this whole line.' % (i + 1))
                        continue
                    value = float(temp[2])  # for stock price.

                    # check if the read in file has new key type.
                    if key in self.data_structure.keys():

                        # check if the predicted.txt has valid hour provided, compare to actual.txt.
                        # hour read in validly should be inside (start_hour, end_hour)
                        if hour < self.start_hour or hour > self.end_hour:
                            print(file_name + ' line %d: read in invalid hour, this hour is not shown in actual.txt. '
                                              'WILL ignore this whole line.' % (i + 1))
                            continue
                        else:
                            self.data_structure[key][file_index][hour - self.start_hour] = value

                        # check what we read in.
                        if self.DEBUG:
                            print(self.data_structure.get(key))

                    # the file has new key type, probably from predicted.txt since keys are extract from actual.txt.
                    else:
                        print(file_name + ' line %d: read in new stock type from predicted.txt. '
                              'WILL ignore this whole line since there is no matched stock in actual.txt.' % (i + 1))
                        continue

        return self

    @staticmethod
    def _round_up(value, decimal_digits=2):
        """
        The function to round up floating point number based on ROUND_HALF criteria.

        For instance:
        round_up(1.995, 2) = 2.00
        round_up(1.994, 2) = 1.99

        Parameters:
        :param value: floating point number
        :param decimal_digits: target round off decimal.

        Returns:
        :return: rounded off numbers in string
        """

        result = str(value)

        # if entered value is '', return '' directly.
        if result != '':

            zero_count = decimal_digits  # number of zeros need to be added into value.
            decimal_index = result.find('.')  # index for the decimal dot '.'

            # case 1: there is decimal in entered value.
            if decimal_index > 0:

                zero_count = len(result[decimal_index + 1:])

                # case 1.1: given decimal digits in the value > required decimal digits
                if zero_count > decimal_digits:
                    # when the last effective digit is greater than 4, add 1 to the previous digit.
                    if int(result[decimal_index + decimal_digits + 1]) > 4:
                        result = str(value + pow(10, decimal_digits * -1))
                    # otherwise, just ignore the rest part of decimal digits.
                    decimal_index = result.find('.')
                    result = result[:decimal_index + decimal_digits + 1]
                    zero_count = 0

                # case 1.2: given decimal digits in the value <= required decimal digits
                else:
                    zero_count = decimal_digits - zero_count

            # case 2: there is no decimal in entered value, take it as integer.
            else:
                result += '.'

            # add necessary zeros into value.
            for i in range(zero_count):
                result += '0'

        return result

    def read_input(self):

        """ This is where the actual feeding-in-stock-price happens. """

        # 2nd scan the actual.txt: read in actual stock price to nested_list[0][:]
        self._read_single_stock_price_file(self.input_actual)

        # 1st scan the predict.txt: read in predicted stock price to nested_list[1][:]
        self._read_single_stock_price_file(self.input_predict)

        return self

    def write_output(self):

        """ This is where we calculate and output the comparison results. """

        # open file to write.
        f_output = open(self.output, 'w')

        # 1st scenario: window size is greater or equal than the actual number of hours.
        if self.window_size >= self.num_hour:
            average_error = self._get_average_error_inside_window(0, self.num_hour - 1)

            # case 1: there is no valid pair exist in this time window. return 'NA'.
            if isinstance(average_error, str):
                string = str(self.start_hour) + '|' + str(self.end_hour) + '|' + \
                         average_error + '\n'

            # case 2: there is some pairs valid, so we can give a float number as average error.
            else:
                string = str(self.start_hour) + '|' + str(self.end_hour) + '|' + \
                    self._round_up(average_error) + '\n'

            # check the string in debug mode.
            if self.DEBUG:
                print(string)

            # write one line output into file.
            f_output.write(string)

        # 2nd scenario: window size is smaller than the actual number of hours.
        else:
            k = 0
            while k + self.window_size - 1 <= self.num_hour - 1:
                average_error = self._get_average_error_inside_window(k, k + self.window_size - 1)

                # case 1: there is no valid pair exist in this time window. return 'NA'.
                if isinstance(average_error, str):
                    string = str(self.start_hour + k) + '|' + str(self.start_hour + k + self.window_size - 1) + '|' + \
                        average_error + '\n'

                # case 2: there is some pairs valid, so we can give a float number as average error.
                else:
                    string = str(self.start_hour + k) + '|' + str(self.start_hour + k + self.window_size - 1) + '|' + \
                        self._round_up(average_error) + '\n'

                # check the string in debug mode.
                if self.DEBUG:
                    print(string)

                # write one line output into file.
                f_output.write(string)

                k += 1

        # close file.
        f_output.close()

        return self


def test_single(path, test_path):

    """ The function to run a single test case. """

    # define input output file path.
    input_window = path + test_path + 'input/window.txt'
    input_actual = path + test_path + 'input/actual.txt'
    input_predict = path + test_path + 'input/predicted.txt'
    output_model = path + test_path + 'output/comparison_model.txt'
    output_truth = path + test_path + 'output/comparison.txt'
    debug = False

    # read and write output file.
    obj = PredictValidate(input_actual, input_predict, input_window, output_model, debug)
    obj.read_input()
    obj.write_output()

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

    blue = '\033[94m'
    bold = '\033[1m'
    path = '../insight_testsuite/tests/'

    # run test_1, have round off error. add tolerance.
    test_path = 'test_1/'
    print(blue + bold + test_path[:-1] + ' is a given basic test case.')
    test_single(path, test_path)

    # run test_2
    test_path = 'test_2/'
    print(blue + bold + test_path[:-1] + ' is a shorter basic test case.')
    test_single(path, test_path)

    # run test_3
    test_path = 'test_3/'
    print(blue + bold + test_path[:-1] + ' is a given demo case with variations on window size.')
    test_single(path, test_path)

    # run test_4
    test_path = 'test_4/'
    print(blue + bold + test_path[:-1] + ' is a given demo test case with ugly input data.')
    test_single(path, test_path)

    # run test_5
    test_path = 'test_5/'
    print(blue + bold + test_path[:-1] + ' is a given demo test case.')
    test_single(path, test_path)

    return 0


if __name__ == "__main__":
    test_all()
