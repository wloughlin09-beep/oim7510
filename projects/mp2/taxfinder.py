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

    Once that filter is working I will want to create a table and not just a one sentense answer.

    Honestly I had a really hard time trying to do any of this without the AI, all of my code failed and had to pivot to using the chat bot to help with the step by step process.
    """)
    return


@app.cell
def county_options():
    county_choices = [
        "Barnstable", "Berkshire", "Bristol", "Dukes", "Essex", "Franklin",
        "Hampden", "Hampshire", "Middlesex", "Nantucket", "Norfolk",
        "Plymouth", "Suffolk", "Worcester",
    ]
    return (county_choices,)


@app.cell
def settings_form_cell(county_choices, mo):
    settings_form = mo.ui.form(
        mo.md("""
        **Choose a county and limits**

        {county}

        {budget}

        {tax_limit}
        """).batch(
            county=mo.ui.dropdown(options=county_choices, value="Middlesex", label="County"),
            budget=mo.ui.number(start=100000, stop=5000000, step=10000, value=700000, label="Home budget ($)"),
            tax_limit=mo.ui.number(start=1000, stop=50000, step=100, value=8000, label="Max annual tax bill ($)"),
        ),
        label="Apply",
    )
    settings_form
    return (settings_form,)


@app.cell
def _(settings_form):
    import requests

    if settings_form.value is None:
        county = "Middlesex"
        budget_dollars = 700000
        tax_limit_dollars = 8000
    else:
        county = settings_form.value["county"]
        budget_dollars = settings_form.value["budget"]
        tax_limit_dollars = settings_form.value["tax_limit"]

    fiscal_year = 2026
    return budget_dollars, county, fiscal_year, requests, tax_limit_dollars


@app.cell
def _(county, requests):
    county_towns = []
    page_number = 1

    while True:
        towns_reply = requests.get(
            "https://oim.zhili.dev/ma/towns",
            params={"county": county, "limit": 100, "page": page_number},
            timeout=10,
        ).json()
        county_towns.extend(towns_reply["items"])
        if len(county_towns) >= towns_reply["pagination"]["total"]:
            break
        page_number += 1

    len(county_towns)
    return (county_towns,)


@app.cell
def _(county_towns, fiscal_year, requests):
    town_summaries = []

    for town in county_towns:
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

    print(f"{len(town_summaries)} of {len(county_towns)} towns had data for fiscal year {fiscal_year}")
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
    return towns_in_budget, towns_sorted


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


@app.cell
def _():
    ##Going Further Items

    return


@app.cell
def _(towns_in_budget):
    def tax_rate_amount(row):
        return row[2]

    towns_by_rate = sorted(towns_in_budget, key=tax_rate_amount)

    print(f"{'Town':<15}{'Avg Home Value':>16}{'Tax Rate':>12}{'Avg Bill':>12}")

    for _row in towns_by_rate:
        _town, _value, _rate, _bill = _row
        print(f"{_town:<15}{_value:>16,.0f}{_rate:>12.2f}{_bill:>12,.0f}")
    return


@app.cell
def _(county_towns, fiscal_year, requests, towns_sorted):
    lowest_three_names = [row[0] for row in towns_sorted[:3]]

    ten_year_start = fiscal_year - 9

    for _town_name in lowest_three_names:
        _dor_code = None
        for _town in county_towns:
            if _town["name"] == _town_name:
                _dor_code = _town["dor_code"]

        _history_reply = requests.get(
            f"https://oim.zhili.dev/ma/towns/{_dor_code}/history",
            timeout=10,
        ).json()

        print(_town_name)
        for _year_record in _history_reply["years"]:
            if ten_year_start <= _year_record["fiscal_year"] <= fiscal_year:
                _bill = _year_record["average_single_family_bill_dollars"]
                if _bill is None:
                    print(" ", _year_record["fiscal_year"], "no data")
                else:
                    print(" ", _year_record["fiscal_year"], f"${_bill:,}")
        print()
    return lowest_three_names, ten_year_start


@app.cell
def _(county_towns, fiscal_year, lowest_three_names, requests, ten_year_start):
    print("% change in average bill, over the years data is available:")

    for _town_name in lowest_three_names:
        _dor_code = None
        for _town in county_towns:
            if _town["name"] == _town_name:
                _dor_code = _town["dor_code"]

        _history_reply = requests.get(
            f"https://oim.zhili.dev/ma/towns/{_dor_code}/history",
            timeout=10,
        ).json()

        _first_year = None
        _first_bill = None
        _last_year = None
        _last_bill = None

        for _year_record in _history_reply["years"]:
            if ten_year_start <= _year_record["fiscal_year"] <= fiscal_year:
                _bill = _year_record["average_single_family_bill_dollars"]
                if _bill is not None:
                    if _first_bill is None:
                        _first_year = _year_record["fiscal_year"]
                        _first_bill = _bill
                    _last_year = _year_record["fiscal_year"]
                    _last_bill = _bill

        _pct_change = (_last_bill - _first_bill) / _first_bill * 100
        _years_elapsed = _last_year - _first_year
        _pct_change_per_year = _pct_change / _years_elapsed

        print(f"  {_town_name}: {_first_year} (${_first_bill:,}) to {_last_year} (${_last_bill:,}) = {_pct_change:.1f}% total, {_pct_change_per_year:.1f}% per year over {_years_elapsed} years")
    return


@app.cell
def _(county_towns, towns_sorted):
    print("Average bill as a share of income per person:")

    for _row in towns_sorted:
        _town_name, _avg_value, _tax_rate, _avg_bill = _row

        _income_per_capita = None
        for _town in county_towns:
            if _town["name"] == _town_name:
                _income_per_capita = _town["income_per_capita_dollars"]

        _share_of_income = _avg_bill / _income_per_capita * 100
        print(f"  {_town_name}: bill ${_avg_bill:,} / income ${_income_per_capita:,} = {_share_of_income:.1f}%")
    return


if __name__ == "__main__":
    app.run()
