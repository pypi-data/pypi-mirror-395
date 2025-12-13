import argparse
import json

from example.shape_parser import parse_shape

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shape Areas")
    parser.add_argument("--input", required=True)
    args, _ = parser.parse_known_args()
    with open(args.input, "r") as input_file:
        shape_dicts = json.load(input_file)
        for shape_dict in shape_dicts:
            shape = parse_shape(shape_dict)
            print(shape.get_area())
