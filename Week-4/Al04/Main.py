from Data import TICKETS
from Search_Support import id_key, category_key, matches, compare_values
from Display import show_ticket, show_tickets


# MONDAY - Separate the requested value from the traversal.

def linear_search(records, target, key=id_key):
    trace = []
    for i, record in enumerate(records):
        value = key(record)
        trace.append((i, value))
        if matches(value, target):
            return i, trace
    return None, trace


def binary_search(records, target, key=id_key):
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