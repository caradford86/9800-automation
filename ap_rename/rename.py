__author__ = "Chris Radford"
__version__ = "0.0.1"
__status__ = "Alpha"

import argparse
import json
import sys
import csv


def load_aps(filename):
    try:
        with open(filename) as file:
            return json.load(file)
    except FileNotFoundError:
        print("could not find {}".format(filename))
    except ValueError:
        print("could not decode {} as json".format(filename))


def load_prefixes(filename):
    try:
        file = open(filename, newline="", encoding="utf-8-sig")
        data = csv.DictReader(file)

        prefixes = {}
        for row in data:
            prefixes[row["floorID"]] = row["apPrefix"]
        file.close()
        return prefixes
    except FileNotFoundError:
        print("could not find {}".format(filename))
    except ValueError:
        print("could not decode {} as json".format(filename))


def main(ap_file, mapping_file):
    access_points = load_aps(ap_file)
    prefixes = load_prefixes(mapping_file)

    ap_count = {}
    for floor in prefixes.keys():
        ap_count[floor] = 1

    for ap in access_points["accessPoints"]:
        floor = ap["location"]["floorPlanId"]
        ap_name = ap["name"]
        try:
            prefix = prefixes[floor]
            ap["name"] = "{}-{:02d}".format(prefix, ap_count[floor])
            # print(f"old: {ap_name} - new: {ap['name']}")
            ap_count[floor] = ap_count[floor] + 1
        except KeyError:
            print(f"Floor ID {floor} did not exist in prefix list for AP {ap_name}.")

    # write modified json to new file
    with open("accessPoints-resequenced.json", "w") as out:
        json.dump(access_points, out, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Renames and resequences Ekahau Site Surveys accessPoints.json.",
        epilog="Made with Python by {}".format(__author__),
    )

    parser.add_argument(
        "-a",
        "--aps",
        default="accessPoints.json",
        help="Specifies access points JSON file. Default: ./accessPoint.json",
    )
    parser.add_argument(
        "-f",
        "--floor_plan_mapping",
        default="floorPlanMapping.csv",
        help="Specifies floor plan ID -> Prefix mapping CSV file. Default: ./floorPlanMapping.csv",
    )
    parser.add_argument(
        "-V", "--version", action="version", version="%(prog)s {}".format(__version__)
    )

    args = parser.parse_args()
    main(args.aps, args.floor_plan_mapping)
