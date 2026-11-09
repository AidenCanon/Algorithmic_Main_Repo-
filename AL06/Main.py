
from scenario_data import SCENARIOS
from record_support import validate_node
from record_display import show_records, show_results

CHOICE = "fundraiser"  


def recursive_total(node, included_status):
    validate_node(node)
    if node["type"] == "entry":
        return node["amount"] if node["status"] == included_status else 0
    subtotal = 0
    for child in node["items"]:
        subtotal += recursive_total(child, included_status)
    return subtotal


def iterative_total(node, included_status):
    stack = [node]
    total = 0
    while stack:
        current = stack.pop()
        validate_node(current)
        if current["type"] == "entry":
            if current["status"] == included_status:
                total += current["amount"]
        else:
            stack.extend(current["items"])
    return total


def main():
    """Choose one context and present only the completed application stages."""
    scenario = SCENARIOS[CHOICE]
    show_records(scenario["data"], scenario["unit"])
    recursive_result = recursive_total(
        scenario["data"], scenario["included_status"]
    )
    iterative_result = iterative_total(
        scenario["data"], scenario["included_status"]
    )
    show_results(scenario, recursive_result, iterative_result)


if __name__ == "__main__":
    main()