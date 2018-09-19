from collections import deque


class PredictValidate:
    """
    This is a class for calculating average error between predicted and actual stock prices.
    """

    def __init__(self, input_actual, input_predict, input_window, output, debug):
        """
        The constructor for PredictValidate class: To initialize a dictionary for saving input data in current window.

        Data structure Description:
        key:'stockID' ==>  value: deque[2][window_size];
        deque[0,:] represents actual price for this stock at this hour;
        deque[1,:] represents predicted price for this stock at this hour.

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
        self.window_start_hour = 0
        self.window_end_hour = 0
        self.gap_line = [None, None]
        self.gap_diff = [None, None]  # it should at least be 1.
        # self.num_hour = 1
        # self.num_stock = 1
        self.window_size = 0
        self.data_structure = {}
        self.window_flag_1 = True  # control the end of actual.txt, exit all loops.
        self.window_flag_2 = True  # control the end of predicted.txt, exit all loops.

        # reassign start window hour, window size, end window hour.
        self._get_init()

    @staticmethod
    def conformity_check(line):
        """
        The function to check if it's a valid three field line with integer|string|float

        Parameter:
        :param line: the current string being checked.

        Return:
        bool: status whether this line is valid (True), or invalid (False)
        temp: the actual separated fields, contains: [hour, stock id, stock price].
        """

        temp = line.split('|')

        # check the length of line. In case there will be IndexError.
        if len(temp) != 3:
            return False

        # check if the time hour is in a valid format.
        try:
            temp[0] = int(temp[0])
        except ValueError:
            return False

        # check if the stock id is in a valid format.
        try:
            if str(temp[1]).strip() == '':
                return False
            else:
                temp[1] = str(temp[1])
        except ValueError:
            return False

        # check if the stock price is in a valid format.
        try:
            temp[2] = float(temp[2])
        except ValueError:
            return False

        return True, temp

    def _get_init(self):

        """ The function to initialize start_hour and window_size. """

        # Obtain window_start_hour: read the first valid line of the file
        with open(self.input_actual, 'r') as f:
            while True:
                line = f.readline()
                # end-all-loop condition: read till end of file. can't find a valid line in the file.
                if line == '':
                    self.in_window_flag = False
                    break
                # check if the line contains start hour info or not.
                status = self.conformity_check(line)
                if len(status) > 1:  # if status is False, len(status)==1
                    self.window_start_hour = status[1][0]
                    break
                else:  # keep seeking the next valid line, till we find a valid line.
                    continue

        # Obtain window_size: read the first valid line of the file
        with open(self.input_window, 'r') as f:
            while True:
                line = f.readline()
                # end-all-loop condition: read till end of file. can't find a valid line in the file.
                if line == '':
                    self.in_window_flag = False
                    break
                # check if the line contains window info or not.
                try:
                    self.window_size = int(line)
                    # end-all-loop condition: not a valid time window input.
                    if self.window_size <= 0:
                        self.in_window_flag = False
                    break
                except ValueError:
                    continue

        # Calculate window_end_hour
        self.window_end_hour = self.window_size + self.window_start_hour - 1

        return self



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

    def read_one_window(self, f_handle, predict_flag):
        # read in one window data from actual.txt or predicted.txt
        while True:
            # read in one whole line.
            line = f_handle.readline()
            # if the file reached to the end, break and set flag.
            if line == '':
                # 0 means actual.txt
                if predict_flag == 0:
                    self.window_flag_1 = False
                # 1 means predicted.txt
                elif predict_flag == 1:
                    self.window_flag_2 = False
                # other cases not implemented yet.
                else:
                    pass
                break
            # check this whole line's conformity.
            status = self.conformity_check(line)
            # status is False.
            if len(status) == 1:
                # continue to read next line in the file.
                continue
            # status if True.
            else:
                # case 1: this line is inside the time window.
                if self.window_start_hour <= status[1][0] <= self.window_end_hour:
                    # a. key is not in dic yet. ==> initialize the dictionary value.
                    if status[1][1] not in self.data_structure.keys():
                        self.data_structure[status[1][1]] = [[None]*self.window_size, [None]*self.window_size]
                    # b. key is in the dic.
                    else:
                        pass
                    temp_index = status[1][0] - self.window_start_hour
                    self.data_structure[status[1][1]][predict_flag][temp_index] = status[1][2]
                # case 2: this line greater than the time window. ==> outside of current window, need to shift window.
                elif status[1][0] > self.window_end_hour:
                    self.gap_line[predict_flag] = status[1]
                    self.gap_diff[predict_flag] = status[1][0] - self.window_end_hour
                    break
                # case 3: this line is smaller than time window, happened when actual has bigger hour gap than predict.
                else:
                    continue
        return self

    def average_error_window(self):
        """
        This is an object internal function, in order to calculate average error of all stocks in any given window
        """

        # based on actual.txt self.gap_diff[0], initialize how many output lines we can write.
        length = self.gap_diff[0]  # has to be >= 1
        average_error = [None]*length

        for i in range(length):
            temp_sum = 0.0
            temp_num = 0

            # calculate i-pop-out window-size average error
            for key in self.data_structure.keys():
                if i > 0:
                    self.data_structure[key][0].pop(0)
                    self.data_structure[key][0].append(None)
                    self.data_structure[key][1].pop(0)
                    self.data_structure[key][1].append(None)
                temp_1 = self.data_structure[key][0]
                temp_2 = self.data_structure[key][1]
                # here, both length are supposed to be the same.
                for j in range(min(len(temp_1), len(temp_2))):
                    if temp_1[j] is not None and temp_2[j] is not None:
                        temp_sum += abs(temp_1[j] - temp_2[j])
                        temp_num += 1

            # case 1: there is no valid pair exist in this time window. return 'NA'.
            if temp_num == 0:
                average_error[i] = 'NA'
            # case 2: there is some pairs valid, so we can give a float number as average error.
            else:
                average_error[i] = temp_sum / temp_num

        return average_error

    def write_window(self, f_handle, average_error):

        for i in range(len(average_error)):
            # case 1: there is no valid pair exist in this time window. return 'NA'.
            if isinstance(average_error[i], str):
                string = str(self.window_start_hour) + '|' + str(self.window_end_hour) + '|' + \
                         average_error[i] + '\n'
            # case 2: there is some pairs valid, so we can give a float number as average error.
            else:
                string = str(self.window_start_hour + i) + '|' + str(self.window_end_hour + i) + '|' + \
                         '{:.2f}'.format(average_error[i]) + '\n'
            # check the string in debug mode.
            if self.DEBUG:
                print(string)
            # write one line output into file.
            f_handle.write(string)

        return self

    def read_write(self):
        """
        :return:
        """
        f_output = open(self.output, 'w')
        with open(self.input_actual, 'r') as f1, open(self.input_predict, 'r') as f2:
            while True:

                # read in one-window-size data from actual.txt
                self.read_one_window(f1, 0)

                # read in one-window-size data from predicted.txt
                self.read_one_window(f2, 1)

                # calculate average error in current window.
                average_error = self.average_error_window()

                # write into output file
                self.write_window(f_output, average_error)

                # stop condition for this loop.
                if not self.window_flag_1:
                    break

                # update window_start_hour and window_end_hour
                self.window_end_hour += self.gap_diff[0]
                self.window_start_hour = self.window_end_hour - self.window_size + 1

                # recover to process the current two line.
                if self.window_start_hour <= self.gap_line[0][0] <= self.window_end_hour:
                    temp_index = self.gap_line[0][0] - self.window_start_hour
                    self.data_structure[self.gap_line[0][1]][0][temp_index] = self.gap_line[0][2]
                else:
                    continue
                if self.window_start_hour <= self.gap_line[1][0] <= self.window_end_hour:
                    temp_index = self.gap_line[1][0] - self.window_start_hour
                    self.data_structure[self.gap_line[1][1]][1][temp_index] = self.gap_line[1][2]
                else:
                    continue
        f_output.close()

        return self
