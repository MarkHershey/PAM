from pathlib import Path
import os
import json
from typing import Optional, Union, List, Tuple, Dict


TAKE_OUT_DIR = Path("/Users/markhuang/Downloads/Takeout")
assert TAKE_OUT_DIR.exists(), "Data directory (Google Takeout) does not exist."

LOCATION_HIST_DIR = TAKE_OUT_DIR / "Location History"
assert LOCATION_HIST_DIR.exists(), "Location history directory does not exist."

SEMANTIC_DIR = LOCATION_HIST_DIR / "Semantic Location History"
assert SEMANTIC_DIR.exists(), "Semantic location history directory does not exist."

RECORDS_FP = LOCATION_HIST_DIR / "Records.json"


def get_monthly_data():
    """Check if all files in semantic location history directory are json files."""
    year_dirs = []
    for year in os.listdir(SEMANTIC_DIR):
        year_dir = SEMANTIC_DIR / year
        if len(year) == 4 and year_dir.is_dir():
            year_dirs.append(year_dir)
    
    monthly_data_dict = {}
    for year_dir in year_dirs:
        for filename in os.listdir(year_dir):
            # filename eg. 2016_APRIL.json
            if not filename.endswith(".json"):
                continue
            # parse year
            year = filename.split("_")[0]
            assert year in str(year_dir)
            # parse month
            month = filename.split("_")[1][:-5]
            assert month in ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
                                "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"], \
                f"Month {month} is not valid."
            # convert month to number
            month = list(range(1, 13))[["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
                                "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"].index(month)]
            
            filepath = year_dir / filename
            assert filepath.exists(), f"File {filepath} does not exist."
            _key = f"{year}-{month:02d}"
            monthly_data_dict[_key] = str(filepath)
    
    return monthly_data_dict

def print_dict_keys(data, level=0, indent=4):
    if isinstance(data, dict):
        for key, value in data.items():
            print(' ' * level * indent + f"{key} ({type(value).__name__})")
            print_dict_keys(value, level + 1, indent)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            print(' ' * level * indent + f"[{index}] ({type(item).__name__})")
            print_dict_keys(item, level + 1, indent)


def check_unique_keys(data):
    def traverse_json(json_dict, parent=None, unique_keys=None, level=0):
        if unique_keys is None:
            unique_keys = {}

        for key, value in json_dict.items():
            if key not in unique_keys:
                if isinstance(value, dict):
                    child_data_type = "dict"
                elif isinstance(value, list):
                    child_data_type = "list"
                else:
                    child_data_type = type(value).__name__

                unique_keys[key] = {
                    "parent": parent,
                    "child_data_type": child_data_type,
                    "level": level
                }

            if isinstance(value, dict):
                traverse_json(value, key, unique_keys, level + 1)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        traverse_json(item, key, unique_keys, level + 1)

        return unique_keys

    # def print_unique_keys(unique_keys):
    #     max_key_len = max([len(key) for key in unique_keys.keys()] + [len("Key")])
    #     max_level_len = max([len(str(info["level"])) for info in unique_keys.values()] + [len("Level")])
    #     max_parent_len = max([len(info["parent"] if info["parent"] else "None") for info in unique_keys.values()] + [len("Parent")])
    #     max_child_data_type_len = max([len(info["child_data_type"] if info["child_data_type"] else "None") for info in unique_keys.values()] + [len("Child Data Type")])

    #     print(f"{'Key':<{max_key_len}} | {'Level':<{max_level_len}} | {'Parent':<{max_parent_len}} | {'Child Data Type':<{max_child_data_type_len}}")
    #     print("-" * (max_key_len + max_level_len + max_parent_len + max_child_data_type_len + 3 * 3))

    #     for key, info in unique_keys.items():
    #         print(f"{key:<{max_key_len}} | {info['level']:<{max_level_len}} | {(info['parent'] if info['parent'] else 'None'):<{max_parent_len}} | {(info['child_data_type'] if info['child_data_type'] else 'None'):<{max_child_data_type_len}}")

    def print_unique_keys(unique_keys):
        max_key_len = max([len(key) for key in unique_keys.keys()] + [len("Key")]) + 8
        max_level_len = max([len(str(info["level"])) for info in unique_keys.values()] + [len("Level")])
        max_parent_len = max([len(info["parent"] if info["parent"] else "None") for info in unique_keys.values()] + [len("Parent")])
        max_child_data_type_len = max([len(info["child_data_type"] if info["child_data_type"] else "None") for info in unique_keys.values()] + [len("Child Data Type")])

        print(f"{'Key':<{max_key_len}} | {'Level':<{max_level_len}} | {'Parent':<{max_parent_len}} | {'Child Data Type':<{max_child_data_type_len}}")
        print("-" * (max_key_len + max_level_len + max_parent_len + max_child_data_type_len + 3 * 3))

        for key, info in unique_keys.items():
            indentation = " " * 2 * info["level"]
            print(f"{indentation}{key:<{max_key_len - 2 * info['level']}} | {info['level']:<{max_level_len}} | {(info['parent'] if info['parent'] else 'None'):<{max_parent_len}} | {(info['child_data_type'] if info['child_data_type'] else 'None'):<{max_child_data_type_len}}")

    
    unique_keys = traverse_json(data)
    print_unique_keys(unique_keys)



def parse_monthly_data(monthly_data):
    assert isinstance(monthly_data, dict), "Monthly data should be a list at the top level."
    timelineObjects = monthly_data["timelineObjects"]
    placeVisits = []
    activitySegments = []
    for timeline_obj in timelineObjects:
        if "placeVisit" in timeline_obj:
            placeVisits.append(timeline_obj)
        elif "activitySegment" in timeline_obj:
            seg = parse_activitySegment(timeline_obj)
            activitySegments.append(seg)
        else:
            print(f"Unknown activity type: {timeline_obj.keys()}")
    
    print(json.dumps(activitySegments[0:10], indent=4))
    print(f"Found {len(activitySegments)} activity segments.")



def parse_placeVisit(placeVisit):
    ...

def parse_activitySegment(activitySegment: dict):
    """
    [301] (dict)
        activitySegment (dict)
            startLocation (dict)
                latitudeE7 (int)
                longitudeE7 (int)
                sourceInfo (dict)
                    deviceTag (int)
            endLocation (dict)
                latitudeE7 (int)
                longitudeE7 (int)
                sourceInfo (dict)
                    deviceTag (int)
            duration (dict)
                startTimestamp (str)
                endTimestamp (str)
            distance (int)
            activityType (str)
            confidence (str)
            activities (list)
                [0] (dict)
                    activityType (str)
                    probability (float)
                [1] (dict)
                    activityType (str)
                    probability (float)
                [2] (dict)
                    activityType (str)
                    probability (float)
                [3] (dict)
                    activityType (str)
                    probability (float)
                [4] (dict)
                    activityType (str)
                    probability (float)
                [5] (dict)
                    activityType (str)
                    probability (float)
                [6] (dict)
                    activityType (str)
                    probability (float)
                [7] (dict)
                    activityType (str)
                    probability (float)
                [8] (dict)
                    activityType (str)
                    probability (float)
                [9] (dict)
                    activityType (str)
                    probability (float)
                [10] (dict)
                    activityType (str)
                    probability (float)
                [11] (dict)
                    activityType (str)
                    probability (float)
                [12] (dict)
                    activityType (str)
                    probability (float)
                [13] (dict)
                    activityType (str)
                    probability (float)
                [14] (dict)
                    activityType (str)
                    probability (float)
            waypointPath (dict)
                waypoints (list)
                    [0] (dict)
                        latE7 (int)
                        lngE7 (int)
                    [1] (dict)
                        latE7 (int)
                        lngE7 (int)
                    [2] (dict)
                        latE7 (int)
                        lngE7 (int)
                source (str)
                distanceMeters (float)
                travelMode (str)
                confidence (float)
    """
    ...
    D = activitySegment["activitySegment"]
    startLat = int(D["startLocation"]["latitudeE7"]) / 1e7
    startLng = int(D["startLocation"]["longitudeE7"]) / 1e7
    endLat = int(D["endLocation"]["latitudeE7"]) / 1e7
    endLng = int(D["endLocation"]["longitudeE7"]) / 1e7

    try:
        waypoints = parse_waypoints(D["waypointPath"]["waypoints"])
    except KeyError:
        waypoints = []


    segment = dict(
        startLatLng = [startLat, startLng],
        endLatLng = [endLat, endLng],
        waypoints = waypoints,
        distance = D["distance"],
        activityType = D["activityType"],
        confidence = D["confidence"],
    )
    return(segment)

def parse_waypoints(waypoints: list):
    """
    [0] (dict)
        latE7 (int)
        lngE7 (int)
    [1] (dict)
        latE7 (int)
        lngE7 (int)
    [2] (dict)
        latE7 (int)
        lngE7 (int)
    """
    ...
    out = []
    for waypoint in waypoints:
        lat = int(waypoint["latE7"]) / 1e7
        lng = int(waypoint["lngE7"]) / 1e7
        out.append([lat, lng])
    return(out)


def del_key_from_dict(key, data_dict):
    for k in data_dict:
        if k == key:
            del data_dict[k]
    return data_dict

def simplify_master_records():
    keys_to_be_removed = [
        "activeWifiScan",
        "wifiScan",
    ]
    keys_to_keep =[
        "latitudeE7",
        "longitudeE7",
        "accuracy",
        "altitude",
        "verticalAccuracy",
        "formFactor",
        "source",
        "serverTimestamp",

    ]
    new_records_path = os.path.join(LOCATION_HIST_DIR, "Records_simplified.json")
    with RECORDS_FP.open("r") as f:
        records = json.load(f)
    
    locations = records["locations"]
    print(f"Found {len(locations)} locations.")

    new_locations = []

    for location in locations:
        new_location = {}
        for key in location:
            if key in keys_to_keep:
                new_location[key] = location[key]
        
        if "activity" in location:
            top1 = location["activity"][0 ]["activity"][0]["type"]
            new_location["activity"] = top1

        new_locations.append(new_location)

    with open(new_records_path, "w") as f:
        json.dump(new_locations, f, indent=4)
        print(f"Saved simplified records to {new_records_path}.")

    return new_records_path
    


def main():
    monthly_data_dict = get_monthly_data()
    sample = monthly_data_dict["2023-03"]
    sample = Path(sample)

    with sample.open("r") as f:
        records = json.load(f)
    

    # print_dict_keys(records)
    parse_monthly_data(records)

if __name__ == "__main__":
    main()