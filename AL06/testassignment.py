"""Unfinished generic test prompts for whichever AL06 application you choose."""

from copy import deepcopy
from Main import CHOICE, recursive_total, iterative_total
from scenario_data import SCENARIOS, make_entry, make_group


def assignment_checks():
    """Check selected totals, boundary/nested cases, invalid data, and preservation."""
    scenario = SCENARIOS[CHOICE]
    included_status = scenario["included_status"]

    # Helper function to check totals for a given node against an expected value.
    def check_totals(node, expected):
        # Preserve the original node to ensure the total functions do not modify it.
        original = deepcopy(node)
        # Check the totals using both recursive and iterative functions.
        assert recursive_total(node, included_status) == expected
        # Ensure the node remains unchanged after the recursive total check.
        assert node == original, "recursive_total changed the input"
        # Ensure the node remains unchanged after the iterative total check as well.
        assert iterative_total(node, included_status) == expected
        # If the iterative total check fails, the assertion will indicate which function caused it.
        assert node == original, "iterative_total changed the input"

    # Fundraiser total: 25 + 40 + 15 received dollars.
    check_totals(scenario["data"], 80)

    # Included and excluded entries have the same amount, so status controls selection.
    check_totals(make_entry("Received", 12, "received"), 12)
    # Boundary case: zero amount with included status.
    check_totals(make_entry("Pledged", 12, "pledged"), 0)
    # Boundary case: zero amount with excluded status.
    check_totals(make_entry("Zero", 0, "received"), 0)

    # Empty group should have a total of zero.
    check_totals(make_group("Empty", []), 0)
    # Flat group with mixed included and excluded entries.
    check_totals(make_group("Flat", [
        make_entry("Received", 11, "received"),
        make_entry("Pledged", 11, "pledged"),
    ]), 11)
    
    # Nested group with mixed included and excluded entries.
    mixed = make_group("Mixed", [
        make_entry("Received", 8, "received"),
        make_entry("Pledged", 8, "pledged"),
        make_group("No matches", [
            make_entry("First pledge", 3, "pledged"),
            make_entry("Second pledge", 5, "pledged"),
        ]),
        make_group("Nested", [
            make_entry("Nested receipt", 4, "received"),
            make_group("Deeper", [
                make_entry("Deep receipt", 2, "received"),
                make_entry("Deep pledge", 4, "pledged"),
            ]),
        ]),
    ])
    # Check totals for the nested mixed group.
    check_totals(mixed, 14)
    # Check totals for a group containing the nested mixed group.
    check_totals(make_group("Additional container", [mixed]), 14)
    
    # Malformed excluded entry should raise a ValueError when checked.
    malformed_excluded_entry = make_entry("Invalid pledge", -1, "pledged")
    for total_function in (recursive_total, iterative_total):
        try:
            total_function(malformed_excluded_entry, included_status)
        except ValueError:
            pass
        else:
            raise AssertionError(
                f"{total_function.__name__} accepted malformed excluded data"
            )


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Run tests without -O so assertions remain enabled.")
    assignment_checks()
    print("AL06 checks passed.")