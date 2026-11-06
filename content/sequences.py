# content/sequences.py

SEQUENCES = [
    {
        "name": "RAMP_RIGHT",
        "display_name": "Right ramp",
        "targets": ["RAMP_RIGHT", "ORBIT_LEFT_REAR", "ORBIT_LEFT_FRONT"]
    },
    {
        "name": "ORBIT_SHORT",
        "display_name": "Speedtrap",
        "targets": ["ORBIT_LEFT_FRONT", "ORBIT_LEFT_REAR"]
    },
    {
        "name": "ORBIT_LONG",
        "display_name": "PARABOLICA",
        "targets": ["ORBIT_LEFT_FRONT", "ORBIT_LEFT_REAR", "ORBIT_RIGHT_REAR"]
   }
]