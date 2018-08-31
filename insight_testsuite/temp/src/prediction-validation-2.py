import sys
from predict_validate_class_2 import PredictValidate


def main():

    # grasp input output full path from command line arguments.
    input_window = sys.argv[1]
    input_actual = sys.argv[2]
    input_predict = sys.argv[3]
    output = sys.argv[4]
    debug = False

    # build an object, read and write.
    obj = PredictValidate(input_actual, input_predict, input_window, output, debug)
    obj.read_write()

    return 0


if __name__ == "__main__":
    main()
