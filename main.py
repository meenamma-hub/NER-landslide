import json

from priority import calculate_priority, get_action
from impact import calculate_impact
from roads import roads
from hospitals import get_nearest_hospitals


# -----------------------------------------
# 1. Load location data from data.json
# -----------------------------------------

with open("data.json", "r") as file:
    data = json.load(file)

locations = data["locations"]


# -----------------------------------------
# 2. Process every location
# -----------------------------------------

for location in locations:

    # -------------------------------------
    # 3. Calculate emergency priority
    # -------------------------------------

    priority_score, priority = calculate_priority(
        location["risk_score"],
        location["population_factor"],
        location["infrastructure_factor"],
        location["connectivity_factor"]
    )


    # -------------------------------------
    # 4. Calculate impact
    # -------------------------------------

    impact = calculate_impact(location)


    # -------------------------------------
    # 5. Get recommended emergency action
    # -------------------------------------

    action = get_action(priority)


    # -------------------------------------
    # 6. Find road information
    # -------------------------------------

    road_info = None

    for road in roads:

        if road["location"] == location["location"]:
            road_info = road
            break


    # -------------------------------------
    # 7. Get nearby hospitals
    # -------------------------------------

    nearby_hospitals = get_nearest_hospitals(
        location["location"],
        3
    )


    # -------------------------------------
    # 8. Create final JSON output
    # -------------------------------------

    result = {
        "location": location["location"],
        "state": location["state"],

        "risk_score": location["risk_score"],

        "priority_score": priority_score,
        "priority": priority,

        "population_affected": impact["population_affected"],

        "connectivity_status": impact["connectivity_status"],

        "recommended_action": action,

        "nearby_hospitals": nearby_hospitals
    }


    # -------------------------------------
    # 9. Add road information if available
    # -------------------------------------

    if road_info is not None:

        result["road"] = road_info["road"]

        result["road_blocked"] = road_info["blocked"]

        result["affected_villages"] = (
            road_info["affected_villages"]
        )

        result["alternative_route"] = (
            road_info["alternative_route"]
        )


    # -------------------------------------
    # 10. Display final JSON
    # -------------------------------------

    print("=" * 50)

    print(
        json.dumps(
            result,
            indent=4
        )
    )

    print("=" * 50)