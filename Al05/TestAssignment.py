"""Unfinished prompts for sort stability, pipeline contracts, and rule revision."""

from copy import deepcopy
from Main import insertion_sort, build_views
from Ticket_Data import TICKETS
from search_support import id_key, days_key
from Pipline import select_open_tickets


def assignment_checks():
    """Check expected orders, stable ties, shared records, and rebuilt query views."""
    # TUESDAY: test empty/singleton, ordered/reverse/shuffled inputs, and stable ties.
    # Compare output with sorted under the same key; source order/fields stay intact.
    # Check new outer list and shared record identities, using `is` where useful.
    # Check the small fixture's expected counts and ID trace, not timing.
    # THURSDAY: check exact selected/display/search IDs at thresholds 4, 7, and 8.
    # Include boundary ages and completed-ticket exclusion; rebuild from TICKETS.
    # Import your local searches when ready: test found/missing and view positions.
    # Mark wrong-view T406 as deliberate invalid use, separate from valid contracts.
    # Use a separate fixture copy if testing a field edit; do not alter shared seed.
    # Monday: use the completed filter and Tuesday sort without Thursday's build_views.
    selected = select_open_tickets(TICKETS, minimum_days=4)
    display, _, _, _ = insertion_sort(selected, key=days_key)
    assert selected is not display
    assert [ticket["id"] for ticket in selected] == ["T403", "T405", "T402", "T406"]
    assert [ticket["id"] for ticket in display] == ["T406", "T402", "T403", "T405"]
    assert all(ticket["days_open"] >= 4 for ticket in selected)
    assert all(ticket["days_open"] >= 4 for ticket in display)
    assert all(ticket["status"] == "open" for ticket in selected)
    assert all(ticket["status"] == "open" for ticket in display)
    # Ensure that the returned lists are sorted correctly according to the intended keys
    assert all(display[i]["days_open"] <= display[i + 1]["days_open"] for i in range(len(display) - 1))
    # Tuesday: test stable ties
    tickets_copy = deepcopy(TICKETS)
    tickets_copy, _, _, _ = insertion_sort(tickets_copy, key=days_key)
    assert all(tickets_copy[i]["days_open"] <= tickets_copy[i + 1]["days_open"] for i in range(len(tickets_copy) - 1))
    # Ensure stable ties: tickets with the same days_open retain their original relative order
    for i in range(len(tickets_copy) - 1):
        if tickets_copy[i]["days_open"] == tickets_copy[i + 1]["days_open"]:
            assert TICKETS.index(tickets_copy[i]) < TICKETS.index(tickets_copy[i + 1])
            assert tickets_copy[i] is not tickets_copy[i + 1]
    # Thursday: add build_views and search-view checks after that stage is implemented.
    assert build_views is not None  # Ensure build_views function exists before further checks
    assert callable(build_views)  # Ensure build_views is callable before further checks
    selected, display, search = build_views(TICKETS, minimum_days=4)
    assert all(ticket["days_open"] >= 4 for ticket in selected)
    assert all(ticket["status"] == "open" for ticket in selected)
    assert all(ticket["days_open"] >= 4 for ticket in display)
    assert all(ticket["status"] == "open" for ticket in display)
    assert all(ticket["days_open"] >= 4 for ticket in search)
    assert all(ticket["status"] == "open" for ticket in search)
    # Ensure that the display view is sorted by days_open
    assert all(display[i]["days_open"] <= display[i + 1]["days_open"] for i in range(len(display) - 1))
    # Ensure that the search view is sorted by ID
    assert all(search[i]["id"] <= search[i + 1]["id"] for i in range(len(search) - 1))
    # Ensure that the search view contains the same tickets as the selected view, but in ID order
    assert set(ticket["id"] for ticket in search) == set(ticket["id"] for ticket in selected)
    # Ensure that the search view is a stable ordering by ID relative to the original TICKETS list
    for i in range(len(search) - 1):
        if search[i]["id"] == search[i + 1]["id"]:
            assert TICKETS.index(search[i]) < TICKETS.index(search[i + 1])
            assert search[i] is not search[i + 1]
        

if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run tests without -O so assertions are enabled.")
    assignment_checks()
    print("AL05 checks passed.")