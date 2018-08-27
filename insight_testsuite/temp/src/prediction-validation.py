
class PredictValidate:

    def __init__(self, input_actual, input_predict, input_window, output, debug):

        """
        Initializing a dictionary for saving all input data, the dict format is as follows:

        key:'stockID' ==>  value: nested_list[2][num_hour];
        nested_list[0,:] represents actual price for this stock at this hour;
        nested_list[1,:] represents predicted price for this stock at this hour.

        :param input_actual: full path to input file actual.txt;
        :param input_predict: full path to input file predicted.txt;
        :param input_window: full path to input file window.txt;
        :param output: full path to output file comparison.txt.
        """

        # Define data attributes.
        self.input_actual = input_actual
        self.input_predict = input_predict
        self.input_window = input_window
        self.output = output
        self.DEBUG = debug

        # Define several attributes for later use.
        self.start_hour = None
        self.end_hour = None
        self.num_hour = None
        self.num_stock = None
        self.window_size = None
        self.data_structure = {}

        # Initialization.
        self._get_init()

    def _get_init(self):

        """
        This is where the actual initialization happens.
        :return: self
        """

        # 1st scan the actual.txt: obtain starting hour, ending hour, entire stock ID list.
        stock_id = []
        temp = []
        with open(self.input_actual, 'r') as f1:
            for i, this_line in enumerate(f1):
                temp = this_line.split('|')
                temp[0] = int(temp[0])  # for hour.
                temp[1] = str(temp[1])  # for stock ID.
                if i == 0:
                    self.start_hour = temp[0]
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

    def read_input(self):

        """
        This is where the actual feeding-in-stock-price happens.
        :return: self
        """

        # 2nd scan the actual.txt: read in actual stock price to nested_list[0][:]
        with open(self.input_actual, 'r') as f3:
            for i, this_line in enumerate(f3):
                temp = this_line.split('|')
                hour = int(temp[0])  # for hour.
                key = str(temp[1])  # for stock ID.
                value = float(temp[2])  # for stock price.
                self.data_structure[key][0][hour - self.start_hour] = value
                if self.DEBUG:
                    print self.data_structure.get(key)

        # 1st scan the predict.txt: read in predicted stock price to nested_list[1][:]
        with open(self.input_predict, 'r') as f4:
            for i, this_line in enumerate(f4):
                temp = this_line.split('|')
                hour = int(temp[0])  # for hour.
                key = str(temp[1])  # for stock ID.
                value = float(temp[2])  # for stock price.
                self.data_structure[key][1][hour - self.start_hour] = value
                if self.DEBUG:
                    print self.data_structure.get(key)

        return self

    def write_output(self):

        """
        This is where we calculate and output the comparison results.
        :return: self
        """

        # open file to write.
        f_output = open(self.output, 'w')

        # 1st scenario: window size is greater or equal than the actual number of hours.
        if self.window_size >= self.num_hour:
            average_error = self._get_average_error_inside_window(0, self.num_hour - 1)
            string = str(self.start_hour) + '|' + str(self.start_hour + self.window_size - 1) + '|' + \
                '{:.2f}'.format(average_error)+'\n'
            if self.DEBUG:
                print string
            f_output.write(string)

        # 2nd scenario: window size is smaller than the actual number of hours.
        else:
            k = 0
            while k + self.window_size - 1 <= self.num_hour - 1:
                average_error = self._get_average_error_inside_window(k, k + self.window_size - 1)
                string = str(self.start_hour + k) + '|' + str(self.start_hour + k + self.window_size - 1) + '|' + \
                    '{:.2f}'.format(average_error) + '\n'
                if self.DEBUG:
                    print string
                f_output.write(string)
                k += 1

        # close file.
        f_output.close()

        return self

    def _get_average_error_inside_window(self, window_start_index, window_end_index):
        """
        This is an object internal function, in order to calculate average error of all stocks in any given window
        :param window_start_index:
        :param window_end_index:
        :return:
        """

        temp_sum = 0.0
        temp_num = 0
        for value in self.data_structure.itervalues():
            for i in range(window_start_index, window_end_index + 1):
                if value[0][i] is not None and value[1][i] is not None:
                    temp_sum += abs(value[0][i] - value[1][i])
                    temp_num += 1
        average_error = temp_sum / temp_num

        return average_error


def main():

    # grasp input output full path from command line arguments.
    input_actual = "../input/actual.txt"
    input_predict = "../input/predicted.txt"
    input_window = "../input/window.txt"
    output = "../output/comparison.txt"
    debug = True

    # build an object.
    obj = PredictValidate(input_actual, input_predict, input_window, output, debug)

    # read and write.
    obj.read_input()
    obj.write_output()

    return 0


if __name__ == "__main__":
    main()