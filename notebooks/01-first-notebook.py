# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "matplotlib",
# ]
# ///
"""Set up your machine and push a notebook.

Session 1 of OIM7510 and OIM6301, second half.

Nothing here reads a data file and nothing here needs the network.

AUTHORING NOTES.

Every markdown cell carries `hide_code=True`, so a student sees the rendered
prose without the `mo.md` wrapper around it. Keep it on any cell that is only
markdown, and leave it off any cell whose code a student should read.

The four experiments ask a student to edit, delete and reorder cells, which
`--mode run` cannot do. This is written for `marimo edit` on the student's own
machine, which is what session 1 spends an hour setting up. A published copy has
to be exported `--mode edit`, and whether an edited cell re-executes there is
still unsettled: `.claude/rules/marimo-notebooks.md`.
"""

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Set Up Your Machine and Push a Notebook""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ▶️ A Name Holding Several Things

    A name holds a value. `=` puts the value there. Read it as *put this in that*.

    The five numbers below are the freight charged on orders `10248` through
    `10252`. Order `10248` is the one from the slides.
    """)
    return


@app.cell
def _():
    freight_charges = [16.75, 22.25, 25.00, 20.25, 36.25]
    freight_charges
    return (freight_charges,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ✏️ Add Three Cells

    Add three cells below with the **+** button. Put one line in each.

    1. The freight on the **first** order: `freight_charges[0]`
    2. **How many** orders there are: `len(freight_charges)`
    3. The **total**: `total = sum(freight_charges)`, then `total` on the next line

    Keep them in separate cells. The next section depends on it.

    *Python counts from zero, so `freight_charges[0]` is the first one.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🙋 Four Questions

    Write all four answers down before you run anything.

    1. Cell A says `x = 5`. Cell B says `print(x)`. You change A to `x = 50`.
       **What does B print?**
    2. Cell A says `orders = 3`. Cell B says `orders * 12`. You **delete cell A**.
       **What happens to B?**
    3. Two different cells both say `total = ...`. **What happens?**
    4. You put `print(total)` **above** the cell that says `total = 5`.
       **Does it run?**

    Four experiments follow. Do them in order, and undo each one before the next.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Experiment 1

    Change `16.75` to `999.99` in the `freight_charges` cell. Run only that cell.

    Watch your three cells.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Experiment 2

    Delete the `freight_charges` cell. Watch your three cells.

    Then bring it back: undo, or type the line again.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Experiment 3

    Add a cell anywhere and put `total = 1` in it.

    Delete it again once you have seen what happens.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Experiment 4

    Drag the cell holding `total = sum(freight_charges)` **below** the cell that shows
    `total`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ▶️ What Happened

    1. **Everything that used the number recomputed by itself.** You ran one cell.
    2. **The cells using the deleted name went blank.** No cell keeps showing a value
       whose source is gone.
    3. **You got an error.** A name is defined in exactly one cell, so you can never
       be looking at a `total` that some other cell changed.
    4. **It ran.** This notebook works out what depends on what and runs in that
       order. Where a cell sits on the page is a layout choice.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ▶️ A Second Name

    `orders` holds the five order numbers, each in the same position as its charge.
    """)
    return


@app.cell
def _():
    orders = [10248, 10249, 10250, 10251, 10252]
    orders
    return (orders,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🙋 Explore

    One line per cell. Write down what you expect before you run it.

    1. `freight_charges[-1]`
    2. `freight_charges[:3]`
    3. `orders[0]` and `freight_charges[0]`. What do those two have in common?
    4. `category = "Confections"`, then `len(category)`. `len` counted five things a moment ago. What is it counting now?
    5. `sum(orders)`. It runs. Should it?
    6. `orders * 2`, then `orders + freight_charges`. Neither one is an error.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 📈 The Same Five Numbers, as Bars

    > **Advanced.** Nothing later depends on this. Skip it if the installs are still fighting you.

    Change a number in `freight_charges` and the bars move on their own.
    """)
    return


@app.cell
def _(freight_charges, orders):
    import matplotlib.pyplot as plt

    _fig, _ax = plt.subplots(figsize=(6, 2.6))
    _ax.bar([str(_o) for _o in orders], freight_charges)
    _ax.set_ylabel("freight")
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🧭 The Three Answers From the Slides

    > **Advanced.** Nothing later depends on this.

    A **dictionary** holds values you look up by name instead of by position. It is also
    the shape data arrives in from the web, which is where session 4 starts.

    `dairy` holds the three splits of order 10248's $16.75 you saw on the slides.
    """)
    return


@app.cell
def _():
    dairy = {"by value": 13.02, "by units": 10.55, "split evenly": 8.38}
    dairy["by value"]
    return (dairy,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In new cells:

    1. `dairy["split evenly"]`
    2. `list(dairy)`, then `list(dairy.values())`
    3. Draw them. Copy the two plotting lines from the chart above, and put `list(dairy)` and `list(dairy.values())` in place of `orders` and `freight_charges`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ✏️ Push It

    1. Change one number in the `freight_charges` list. Watch your three cells update.
    2. Save the file **inside your repository, in the `notebooks/` folder**.
    3. In **GitHub Desktop**: write a commit message, click **Commit to main**,
       then **Push origin**.
    4. Open **github.com**, go to your repository, and click on the notebook.

    *Nothing there? Check that GitHub Desktop is showing the right repository at
    the top left, and that the file you saved is inside that repository's folder.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🚀 Ask For a Line You Could Not Write

    You have five freight charges and three lines of Python.

    1. **Pick something about `freight_charges` the cells above do not show**, such as the average, the largest, or how many are above 22.
    2. **Ask your agent for it.** Show it the list and state what you want back.
    3. **Paste what it gives you into a new cell and run it.** If it errors, keep the error.
    4. **Add a markdown cell underneath.** What does the line do, in your words, and which part of it are you unsure about?
    5. **Commit and push.**

    *New to markdown? The [Markdown guide](https://oim7510.github.io/guides/markdown/) is a ten-minute read, and we cover it properly next session.*
    """)
    return


if __name__ == "__main__":
    app.run()
