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
    return


if __name__ == "__main__":
    app.run()
