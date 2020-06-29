import json
import os

import shapely.geometry

with open(os.path.join(os.path.dirname(__file__), "constants.json"), encoding="utf-8") as file:
    constants = json.load(file)

constants["mid_lane"] = shapely.geometry.Polygon(constants["mid_lane"])
constants["top_lane"] = shapely.geometry.Polygon(constants["top_lane"])
constants["bot_lane"] = shapely.geometry.Polygon(constants["bot_lane"])
constants["jungle_blue"] = shapely.geometry.Polygon(constants["jungle_blue"])
constants["jungle_red"] = shapely.geometry.Polygon(constants["jungle_red"])
