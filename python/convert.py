import json
import os
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent


def points():
    OBJ_NAME = "PointsData"
    OUTFILE = f"{OBJ_NAME}.ts"

    with open("data/Singapore.json") as f:
        data = json.load(f)

    for idx, sample in data.items():
        obj = []
        for point in sample:
            lat, lng = point["lat"], point["lng"]
            obj.append([lat, lng])

        obj_str = json.dumps(obj)

        long_string = """import { LatLngExpression } from "leaflet";\n\n"""
        long_string = (
            long_string
            + f"""export const {OBJ_NAME}: LatLngExpression[] = {obj_str};"""
        )

        with open(OUTFILE, "w") as f:
            f.write(long_string)

        return


def routes():
    data_dir = project_root / "python/data"
    routes_dir: Path = project_root / "map-app/src/assets/routes"
    routes_dir.mkdir(exist_ok=True)

    file_counter = 0

    for filename in os.listdir(data_dir):
        long_string = """import { LatLngExpression } from "leaflet";\n\n"""

        if not filename.startswith("routes_"):
            continue

        file_counter += 1
        area = filename[:-5].split()[0]
        area = area[7:]
        area = area.strip(",")

        routefile = data_dir / filename
        outfile = routes_dir / f"Routes{area}.ts"

        with open(routefile, "r") as f:
            data = json.load(f)

        for idx, sample in enumerate(data):
            OBJ_NAME = f"multiPolyline{idx}"
            coords = sample["coordinates"]
            obj_str = json.dumps(coords)
            long_string += (
                f"export const {OBJ_NAME}: LatLngExpression[][] = {obj_str};\n\n"
            )

        with open(outfile, "w") as f:
            f.write(long_string)
            print("Saved routes to", outfile)


def convert_routes2():
    ROOT_DIR = Path(__file__).resolve().parent.parent

    PROCESSED_TL_DIR = ROOT_DIR / "python" / "processed_tl"

    files = [
        "routes_commute.json",
        "routes_walk.json",
        "routes_drive.json",
    ]

    data_dir = project_root / "python/data"
    routes_dir: Path = project_root / "map-app/src/assets/routes"
    routes_dir.mkdir(exist_ok=True)


    for filename in files:
        long_string = """import { LatLngExpression } from "leaflet";\n\n"""


        mode = filename[:-5].split("_")[1]
        # capitalize first letter
        mode = mode[0].upper() + mode[1:]


        routefile = PROCESSED_TL_DIR / filename
        outfile = routes_dir / f"Routes{mode}.ts"

        with open(routefile, "r") as f:
            data = json.load(f)

        for idx, sample in enumerate(data):
            OBJ_NAME = f"multiPolyline{idx}"
            coords = sample["coordinates"]
            obj_str = json.dumps(coords)
            long_string += (
                f"export const {OBJ_NAME}: LatLngExpression[][] = {obj_str};\n\n"
            )

        with open(outfile, "w") as f:
            f.write(long_string)
            print("Saved routes to", outfile)

def convert_routes3():
    ROOT_DIR = Path(__file__).resolve().parent.parent

    PROCESSED_TL_DIR = ROOT_DIR / "python" / "processed_tl"

    files = [
        "routes_commute.json",
        "routes_walk.json",
        "routes_drive.json",
    ]

    data_dir = project_root / "python/data"
    routes_dir: Path = project_root / "map-app/src/assets/routes"
    routes_dir.mkdir(exist_ok=True)


    for filename in files:
        long_string = """import { LatLngExpression } from "leaflet";\n\n"""


        mode = filename[:-5].split("_")[1]
        # capitalize first letter
        mode = mode[0].upper() + mode[1:]


        routefile = PROCESSED_TL_DIR / filename
        outfile = routes_dir / f"Routes{mode}.ts"

        with open(routefile, "r") as f:
            data = json.load(f)
        
        all_routes = []

        for idx, sample in enumerate(data):
            coords = sample["coordinates"]
            all_routes.append(coords)
        
        obj_str = json.dumps(all_routes)

        long_string += (
            f"export const Routes{mode}: LatLngExpression[][][] = {obj_str};\n\n"
        )

        with open(outfile, "w") as f:
            f.write(long_string)
            print("Saved routes to", outfile)

if __name__ == "__main__":
    # routes()
    # points()
    convert_routes3()
    ...
