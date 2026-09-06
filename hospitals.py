hospitals = {
    "Tawang": [
        {
            "name": "Khan Drowa Zangmo District Hospital",
            "distance_km": 0
        },
        {
            "name": "Hospital 2",
            "distance_km": 0
        },
        {
            "name": "Hospital 3",
            "distance_km": 0
        }
    ],

    "Bomdila": [
        {
            "name": "General Hospital, Bomdila",
            "distance_km": 0
        },
        {
            "name": "Hospital 2",
            "distance_km": 0
        },
        {
            "name": "Hospital 3",
            "distance_km": 0
        }
    ],

    "Itanagar": [
        {
            "name": "Ramakrishna Mission Hospital",
            "distance_km": 0
        },
        {
            "name": "Heema Hospital",
            "distance_km": 0
        },
        {
            "name": "Niba Hospital",
            "distance_km": 0
        }
    ],

    "Aizawl": [
        {
            "name": "Civil Hospital, Aizawl",
            "distance_km": 0
        },
        {
            "name": "Kulikawn Hospital",
            "distance_km": 0
        },
        {
            "name": "State Referral Hospital, Falkawn",
            "distance_km": 0
        }
    ],

    "Churachandpur": [
        {
            "name": "District Hospital Churachandpur",
            "distance_km": 0
        },
        {
            "name": "Nazareth Hospital",
            "distance_km": 0
        },
        {
            "name": "Sielmat Hospital",
            "distance_km": 0
        }
    ],

    "Kohima": [
        {
            "name": "Naga Hospital Authority",
            "distance_km": 0
        },
        {
            "name": "Oking Hospital",
            "distance_km": 0
        },
        {
            "name": "Bethesda Hospital",
            "distance_km": 0
        }
    ],

    "Shillong": [
        {
            "name": "Civil Hospital Shillong",
            "distance_km": 0
        },
        {
            "name": "NEIGRIHMS",
            "distance_km": 0
        },
        {
            "name": "Ganesh Das Government MCH Hospital",
            "distance_km": 0
        }
    ],

    "Gangtok": [
        {
            "name": "STNM Hospital",
            "distance_km": 0
        },
        {
            "name": "Central Referral Hospital",
            "distance_km": 0
        },
        {
            "name": "Hospital 3",
            "distance_km": 0
        }
    ],

    "Haflong": [
        {
            "name": "Haflong Civil Hospital",
            "distance_km": 0
        },
        {
            "name": "Hospital 2",
            "distance_km": 0
        },
        {
            "name": "Hospital 3",
            "distance_km": 0
        }
    ],

    "Agartala": [
        {
            "name": "Hospital 1",
            "distance_km": 0
        },
        {
            "name": "Hospital 2",
            "distance_km": 0
        },
        {
            "name": "Hospital 3",
            "distance_km": 0
        }
    ]
}


def get_nearest_hospitals(location, count=3):
    location_hospitals = hospitals.get(location, [])

    sorted_hospitals = sorted(
        location_hospitals,
        key=lambda hospital: hospital["distance_km"]
    )

    return sorted_hospitals[:count]