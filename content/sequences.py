# content/sequences.py

SEQUENCES = [
    {
         "name": "ORBIT_SHORT",
         "display_name": "Speedtrap",
         "score": 500,
         "targets": ["ORBIT_LEFT_FRONT", "ORBIT_LEFT_REAR"]
    },
    {
         "name": "ORBIT_LONG",
         "display_name": "PARABOLICA",
         "score": 1750,
         "targets": ["ORBIT_LEFT_FRONT", "ORBIT_LEFT_REAR", "ORBIT_RIGHT_REAR"]
    },
    {
        "name": "RAMP_LEFT",
        "display_name": "COTA, Climb that tower",
        "score": 2500,
        "targets": ["RAMP_LEFT", "ESCAPE_LANE"]
    },
    {
        "name": "RAMP_RIGHT",
        "display_name": "Right ramp",
        "score": 2500,
        "targets": ["RAMP_RIGHT", "ORBIT_LEFT_REAR", "ORBIT_LEFT_FRONT"]
    },
    {
        "name": "SWITCHBACK",
        "display_name": "Figure 8",
        "score": 2500,
        "targets": ["SWITCHBACK_ENTRY", "SWITCHBACK_EXIT"]
    }
]