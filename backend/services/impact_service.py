def calculate_impact(population_factor, connectivity_factor):
    population_affected = population_factor * 10

    if connectivity_factor >= 80:
        connectivity_status = "High connectivity risk"
    elif connectivity_factor >= 60:
        connectivity_status = "Moderate connectivity risk"
    else:
        connectivity_status = "Low connectivity risk"

    return {
        "population_affected": population_affected,
        "connectivity_status": connectivity_status
    }