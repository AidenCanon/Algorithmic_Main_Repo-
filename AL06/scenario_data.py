"""Comparable fictional nested data; choose one application for AL06."""


def make_entry(name, amount, status):
    """Build a leaf record without performing eligibility or aggregation."""
    return {"type": "entry", "name": name, "amount": amount, "status": status}


def make_group(name, items):
    """Build a group record containing the supplied child records."""
    return {"type": "group", "name": name, "items": items}


SCENARIOS = {
    "fundraiser": {
        "title": "Fundraiser Tracker",
        "unit": "whole dollars",
        "included_status": "received",
        "data": make_group("Community fundraiser", [
            make_entry("Welcome-table donations", 25, "received"),
            make_group("North team", [
                make_entry("Bake-sale donations", 40, "received"),
                make_entry("Sponsor promise", 90, "pledged"),
                make_group("Student volunteers", [
                    make_entry("Collection jar", 15, "received"),
                    make_entry("Matching pledge", 35, "pledged"),
                ]),
            ]),
            make_entry("Online promise", 10, "pledged"),
            make_group("New team", []),
        ]),
    },
}