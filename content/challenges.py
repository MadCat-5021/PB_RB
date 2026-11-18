CHALLENGES = [
    {
        "name": "PITSTOP_DASH",
        "display_name": "Pitstop Dash",
        "description": "Tire's are at the cliff, BOX BOX",
        "missions": ["MISSION_1"],
        "trigger": {
            "type": "target_hit_multiple",
            "target": "POP_1",
            "every": 50,
            "chance": 1.0,
        },
        "requirements": {
            "targets": [],
            "groups": ["TIRE"],
            "sequences": [],
        },
        "time_limit_seconds": 60,
        "score": 5000,
        "assets": {
            "image": None,
            "sound": None,
            "background_track": None,
        },
    },
    {
        "name": "RANDOM_TRACK_ATTACK",
        "display_name": "Track Attack",
        "description": "Raak de orbit vijf keer en voltooi de switchback.",
        "missions": [],
        "trigger": {
            "type": "random",
            "check_on": "target_hit",
            "chance": 0.05,
        },
        "requirements": {
            "targets": [{"name": "ORBIT_LEFT_REAR", "hits": 5}],
            "groups": [],
            "sequences": ["SWITCHBACK"],
        },
        "time_limit_seconds": None,
        "score": 50000,
        "assets": {
            "image": None,
            "sound": None,
            "background_track": None,
        },
    },
]