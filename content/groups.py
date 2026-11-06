# content/groups.py

GROUPS = [
    {
        "name": "DRIVER",
        "display_name": "Threading the needle",
        "score": 2500,
        "targets": ["ESCAPE_LANE", "INLANE_LEFT", "INLANE_RIGHT", "OUTLANE_LEFT", "OUTLANE_RIGHT"]
    },
    {
        "name": "LANES",
        "display_name": "Lanes",
        "score": 2000,
        "targets": ["INLANE_LEFT", "INLANE_RIGHT", "OUTLANE_LEFT", "OUTLANE_RIGHT"]
    },
    {
        "name": "GATES",
        "display_name": "Events",
        "targets": ["GATE_1", "GATE_2", "GATE_3", "GATE_4"]
    },
    {
        "name": "DROP",
        "display_name": "breaking points",
        "score": 1500,
        "targets": ["DROP_1", "DROP_2", "DROP_3", "DROP_4"]
    },
    {
        "name": "TIRE",
        "display_name": "Pitstop",
        "score": 1250,
        "targets": ["TIRE_1", "TIRE_2", "TIRE_3", "TIRE_4"]
    }
]
