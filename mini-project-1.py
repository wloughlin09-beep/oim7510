# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.23.3",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of project, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *A home buyer would use this tool to examine different loan rates, repayment scedules and impacts of additonal payments to principle to make a decision on financing options*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    Establish items for the loan amount, different interest rates and years.
    Establish a list to put the payments into with the requested data items
    create a loop where if loan term in months is > 0 and the balance on the loan is > 0 add to the list with payment amount, the caluclated interest, pricipal and the remainder of the balance. Subtract 1 month from loan term and principal payment from balance.
    Run the code, if no errors compare with an excel sheet to confirm numbers.


    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your project from the Mini Project 1 page. If you chose your own project, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    # Your inputs.

    loan_amount = 400000
    annual_rates = {30: 0.0703, 15: 0.0642}
    return annual_rates, loan_amount


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _():
    #my code no AI help, cant get it to round to save my life

    return


@app.cell
def _(annual_rates, loan_amount):
    monthly_payment = round(loan_amount * (annual_rates[30] / 12) / (1 - (1 + annual_rates[30] / 12) ** (-30 * 12)), 2)
    new_balance = loan_amount 
    interest_payment = round(new_balance * (annual_rates[30] / 12), 2)
    principal_payment = round(monthly_payment - interest_payment, 2)
    payment_schedule = []
    remaining_payments = 30 * 12
    while remaining_payments > 1:
            interest_payment = round(new_balance * (annual_rates[30] / 12), 2)
            principal_payment = round(monthly_payment - interest_payment, 2)        
            new_balance -= round(principal_payment, 2)
            payment_schedule.append(monthly_payment, interest_payment, principal_payment, new_balance)
            remaining_payments -= 1
    print(payment_schedule)        
    return


@app.cell
def _():
    #AI HELP
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    total_interest1_30 = 0
    for row in schedule_30:
        total_interest_301 += row[2]

    total_interest1_15 = 0
    for row in schedule_15:
        total_interest1_15 += row[2]

    print(f"30-year total interest: ${total_interest_30:,.2f}")
    print(f"15-year total interest: ${total_interest_15:,.2f}")
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    total_paid_30 = 0
    for row2 in schedule_30:
        total_paid_30 += row2[1]

    check_interest_30 = round(total_paid_30 - loan_amount, 2)

    print(f"Total interest (direct sum): ${total_interest_30:,.2f}")
    print(f"Total interest (payments minus principal): ${check_interest_30:,.2f}")
    """)
    return


@app.cell
def _(loan_amount, months_30, payment_30, rate_30, total_interest_30):
    extra_payment = 200

    schedule_30_extra = []
    balance_30_extra = loan_amount
    month_30_extra = 0

    while balance_30_extra > 0:
        month_30_extra += 1
        interest_30_extra = round(balance_30_extra * rate_30, 2)
        principal_30_extra = round(payment_30 - interest_30_extra + extra_payment, 2)
        if principal_30_extra > balance_30_extra:
            principal_30_extra = balance_30_extra
        balance_30_extra = round(balance_30_extra - principal_30_extra, 2)
        actual_payment_30_extra = round(principal_30_extra + interest_30_extra, 2)
        schedule_30_extra.append([month_30_extra, actual_payment_30_extra, interest_30_extra, principal_30_extra, balance_30_extra])

    total_interest_30_extra = 0
    for row3 in schedule_30_extra:
        total_interest_30_extra += row3[2]

    months_saved_30 = months_30 - month_30_extra
    interest_saved_30 = round(total_interest_30 - total_interest_30_extra, 2)

    print(f"30-year with extra $200/month: paid off in {month_30_extra} months, saving {months_saved_30} months")
    print(f"Interest saved: ${interest_saved_30:,.2f}")
    return


@app.cell
def _(schedule_30):
    balance_at_60 = schedule_30[59][4]
    balance_at_60
    return (balance_at_60,)


@app.cell
def _(balance_at_60, months_30):
    rate_refi = 0.06 / 12
    months_refi = months_30 - 60

    payment_refi = round(balance_at_60 * rate_refi / (1 - (1 + rate_refi) ** (-months_refi)), 2)

    schedule_refi = []
    balance_refi = balance_at_60

    for month_refi in range(1, months_refi + 1):
        interest_refi = round(balance_refi * rate_refi, 2)
        principal_refi = round(payment_refi - interest_refi, 2)
        if month_refi == months_refi or principal_refi > balance_refi:
            principal_refi = balance_refi
        balance_refi = round(balance_refi - principal_refi, 2)
        actual_payment_refi = round(principal_refi + interest_refi, 2)
        schedule_refi.append([month_refi, actual_payment_refi, interest_refi, principal_refi, balance_refi])

    schedule_refi
    return months_refi, schedule_refi


@app.cell
def _(months_refi, schedule_30, schedule_refi):
    refinance_cost = 6000
    cumulative_savings = -refinance_cost
    breakeven_month = None

    for i in range(months_refi):
        original_interest = schedule_30[60 + i][2]
        refi_interest = schedule_refi[i][2]
        cumulative_savings += (original_interest - refi_interest)
        if cumulative_savings > 0 and breakeven_month is None:
            breakeven_month = 60 + i + 1

    print(f"Refinance savings overtake the $6,000 cost in month {breakeven_month}")
    return


@app.cell
def _(rate_15_input, rate_30_input):
    annual_rates = {30: rate_30_input.value / 100, 15: rate_15_input.value / 100}
    return (annual_rates,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(mo):
    loan_amount_input = mo.ui.slider(50000, 1000000, value=350000, step=5000, label="Loan amount ($)")
    rate_30_input = mo.ui.slider(4.0, 9.0, value=7.03, step=0.01, label="30-year rate (%)")
    rate_15_input = mo.ui.slider(4.0, 9.0, value=6.42, step=0.01, label="15-year rate (%)")
    extra_payment_input = mo.ui.slider(0, 1000, value=200, step=25, label="Extra payment per month ($)")

    mo.vstack([loan_amount_input, rate_30_input, rate_15_input, extra_payment_input])
    return rate_15_input, rate_30_input


@app.cell
def _(loan_amount, rate_15_input, rate_30_input):
    rate_15 = rate_15_input.value / 100
    months_15 = 15 * 12
    payment_15 = round(loan_amount * rate_15 / 12 / (1 - (1 + rate_15 / 12) ** (-months_15)), 2)

    schedule_15 = []
    balance_15 = loan_amount

    for month_15 in range(1, months_15 + 1):
        interest_15 = round(balance_15 * rate_15 / 12, 2)
        principal_15 = round(payment_15 - interest_15, 2)
        if month_15 == months_15 or principal_15 > balance_15:
            principal_15 = balance_15
        balance_15 = round(balance_15 - principal_15, 2)
        actual_payment_15 = round(principal_15 + interest_15, 2)
        schedule_15.append([month_15, actual_payment_15, interest_15, principal_15, balance_15])

    schedule_15

    rate_30 = rate_30_input.value / 100
    months_30 = 30 * 12
    payment_30 = round(loan_amount * rate_30 / (1 - (1 + rate_30) ** (-months_30)), 2)

    schedule_30 = []
    balance_30 = loan_amount

    for month_30 in range(1, months_30 + 1):
        interest_30 = round(balance_30 * rate_30, 2)
        principal_30 = round(payment_30 - interest_30, 2)
        if month_30 == months_30 or principal_30 > balance_30:
            principal_30 = balance_30
        balance_30 = round(balance_30 - principal_30, 2)
        actual_payment_30 = round(principal_30 + interest_30, 2)
        schedule_30.append([month_30, actual_payment_30, interest_30, principal_30, balance_30])

    schedule_30


    total_interest_15 = 0
    for row5 in schedule_15:
        total_interest_15 += row5[2]
    print(f"15-year total interest: ${total_interest_15:,.2f}")

    total_interest_30 = 0
    for row6 in schedule_30:
        total_interest_30 += row6[2]
    print(f"30-year total interest: ${total_interest_30:,.2f}") 
    return months_30, payment_30, rate_30, schedule_30, total_interest_30


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


if __name__ == "__main__":
    app.run()
