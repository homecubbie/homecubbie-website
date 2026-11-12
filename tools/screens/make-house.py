"""Writes a HomeCubbie format-2 backup of a fictional house, 14 Alder Street.

Every name, number and address here is invented for the website's
screenshots. Phone numbers are in the 555-01xx range reserved for fiction.
Brands and model numbers identify products, not people.

Usage: python3 -I make-house.py <template-dir> <out.zip>

<template-dir> is any backup the app has just written, unzipped: it supplies
the list of tables and the schema version, so this keeps working as the
schema moves. See README.md.
"""
import hashlib
import json
import os
import sys
import uuid
import zipfile
from datetime import date

TEMPLATE, OUT = sys.argv[1], sys.argv[2]
NOW = "2026-11-01T15:00:00.000Z"
U = lambda: str(uuid.uuid4())
TS = {"created_at": NOW, "updated_at": NOW, "deleted_at": None}

rows = {}
def add(table, row):
    rows.setdefault(table, []).append(row)
    return row["id"]

PROP = U()
HH = U()
add("property", {"id": PROP, "name": "14 Alder Street", **TS})
add("household", {"id": HH, "name": "14 Alder Street", **TS, "property_id": PROP})
add("preference", {"id": "backup.frequency", "value": "weekly", **TS})
P = {"property_id": PROP}

# ---------------- people ----------------
def person(name, kind, role=None, phone=None, email=None, notes=None, lives_here=0):
    return add("person", {"id": U(), "household_id": HH, "name": name, **TS, **P, "kind": kind,
                          "role": role, "phone": phone, "email": email, "notes": notes, "lives_here": lives_here})

maya = person("Maya", "person", lives_here=1)
sam = person("Sam", "person", lives_here=1)
plumber = person("Northside Plumbing", "organization", "Plumber", "(555) 010-4471")
hvac = person("Northside Heating & Air", "organization", "Heating and cooling", "(555) 010-4472")
handy = person("Dana Ortiz", "person", "Handyman", "(555) 010-4188", "dana.ortiz@example.com")
insurer = person("Harbor Mutual", "organization", "Insurer", "(555) 010-2290")
lg = person("LG", "organization", "Manufacturer", "(555) 010-5544")
bosch = person("Bosch", "organization", "Manufacturer", "(555) 010-5545")
whirl = person("Whirlpool", "organization", "Manufacturer", "(555) 010-5546")
power = person("Alder Valley Electric", "organization", "Electricity", "(555) 010-3300")
water = person("Alder Valley Water", "organization", "Water", "(555) 010-3301")
fiber = person("Coastline Fiber", "organization", "Internet", "(555) 010-3302")
bank = person("Keystone Home Loans", "organization", "Mortgage", "(555) 010-3303")
county = person("Alder County Treasurer", "organization", "Property tax", "(555) 010-3304")
dmv = person("Motor Vehicles", "organization", "Registration", "(555) 010-3305")

# ---------------- places ----------------
def place(name, type_, parent=None, icon=None):
    return add("location", {"id": U(), "parent_id": parent, "type": type_, "name": name, "metadata": None, **TS,
                            "household_id": None, "status": "active", "archived_at": None, **P,
                            "icon_key": icon, "kind": None, "sort_order": None})

whole = place("Whole house", "WholeHome")
main = place("Main floor", "Floor")
up = place("Upstairs", "Floor")
base = place("Basement", "Floor")
kitchen = place("Kitchen", "Room", main, "pot")
living = place("Living room", "Room", main, "sofa")
laundry = place("Laundry", "Room", main, "washer")
entry = place("Entry", "Area", main, "door")
bed = place("Primary bedroom", "Room", up)
bath = place("Bathroom", "Room", up, "drop")
mech = place("Mechanical room", "Area", base, "valve")
garage = place("Garage", "Garage")
yard = place("Yard", "Yard")

# ---------------- things ----------------
def thing(name, loc, make, model, serial=None, year=None, bought=None, icon=None):
    return add("asset", {"id": U(), "name": name, "location_id": loc, "metadata": None, **TS,
                         "household_id": None, "status": "active", "archived_at": None, **P,
                         "make": make, "model": model, "serial": serial, "year": year,
                         "purchased_on": bought, "purchase_price_cents": None, "icon_key": icon, "kind": None})

fridge = thing("Fridge", kitchen, "LG", "LRFXS2503S", "105KRAB3F719", None, "2021-06-12", "fridge")
dish = thing("Dishwasher", kitchen, "Bosch", "SHPM65Z55N", "FD9803 0041", None, "2022-03-04")
furnace = thing("Furnace", mech, "Carrier", "59SC5A060E17", "2419A60311", None, "2019-10-01", "flame")
heater = thing("Water heater", mech, "Rheem", "XG50T06EC36U1", "Q201734118", None, "2020-08-20", "drop")
washer = thing("Washer", laundry, "Whirlpool", "WTW5057LW", "C30711842", None, "2023-01-15", "washer")
car = thing("Honda CR-V", garage, "Honda", "CR-V EX", None, 2021, "2021-04-10", "car")
opener = thing("Garage door opener", garage, "Chamberlain", "B4613T", None, None, "2020-05-02", "garage")
mower = thing("Lawn mower", garage, "EGO", "LM2135SP", None, None, "2024-04-20", "leaf")

# ---------------- policies ----------------
def policy(kind, provider, name=None, asset=None, prop=None, terms=(), fields=()):
    pid = U()
    term_ids = []
    for starts, ends, cost, period in terms:
        term_ids.append(U())
    for i, (starts, ends, cost, period) in enumerate(terms):
        add("policy_term", {"id": term_ids[i], "policy_id": pid, "starts_on": starts, "ends_on": ends,
                            "cost_cents": cost, "cost_period": period,
                            "superseded_by": term_ids[i + 1] if i + 1 < len(term_ids) else None,
                            **P, **TS, "cost_period_canonical": period, "actor_person_id": None})
    for j, (label, value, sensitive) in enumerate(fields):
        add("policy_field", {"id": U(), "policy_term_id": term_ids[-1], "label": label, "value": value,
                             "sort_order": j, "is_sensitive": sensitive, **P, **TS})
    add("policy", {"id": pid, "kind": kind, "subject_property_id": prop, "subject_asset_id": asset,
                   "provider_person_id": provider, "current_term_id": term_ids[-1], **P, **TS,
                   "ended_on": None, "name": name, "actor_person_id": None})
    return pid

policy("warranty", lg, asset=fridge, terms=[("2021-06-12", "2026-06-12", None, None)],
       fields=[("Serial number", "105KRAB3F719", 0)])
policy("warranty", bosch, asset=dish, terms=[("2022-03-04", "2027-03-04", None, None)])
policy("warranty", whirl, name="Extended warranty", asset=washer, terms=[("2023-01-15", "2028-01-15", 12900, None)])
policy("insurance", insurer, name="Car insurance", asset=car,
       terms=[("2025-05-18", "2025-11-18", 59400, "every 6 months"), ("2025-11-18", "2026-05-18", 61200, "every 6 months"), ("2026-05-18", "2026-11-18", 64800, "every 6 months")],
       fields=[("Policy number", "HM-4471-2290-03", 0), ("Claims line", "(555) 010-2299", 0),
               ("Coverage", "100/300/100", 0), ("Deductible", "$500", 0)])
policy("insurance", insurer, name="Home insurance", prop=PROP,
       terms=[("2025-03-01", "2026-03-01", 141600, "a year"), ("2026-03-01", "2027-03-01", 148200, "a year")],
       fields=[("Policy number", "HM-H-88310-7", 0), ("Claims line", "(555) 010-2299", 0),
               ("Dwelling", "$420,000", 0), ("Deductible", "$1,000", 0)])
policy("registration", dmv, name="Registration", asset=car, terms=[("2025-12-31", "2026-12-31", 18600, "a year")],
       fields=[("Plate", "8ALD 142", 0)])
plan = policy("service_plan", hvac, name="Furnace service plan", asset=furnace,
              terms=[("2026-02-01", "2027-02-01", 1900, "a month")],
              fields=[("Plan number", "NHA-20931", 0), ("Visits", "Two a year, spring and fall", 0)])

# ---------------- events ----------------
def event(kind, name, on, asset=None, cost=None, who=None, notes=None, covered=None, loc=None, prop=None):
    return add("event", {"id": U(), "kind": kind, "subject_property_id": prop, "subject_location_id": loc,
                         "subject_asset_id": asset, "name": name, "occurred_on": on, "cost_cents": cost,
                         "person_id": who, "notes": notes, **P, **TS, "actor_person_id": None,
                         "completion_event_id": None, "covered_by_policy_id": covered})

event("purchase", "Bought the fridge", "2021-06-12", fridge, 189900)
event("purchase", "Bought the dishwasher", "2022-03-04", dish, 94900)
event("purchase", "Bought the washer", "2023-01-15", washer, 74900)
event("purchase", "Bought the lawn mower", "2024-04-20", mower, 54900)
event("repair", "Replaced the ice maker valve", "2026-07-09", fridge, 21500, handy,
      "Ice maker stopped filling. The inlet valve had cracked; replaced with an LG part.")
event("service", "Fall furnace tune-up", "2026-10-14", furnace, 0, hvac, "Covered by the plan. Filter changed, burners cleaned.", plan)
event("service", "Spring furnace tune-up", "2026-04-08", furnace, 0, hvac, None, plan)
event("repair", "Replaced a garage door spring", "2026-03-22", opener, 28500, handy)
event("repair", "Fixed the leak under the kitchen sink", "2026-08-30", None, 18900, plumber,
      "Loose compression fitting on the cold line.", None, kitchen)
event("service", "Flushed the water heater", "2025-12-06", heater, None, sam)
event("repair", "Replaced the dishwasher drain pump", "2025-06-17", dish, 34000, handy)
event("service", "Furnace check before winter", "2025-10-09", furnace, 18900, hvac)
event("repair", "Patched the roof flashing", "2025-04-02", None, 42000, None, None, None, None, PROP)

# ---------------- notes ----------------
def note(cat, label, value, detail=None, sensitive=0, order=0):
    add("note", {"id": U(), "category": cat, "label": label, "value": value, "detail": detail,
                 "is_sensitive": sensitive, "sort_order": order, **P, **TS})

note("emergency", "Water shutoff", "Basement, behind the furnace on the north wall", "Turn it clockwise. The wrench hangs beside it.", 0, 0)
note("emergency", "Gas shutoff", "Outside, left of the meter on the east side", "Needs the gas wrench in the garage drawer.", 0, 1)
note("emergency", "Breaker panel", "Garage, beside the door to the kitchen", "Breaker 14 is the kitchen outlets.", 0, 2)
note("access", "Alarm code", "4821", "Panel by the front door", 1, 0)
note("access", "Key safe", "0715", "On the back porch post", 1, 1)
note("access", "Wi-Fi", "AlderStreet / tidy-lemon-42", None, 1, 2)
note("routines", "Trash and recycling", "Trash Tuesday morning, recycling every other Thursday", None, 0, 0)
note("utilities", "Furnace filter", "16 × 25 × 1, MERV 11", "Spares on the shelf above the furnace", 0, 0)
note("utilities", "Water heater", "Rheem 50 gallon, gas, in the basement", None, 0, 1)
note("finishes", "Living room paint", "Agreeable Gray SW 7029, eggshell", "Touch-up can in the garage", 0, 0)
note("settings", "Thermostat", "68° by day, 62° at night", None, 0, 0)

# ---------------- accounts and bills ----------------
def account(kind, provider, name=None, number=None, loan=None):
    row = {"id": U(), "kind": kind, "provider_person_id": provider, "name": name, "account_number": number,
           "tariff_ends_on": None, "notes": None, **P, **TS, "ended_on": None,
           "loan_amount_cents": None, "loan_rate_basis_points": None, "loan_term_years": None, "loan_started_on": None}
    if loan:
        row.update(loan)
    return add("account", row)

def month_end(y, m):
    nxt = date(y + (m == 12), m % 12 + 1, 1)
    return date.fromordinal(nxt.toordinal() - 1).isoformat()

def bills(acct, provider, amounts, start=(2025, 11), step=1):
    y, m = start
    for amt in amounts:
        end_m, end_y = m + step - 1, y
        while end_m > 12:
            end_m -= 12; end_y += 1
        add("account_bill", {"id": U(), "account_id": acct, "period_start": date(y, m, 1).isoformat(),
                             "period_end": month_end(end_y, end_m), "amount_cents": amt, "notes": None, **P, **TS,
                             "provider_person_id": provider, "actor_person_id": None})
        m += step
        while m > 12:
            m -= 12; y += 1

elec = account("electricity", power, None, "4410-2276-01")
bills(elec, power, [14200, 12900, 11300, 9600, 9200, 13100, 16900, 17400, 14300, 10100, 11800, 13600, 14900, 12700, 10400, 9100, 9800, 14200, 17800, 18600, 15100, 10900], (2025, 1))
wat = account("water", water, None, "W-30817")
bills(wat, water, [5800, 6100, 8400, 8900, 7200, 6200, 5900, 6400, 7800, 9100, 8700], (2025, 1), 2)
net = account("internet", fiber, None, "CF-0091142")
bills(net, fiber, [6500] * 10 + [7000] * 12, (2025, 1))
mort = account("mortgage", bank, None, "KHL-55310298",
               {"loan_amount_cents": 34000000, "loan_rate_basis_points": 625, "loan_term_years": 30, "loan_started_on": "2019-09-30"})
bills(mort, bank, [209400] * 22, (2025, 1))
tax = account("property_tax", county, None, "APN 112-40-077")
bills(tax, county, [298000, 298000, 315000, 315000], (2025, 1), 6)

# ---------------- tasks ----------------
cats = {name: add("category", {"id": U(), "name": name, **TS, "household_id": None, "parent_category_id": None, **P})
        for name in ["Safety", "Heating and cooling", "Appliance care", "Outside", "Car"]}

def task(name, type_, cat, anchor, months, asset=None, loc=None, minutes=None, cost=None, safety=0):
    tid = add("task_definition", {"id": U(), "name": name, "description": None, "type": type_,
                                  "category_id": cats[cat], "estimated_minutes": minutes, "instructions": None, **TS,
                                  "household_id": None, **P, "expected_cost_cents": cost, "safety_critical": safety})
    add("schedule", {"id": U(), "task_definition_id": tid, "location_id": None, "recurrence_type": "EVERY_N_MONTHS",
                     "anchor_date": anchor, "interval_days": None, "interval_months": months, "week_ordinal": None,
                     "day_of_week": None, "month_of_year": None, "day_of_month": None, "season": None,
                     "days_after_completion": None, "extra_config": None, **TS, "seasonal_trigger": None, **P,
                     "active_from_month": None, "active_to_month": None})
    if asset:
        add("task_asset", {"id": U(), "task_definition_id": tid, "asset_id": asset, **TS, **P})
    if loc:
        add("task_location", {"id": U(), "task_definition_id": tid, "location_id": loc, **TS, **P})

task("Replace the furnace filter", "Replacement", "Heating and cooling", "2026-11-05", 3, furnace, minutes=10, cost=1800)
task("Clean the gutters", "Maintenance", "Outside", "2026-11-09", 6, loc=yard, minutes=90)
task("Test the smoke alarms", "Inspection", "Safety", "2026-11-12", 1, loc=whole, minutes=15, safety=1)
task("Run a dishwasher cleaning cycle", "Cleaning", "Appliance care", "2026-11-12", 1, dish, minutes=5)
task("Change the fridge water filter", "Replacement", "Appliance care", "2026-11-14", 6, fridge, minutes=10, cost=4900)
task("Clean the washer drum", "Cleaning", "Appliance care", "2026-11-15", 1, washer, minutes=10)
task("Winterize the outdoor faucets", "Maintenance", "Outside", "2026-11-16", 12, loc=yard, minutes=20)
task("Lubricate the garage door", "Maintenance", "Outside", "2026-11-18", 6, opener, minutes=15)
task("Rotate the tires", "Maintenance", "Car", "2026-11-25", 6, car)
task("Test the sump pump", "Inspection", "Safety", "2026-12-01", 3, loc=mech, minutes=10)
task("Flush the water heater", "Maintenance", "Appliance care", "2026-12-06", 12, heater, minutes=45)
task("Vacuum the fridge coils", "Cleaning", "Appliance care", "2027-01-10", 6, fridge, minutes=20)
task("Tune up the lawn mower", "Maintenance", "Outside", "2027-03-15", 12, mower, minutes=30)

# ---------------- write the archive ----------------
template = json.load(open(os.path.join(TEMPLATE, "manifest.json")))
manifest = {"app": "HomeCubbie", "kind": "full-backup", "formatVersion": template["formatVersion"],
            "schemaVersion": template["schemaVersion"], "createdAt": "2026-11-12T12:00:00.000Z",
            "tables": {}, "documents": {}}
unknown = set(rows) - set(template["tables"])
assert not unknown, unknown
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for name in template["tables"]:
        data = "".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows.get(name, []))
        b = data.encode("utf-8")
        path = f"tables/{name}.ndjson"
        z.writestr(path, b)
        manifest["tables"][name] = {"path": path, "rows": len(rows.get(name, [])), "sha256": hashlib.sha256(b).hexdigest()}
    z.writestr("manifest.json", json.dumps(manifest, indent=2))
print({k: len(v) for k, v in rows.items()})
