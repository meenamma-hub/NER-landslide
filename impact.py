def calculate_impact(location):

    population_affected = location["population_factor"] * 10

    connectivity = location["connectivity_factor"]

    if connectivity >= 80:
        connectivity_status = "High connectivity risk"

    elif connectivity >= 60:
        connectivity_status = "Moderate connectivity risk"

    else:
        connectivity_status = "Low connectivity risk"

    return {
        "population_affected": population_affected,
        "connectivity_status": connectivity_status
    }