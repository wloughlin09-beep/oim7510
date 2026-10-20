# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo>=0.25.2",
# ]
# ///

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A · Where the Tax Bill Is Lowest#
    A couple is looking for a single-family home in Middlesex County with a budget of $700,000, and they want to keep the property tax bill under $8,000 a year. They want a short list of towns where the average home fits the budget and the average bill fits the limit, cheapest bill first, and they want to rerun it for another county or another budget.

    The data is the course API's Massachusetts endpoints, built from the state's Division of Local Services: oim.zhili.dev/ma lists them, and oim.zhili.dev/docs describes every field.

    county = "Middlesex"
    budget_dollars = 700000
    tax_limit_dollars = 8000
    fiscal_year = 2026
    Copy
    The main task

    Every town in the county, from /ma/towns?county=.... The reply's pagination reports how many towns there are; make sure you have all of them.
    For each town, its figures for fiscal_year from /ma/towns/{dor_code}/history. Compare every town for the same year.
    A table of the towns that pass both limits, cheapest bill first: town, average home value, residential tax rate, and average bill.
    One sentence that answers the couple, with the numbers in it.
    You may need the params= argument of requests.get. A page holds 50 towns unless you ask for more, up to 100.

    Going further

    Rank the same towns by tax rate in place of the bill. Does the order change, and why?
    Show how the bill has changed over 10 years for the three towns with the lowest bill on your list.
    Add the town's income per person and state the bill as a share of it.
    Let the couple change the county and the limits without editing code.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notes while I figure this out: We want to pull every town in the county including paginations.We need to loop through pages and collect all towns, handling the "next page" button until it no longer exists.

    I will want to check the data I pull against the data that the document actually shows. Once I am able to get all of the data throgh the pagination I will want to be able to filter against both limits given in the request.

    Once that filter is working I will want to create a table and not just a one sentense answer
    """)
    return


@app.cell
def _():
    import requests

    county = "Middlesex"
    budget_dollars = 700000
    tax_limit_dollars = 8000
    fiscal_year = 2026
    return budget_dollars, county, fiscal_year, requests, tax_limit_dollars


@app.cell
def _(county, requests):
    middlesex_towns = []
    page_number = 1

    while True:
        towns_reply = requests.get(
            "https://oim.zhili.dev/ma/towns",
            params={"county": county, "limit": 100, "page": page_number},
            timeout=10,
        ).json()
        middlesex_towns.extend(towns_reply["items"])
        if len(middlesex_towns) >= towns_reply["pagination"]["total"]:
            break
        page_number += 1

    len(middlesex_towns)
    return (middlesex_towns,)


@app.cell
def _(fiscal_year, middlesex_towns, requests):
    town_summaries = []

    for town in middlesex_towns:
        dor_code = town["dor_code"]
        history_reply = requests.get(
            f"https://oim.zhili.dev/ma/towns/{dor_code}/history",
            timeout=10,
        ).json()

        for record in history_reply["years"]:
            if record["fiscal_year"] == fiscal_year:
                town_summaries.append([
                    town["name"],
                    record["average_single_family_value_dollars"],
                    record["residential_rate_per_thousand"],
                    record["average_single_family_bill_dollars"],
                ])

    print(f"{len(town_summaries)} of {len(middlesex_towns)} towns had data for fiscal year {fiscal_year}")
    return (town_summaries,)


@app.cell
def _(budget_dollars, tax_limit_dollars, town_summaries):
    towns_in_budget = []

    for _row in town_summaries:
        town_name, avg_value, tax_rate, avg_bill = _row
        if avg_value <= budget_dollars and avg_bill <= tax_limit_dollars:
            towns_in_budget.append(_row)

    def bill_amount(row):
        return row[3]

    towns_sorted = sorted(towns_in_budget, key=bill_amount)
    towns_sorted
    return (towns_sorted,)


@app.cell
def _(towns_sorted):
    town_table = []
    for row in towns_sorted:
        town_table.append({
            "town": row[0],
            "average_home_value": row[1],
            "residential_tax_rate": row[2],
            "average_bill": row[3],
        })

    town_table
    return


@app.cell
def _(budget_dollars, county, tax_limit_dollars, towns_sorted):
    if len(towns_sorted) == 0:
        print(f"No town in {county} County fits a ${budget_dollars:,} home within an ${tax_limit_dollars:,} tax bill.")
    else:
        cheapest = towns_sorted[0]
        print(
            f"In {county} County, {cheapest[0]} has the lowest average tax bill at "
            f"${cheapest[3]:,.2f} a year, with an average home value of ${cheapest[1]:,.2f}, "
            f"fitting the couple's ${budget_dollars:,} budget and ${tax_limit_dollars:,} limit."
        )
    return


@app.cell
def _(towns_sorted):
    print(f"{'Town':<15}{'Avg Home Value':>16}{'Tax Rate':>12}{'Avg Bill':>12}")

    for _row in towns_sorted:
        _town, _value, _rate, _bill = _row
        print(f"{_town:<15}{_value:>16,.0f}{_rate:>12.2f}{_bill:>12,.0f}")
    return


if __name__ == "__main__":
    app.run()
