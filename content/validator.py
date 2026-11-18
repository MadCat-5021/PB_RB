# content/validator.py

from content.targets import TARGETS
from content.groups import GROUPS
from content.sequences import SEQUENCES
from content.missions import MISSIONS
from content.challenges import CHALLENGES

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
    validate_challenges(
        target_names,
        {group["name"] for group in GROUPS},
        {sequence["name"] for sequence in SEQUENCES},
        {mission["name"] for mission in MISSIONS})
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

def validate_challenges(
    target_names,
    group_names,
    sequence_names,
    mission_names
):
    known_requirements = {
        "targets": target_names,
        "groups": group_names,
        "sequences": sequence_names,
    }
    challenge_names = set()
    for challenge in CHALLENGES:
        challenge_name = challenge["name"]
        if challenge_name in challenge_names:
            raise ValueError(f"Duplicate challenge '{challenge_name}'")
        challenge_names.add(challenge_name)

        if challenge["score"] < 0:
            raise ValueError(
                f"Challenge '{challenge_name}' cannot have a negative score"
            )
        time_limit = challenge["time_limit_seconds"]
        if time_limit is not None and time_limit <= 0:
            raise ValueError(
                f"Challenge '{challenge_name}' must have a positive "
                "time limit or None"
            )

        for mission_name in challenge["missions"]:
            if mission_name not in mission_names:
                raise ValueError(
                    f"Unknown mission '{mission_name}' "
                    f"in challenge '{challenge_name}'"
                )

        trigger = challenge["trigger"]
        if trigger["type"] == "target_hit_multiple":
            target_name = trigger["target"]
            if target_name not in target_names:
                raise ValueError(
                    f"Unknown target '{target_name}' "
                    f"in challenge trigger '{challenge_name}'"
                )
            if trigger["every"] < 1:
                raise ValueError(
                    f"Challenge '{challenge_name}' trigger interval "
                    "must be at least 1"
                )
            if not 0 <= trigger["chance"] <= 1:
                raise ValueError(
                    f"Challenge '{challenge_name}' trigger chance "
                    "must be between 0 and 1"
                )
        elif trigger["type"] == "random":
            if trigger["check_on"] != "target_hit":
                raise ValueError(
                    f"Unsupported random trigger event in "
                    f"challenge '{challenge_name}'"
                )
            if not 0 <= trigger["chance"] <= 1:
                raise ValueError(
                    f"Challenge '{challenge_name}' trigger chance "
                    "must be between 0 and 1"
                )
        else:
            raise ValueError(
                f"Unknown trigger type '{trigger['type']}' "
                f"in challenge '{challenge_name}'"
            )

        requirements = challenge["requirements"]
        target_chain = challenge.get("target_chain", [])
        if not any(requirements.values()) and not target_chain:
            raise ValueError(
                f"Challenge '{challenge_name}' must have at least one "
                "requirement"
            )
        for target_name in target_chain:
            if target_name not in target_names:
                raise ValueError(
                    f"Unknown target '{target_name}' "
                    f"in challenge chain '{challenge_name}'"
                )
        if target_chain and challenge["time_bonus_per_hit"] < 0:
            raise ValueError(
                f"Challenge '{challenge_name}' time bonus "
                "cannot be negative"
            )
        for requirement_type, requirement_values in requirements.items():
            if requirement_type not in known_requirements:
                raise ValueError(
                    f"Unknown requirement type '{requirement_type}' "
                    f"in challenge '{challenge_name}'"
                )
            if requirement_type == "targets":
                target_requirements = (
                    requirement
                    if isinstance(requirement, dict)
                    else {"name": requirement, "hits": 1}
                    for requirement in requirement_values
                )
                for requirement in target_requirements:
                    target_name = requirement["name"]
                    if target_name not in target_names:
                        raise ValueError(
                            f"Unknown target '{target_name}' "
                            f"in challenge '{challenge_name}'"
                        )
                    if requirement["hits"] < 1:
                        raise ValueError(
                            f"Target hit requirement in challenge "
                            f"'{challenge_name}' must be at least 1"
                        )
            else:
                for requirement_name in requirement_values:
                    if requirement_name not in known_requirements[
                        requirement_type
                    ]:
                        raise ValueError(
                            f"Unknown {requirement_type[:-1]} "
                            f"'{requirement_name}' in challenge "
                            f"'{challenge_name}'"
                        )
