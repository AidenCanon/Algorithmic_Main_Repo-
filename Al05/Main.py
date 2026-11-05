from Ticket_Data import TICKETS
from search_support import id_key, days_key, matches, compare_values
from Pipline import select_open_tickets
from Ticket_Display import show_ticket, show_tickets

# After preparing your local search_algorithms.py, add its search imports here.
# Copy your AL04 functions/imports, or use the instructor-released recovery module.
def linear_search(records, target, key=id_key):
    """Return a first matching view position and trace, or None and the visit trace."""
    trace = []
    for position, record in enumerate(records):
        value = key(record)
        trace.append((position, value))
        if matches(value, target):
            return position, trace
    return None, trace


def binary_search(records, target, key=id_key):
    """Return any match and trace, assuming ascending order under the selected key."""
    low = 0
    high = len(records) - 1
    trace = []
    while low <= high:
        middle = (low + high) // 2
        value = key(records[middle])
        trace.append((low, high, middle, value))
        comparison = compare_values(value, target)
        if comparison == 0:
            return middle, trace
        if comparison < 0:
            low = middle + 1
        else:
            high = middle - 1
    return None, trace


# TUESDAY - Stable ordering, with counts for one tiny example.

def insertion_sort(records, key):
    """Return a stable shallow ordered list, comparison/shift counts, and ID trace."""
    # Copy the outer list, sharing its record dictionaries. Start counts/trace.
    # Each position after the first introduces one item into the sorted prefix.
    # Save that item, then inspect earlier items from right to left.
    # Count each executed key comparison; shift only when the earlier key is larger.
    # Count right-shifts, not final placements. Stop shifting on equality.
    # Place the saved item in the gap. Record the entire ID order after insertion.
    # Return ordered list, comparisons, moves, and trace, even for empty input.
    ordered = records[:]
    comparisons = 0
    moves = 0
    trace = []
    for i in range(1, len(ordered)):
        current = ordered[i]
        current_key = key(current)
        j = i - 1
        while j >= 0 and compare_values(key(ordered[j]), current_key) > 0:
            comparisons += 1
            ordered[j + 1] = ordered[j]
            moves += 1
            j -= 1
        if j >= 0:
            comparisons += 1
        ordered[j + 1] = current
        trace.append([r["id"] for r in ordered])
    return ordered, comparisons, moves, trace


# THURSDAY - Compose existing interfaces; rebuild after the eligibility change.

def build_views(records, minimum_days=4):
    """Return selected, age-display, and ID-search lists sharing eligible records."""
    # Use the supplied open/age filter on the authoritative source.
    # Use your insertion sort with days_key to build the display view.
    # Use sorted with id_key to build the separate binary-search view.
    # Return the three lists; do not copy records or edit their fields.
    selected = select_open_tickets(records, minimum_days=minimum_days)
    display, _, _, _ = insertion_sort(selected, key=days_key)
    search = sorted(selected, key=id_key)
    return selected, display, search


def main():
    """Present completed daily stages and explain the issued threshold change."""
    # TUESDAY: select open tickets aged at least 4 days; show stable age ordering.
    # Label the tiny ID trace and comparison/right-shift counts as teaching evidence.
    # Check your sort against sorted, including tied keys and unchanged source.

    # THURSDAY: build both views and use the local search_algorithms functions.
    # Find T403 and absent T499; resolve positions in the particular list searched.
    # Deliberately use the age display for ID binary search of T406; explain failure.
    # Rebuild from TICKETS at minimum_days=7, then 8, to show revised/empty results.
    # Keep app output readable; put short workload/copy/change notes in README.md.
    # Test and submit the complete personal week_04/AL05 folder independently.
    print("Monday output")
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
        
    print("\nTuesday output")
    tuesday_tickets = select_open_tickets(TICKETS, minimum_days=4)
    for ticket in tuesday_tickets:
        show_ticket(ticket)

    print("\nThursday output")
    selected, display, search = build_views(TICKETS, minimum_days=4)
    print("Selected view:")
    for ticket in selected:
        show_ticket(ticket)
    print("Display view:")
    for ticket in display:
        show_ticket(ticket)
    print("Search view:")
    for ticket in search:
        show_ticket(ticket)


if __name__ == "__main__":
    main()