from Data import TICKETS
from Search_Support import id_key, category_key, matches, compare_values
from Display import show_ticket, show_tickets


# MONDAY - Separate the requested value from the traversal.

def linear_search(records, target, key=id_key):
    """Return the first matching position and visits, or None and visits."""
    # Begin an empty trace. Visit records in their existing order.
    # Select each record's value through key(record).
    # Remember its position and selected value before checking for a match.
    # Return the position and trace on a match; otherwise finish with None/trace.
    # Leave the records unchanged. An empty input has no visits.
    trace = []
    for i, record in enumerate(records):
        value = key(record)
        trace.append((i, value))
        if matches(value, target):
            return i, trace
    return None, trace


def binary_search(records, target, key=id_key):
    """Return any matching position and interval visits on a key-ordered input."""
    # The caller supplies a list ascending under the same key used here.
    # Begin with an empty trace and an inclusive interval covering the list.
    # While the interval contains candidates, select its integer midpoint.
    # Record low, high, middle, and the selected value before changing bounds.
    # Compare that value with target: match, lower, or higher.
    # Return on equality; otherwise discard the impossible side AND midpoint.
    # When no candidates remain, return None with the visits collected.
    # Do not sort or perform a sortedness scan inside this function.
    trace = []
    low = 0
    high = len(records) - 1
    while low <= high:
        mid = (low + high) // 2
        value = key(records[mid])
        trace.append((low, high, mid, value))
        if matches(value, target):
            return mid, trace
        elif value < target:
            low = mid + 1
        else:
            high = mid - 1
    return None, trace


# TUESDAY CHECKPOINT - Verify the contract and preserve an independent submission.

def main():
    """Show completed searches with readable results."""
    # MONDAY: inspect TICKETS, then show found T403 and absent T499 using a scan.
    # Prepare an ID-ascending view outside binary_search; repeat those requests.
    # A result position belongs to the exact list searched; test `is None`.
    # Deliberately search original unsorted data for T401; explain the miss.
    # Use category_key with a category-ordered view for repeated category account.
    # Accept any matching category record, not necessarily the same position.

    # TUESDAY: finish the boundary/duplicate/nonmutation tests and short README.
    # Run the final personal week_04/AL04 copy before submitting its repo URL.
    # Copy completed functions into AL05 later; preserve this submitted snapshot.
    # Show every ticket first
    show_tickets("All tickets", TICKETS)

    # Linear search: found ticket
    print("\nLinear search for T403 ")
    position, trace = linear_search(TICKETS, "T403", key=id_key)
    print("Position found:", position)
    if position is not None:
        show_ticket(TICKETS[position])

    # Linear search: missing ticket
    print("\n Linear search for T499 ")
    position, trace = linear_search(TICKETS, "T499", key=id_key)
    print("Position found:", position)
    show_ticket(None)
    
    print("\n Linear search for T401 ")
    position, trace = linear_search(TICKETS, "T401", key=id_key)
    print("Position found:", position)
    if position is not None:
        show_ticket(TICKETS[position])

    # Binary search needs sorted data, so sort a copy by ID first
    sorted_tickets = sorted(TICKETS, key=id_key)

    print("\n Binary search for T403 (sorted copy)")
    position, trace = binary_search(sorted_tickets, "T403", key=id_key)
    print("Position found:", position)
    if position is not None:
        show_ticket(sorted_tickets[position])

    print("\n Binary search for T499 (sorted copy)")
    position, trace = binary_search(sorted_tickets, "T499", key=id_key)
    print("Position found:", position)
    show_ticket(None)
    
    print("\n Binary search for T401 (unsorted data)")
    position, trace = binary_search(TICKETS, "T401", key=id_key)
    print("Position found:", position)
    if position is not None:
        show_ticket(TICKETS[position])


if __name__ == "__main__":
    main()