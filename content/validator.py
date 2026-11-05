# content/validator.py

from content.targets import TARGETS
from content.groups import GROUPS
from content.sequences import SEQUENCES

def validate():
    target_names = {
        target["name"]
        for target in TARGETS
    }
    validate_groups(target_names)
    validate_sequences(target_names)
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
