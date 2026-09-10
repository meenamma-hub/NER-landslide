def calculate_priority(
    risk_score,
    population_factor,
    infrastructure_factor,
    connectivity_factor
):
    priority_score = (
        risk_score * 0.4
        + population_factor * 0.2
        + infrastructure_factor * 0.2
        + connectivity_factor * 0.2
    )

    priority_score = round(priority_score)

    if priority_score >= 80:
        priority = "P1"
    elif priority_score >= 60:
        priority = "P2"
    else:
        priority = "P3"

    return priority_score, priority


def get_action(priority):
    if priority == "P1":
        return "Deploy response team immediately"
    elif priority == "P2":
        return "Urgent field inspection required"
    else:
        return "Continuous monitoring"