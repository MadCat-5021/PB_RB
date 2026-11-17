# content/validator.py

from content.targets import TARGETS
from content.groups import GROUPS
from content.sequences import SEQUENCES
from content.missions import MISSIONS

def validate():
    target_names = {
        target["name"]
        for target in TARGETS
    }
    validate_groups(target_names)
    validate_sequences(target_names)
    validate_missions(
        target_names,
        {group["name"] for group in GROUPS},
        {sequence["name"] for sequence in SEQUENCES})
    print("Content validation successful")

def validate_groups(target_names):
    for group in GROUPS:
        for target in group["targets"]:
            if target not in target_names:
                raise ValueError(
                    f"Unknown target '{target}' "
                    f"in group '{group['name']}'"
                )

def validate_sequences(target_names):
    for sequence in SEQUENCES:
        for target in sequence["targets"]:
            if target not in target_names:
                raise ValueError(
                    f"Unknown target '{target}' "
                    f"in sequence '{sequence['name']}'"
                )

def validate_missions(target_names, group_names, sequence_names):
    if not MISSIONS:
        raise ValueError("At least one mission must be configured")

    known_requirements = {
        "targets": target_names,
        "groups": group_names,
        "sequences": sequence_names,
    }
    mission_names = set()
    for mission in MISSIONS:
        mission_name = mission["name"]
        if mission_name in mission_names:
            raise ValueError(f"Duplicate mission '{mission_name}'")
        mission_names.add(mission_name)

        if not any(mission["requirements"].values()):
            raise ValueError(
                f"Mission '{mission_name}' must have at least one requirement"
            )

        for requirement_type, requirement_names in mission[
            "requirements"
        ].items():
            if requirement_type not in known_requirements:
                raise ValueError(
                    f"Unknown requirement type '{requirement_type}' "
                    f"in mission '{mission_name}'"
                )
            for requirement_name in requirement_names:
                if requirement_name not in known_requirements[
                    requirement_type
                ]:
                    raise ValueError(
                        f"Unknown {requirement_type[:-1]} "
                        f"'{requirement_name}' in mission '{mission_name}'"
                    )
