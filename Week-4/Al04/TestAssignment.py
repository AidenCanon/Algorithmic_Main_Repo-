from copy import deepcopy

from Data import TICKETS
from Main import binary_search, linear_search
from Search_Support import category_key, id_key


def assignment_checks():
    original_tickets = deepcopy(TICKETS)

    # Linear search returns positions in the original, unsorted list.
    assert linear_search(TICKETS, "T403", key=id_key)[0] == 0
    assert linear_search(TICKETS, "T499", key=id_key)[0] is None
    assert linear_search([], "T403", key=id_key) == (None, [])

    # Singleton and two-record inputs cover found and missing targets.
    singleton = [TICKETS[0]]
    assert linear_search(singleton, "T403", key=id_key)[0] == 0
    assert linear_search(singleton, "T401", key=id_key)[0] is None
    pair = [TICKETS[0], TICKETS[1]]
    assert linear_search(pair, "T401", key=id_key)[0] == 1
    assert linear_search(pair, "T499", key=id_key)[0] is None

    # Binary search requires the records to be sorted by the selected key.
    # This particular unsorted input demonstrates a miss; it is not a general
    # guarantee that binary search misses every target on unsorted input.
    assert binary_search(TICKETS, "T401", key=id_key)[0] is None

    sorted_tickets = sorted(TICKETS, key=id_key)
    assert binary_search(sorted_tickets, "T401", key=id_key)[0] == 0
    assert binary_search(sorted_tickets, "T403", key=id_key)[0] == 2
    assert binary_search(sorted_tickets, "T406", key=id_key)[0] == 5
    assert binary_search(sorted_tickets, "T499", key=id_key)[0] is None
    assert binary_search([], "T403", key=id_key) == (None, [])

    sorted_singleton = [TICKETS[0]]
    assert binary_search(sorted_singleton, "T403", key=id_key)[0] == 0
    assert binary_search(sorted_singleton, "T401", key=id_key)[0] is None

    # Duplicate categories may match at any position in the category-sorted list.
    category_sorted = sorted(TICKETS, key=category_key)
    position, _ = binary_search(category_sorted, "account", key=category_key)
    assert position is not None
    assert category_key(category_sorted[position]) == "account"

    # Searches must not mutate the caller's records.
    assert TICKETS == original_tickets


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run tests without -O so assertions are enabled.")
    assignment_checks()
    print("Checks passed.")