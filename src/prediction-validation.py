import sys
from predic_validate_class import PredictValidate


def main():

    # grasp input output full path from command line arguments.
    input_window = sys.argv[1]
    input_actual = sys.argv[2]
    input_predict = sys.argv[3]
    output = sys.argv[4]
    debug = False

    # build an object.
    obj = PredictValidate(input_actual, input_predict, input_window, output, debug)

    # read and write.
    obj.read_input()
    obj.write_output()

    return 0


if __name__ == "__main__":
    main()
