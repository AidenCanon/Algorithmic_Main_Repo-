_MIN_AGE_DAYS_FOR_FOLLOW_UP = 2
from ticket_data import TICKETS

# Validate ticket records and generate reports for open tickets.
def check_validation(ticket):
    # Check if the ticket is a dictionary and has the required fields.  
    if not isinstance(ticket, dict):
        return ["Invalid ticket record: expected a dictionary."]

    ticket_id = ticket.get("id")
    usable_id = isinstance(ticket_id, str) and bool(ticket_id.strip())
    label = ticket_id.strip() if usable_id else "unknown ticket"
    issues = []
    # Validate the ticket ID.
    if not usable_id:
        issues.append(f"{label}: id must be a non-empty string.")
    # Validate the status, category, and priority fields.
    accepted_values = {
        "status": {"open", "closed"},
        "category": {"software", "access", "network"},
        "priority": {"high", "normal", "low"},
    }
    for field, accepted in accepted_values.items():
        if field not in ticket:
            issues.append(f"{label}: missing required field '{field}'.")
        elif not isinstance(ticket[field], str) or ticket[field] not in accepted:
            options = ", ".join(sorted(accepted))
            issues.append(
                f"{label}: '{field}' must be one of: {options}."
            )

    # Validate the age_days field.
    if "age_days" not in ticket:
        issues.append(f"{label}: missing required field 'age_days'.")
    else:
        age_days = ticket["age_days"]
        if (
            isinstance(age_days, bool)
            or not isinstance(age_days, int)
            or age_days < 0
        ):
            issues.append(
                f"{label}: 'age_days' must be a non-negative integer."
            )

    return issues

# Select open tickets from the list of records.
def select_open_tickets(records):
    # Initialize lists for selected tickets and issues.
    selected = []
    # List to store issues found during validation.
    issues = []

    # Iterate through each ticket and validate it.
    for ticket in records:
        ticket_issues = check_validation(ticket)
        # If there are issues with the ticket, add them to the issues list. Otherwise, if the ticket is open, add it to the selected list.
        if ticket_issues:
            issues.extend(ticket_issues)
        # Skip adding this ticket to the selected list since it has validation issues.
        elif ticket["status"] == "open":
            selected.append(ticket)

    return selected, issues

# Display a report of selected tickets and any issues found during validation.
def show_report(title, policy, selected, issues):
    print(f"\n{title}")
    print(f"Policy: {policy}")
    print("-" * 40)
    # Display the list of selected tickets.
    if selected:
        for ticket in selected:
            print(
                f"{ticket['id']} | "
                f"Status: {ticket['status']} | "
                f"Category: {ticket['category']} | "
                f"Age: {ticket['age_days']} days | "
                f"Priority: {ticket['priority']}"
            )
    else:
        print("No tickets match this view.")

    # Display the count of selected tickets.
    print(f"Selected tickets: {len(selected)}")
    # Display any issues found during validation.
    if issues:
        print("\nTickets needing review:")
        # List each issue that needs review.
        for issue in issues:
            print(f"- {issue}")
    else:
        print("\nNo ticket data issues found.")

def check_policy(tickets):
    follow_up_tickets = []
    prev_selected = []
    for ticket in tickets:
        if ticket['age_days'] >= _MIN_AGE_DAYS_FOR_FOLLOW_UP:
            prev_selected.append(ticket)
    
    for ticket in prev_selected:
        if ticket['priority'] == 'high' or ticket['category'] == 'access':
            follow_up_tickets.append(ticket)
    return follow_up_tickets, prev_selected

# Main function to execute the ticket selection and reporting process.
def main():
    # Select open tickets and gather any validation issues.
    selected, issues = select_open_tickets(TICKETS)
    #print(selected)
    selected, prev_selected = check_policy(selected)
    # Generate and display the report for the selected tickets and any issues.
    show_report("Open Tickets", "Previous selection policy", prev_selected, issues)
    show_report("Open Tickets", "Follow-up policy", selected, issues)
    # Entry point for the script.
if __name__ == "__main__":
    # Call the main function to execute the script.
    main()