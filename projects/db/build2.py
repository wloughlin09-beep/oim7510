import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb

    return duckdb, mo


@app.cell
def _(duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (database,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##The Tables
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(f"""DROP TABLE IF EXISTS payments;
    DROP TABLE IF EXISTS line_options;
    DROP TABLE IF EXISTS order_lines;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS options;
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS members;

    CREATE TABLE members (
        member_id       VARCHAR PRIMARY KEY,
        first_name      VARCHAR NOT NULL,
        mobile_number   VARCHAR NOT NULL,
        email           VARCHAR,
        join_date       DATE NOT NULL,
        points_balance  INTEGER NOT NULL DEFAULT 0
    );

    CREATE TABLE products (
        product_id       VARCHAR PRIMARY KEY,
        product_name     VARCHAR NOT NULL,
        category         VARCHAR NOT NULL CHECK (category IN ('coffee', 'tea', 'food', 'other')),
        price            DECIMAL(10,2) NOT NULL,
        cost             DECIMAL(10,2) NOT NULL,
        available_today  BOOLEAN NOT NULL DEFAULT TRUE
    );

    CREATE TABLE options (
        option_id    VARCHAR PRIMARY KEY,
        option_name  VARCHAR NOT NULL,
        price        DECIMAL(10,2) NOT NULL CHECK (price >= 0),
        cost         DECIMAL(10,2) NOT NULL
    );

    CREATE TABLE orders (
        order_id        VARCHAR PRIMARY KEY,
        order_datetime  TIMESTAMP NOT NULL,
        member_id       VARCHAR REFERENCES members(member_id),
        channel         VARCHAR NOT NULL CHECK (channel IN ('counter', 'app'))
    );

    CREATE TABLE order_lines (
        order_line_id  VARCHAR PRIMARY KEY,
        order_id       VARCHAR NOT NULL REFERENCES orders(order_id),
        product_id     VARCHAR NOT NULL REFERENCES products(product_id),
        quantity       INTEGER NOT NULL CHECK (quantity > 0),
        unit_price     DECIMAL(10,2) NOT NULL
    );

    CREATE TABLE line_options (
        order_line_id  VARCHAR NOT NULL REFERENCES order_lines(order_line_id),
        option_id      VARCHAR NOT NULL REFERENCES options(option_id),
        unit_price     DECIMAL(10,2) NOT NULL,
        PRIMARY KEY (order_line_id, option_id)
    );

    CREATE TABLE payments (
        payment_id  VARCHAR PRIMARY KEY,
        order_id    VARCHAR NOT NULL REFERENCES orders(order_id),
        method      VARCHAR NOT NULL,
        amount      DECIMAL(10,2) NOT NULL CHECK (amount > 0)
    );""")
    return


@app.cell
def _(
    _line_options_view,
    _members_view,
    _options_view,
    _order_lines_view,
    _orders_view,
    _payments_view,
    _products_view,
    duckdb,
    line_options,
    members,
    mo,
    options,
    order_lines,
    orders,
    payments,
    pl,
    products,
):
    _data_dir = mo.notebook_dir() / "data"

    _members = pl.read_csv(_data_dir / "members.csv")
    _products = pl.read_csv(_data_dir / "products.csv")
    _options = pl.read_csv(_data_dir / "options.csv")
    _orders = pl.read_csv(_data_dir / "orders.csv", try_parse_dates=True)
    _order_lines = pl.read_csv(_data_dir / "order_lines.csv")
    _line_options = pl.read_csv(_data_dir / "line_options.csv")
    _payments = pl.read_csv(_data_dir / "payments.csv")

    # duckdb.register makes a polars table visible to SQL under a name, so we
    # can SELECT it straight into a real table in the database
    duckdb.register("_members_view", _members)
    duckdb.register("_products_view", _products)
    duckdb.register("_options_view", _options)
    duckdb.register("_orders_view", _orders)
    duckdb.register("_order_lines_view", _order_lines)
    duckdb.register("_line_options_view", _line_options)
    duckdb.register("_payments_view", _payments)

    duckdb.sql("DELETE FROM payments")
    duckdb.sql("DELETE FROM line_options")
    duckdb.sql("DELETE FROM order_lines")
    duckdb.sql("DELETE FROM orders")
    duckdb.sql("DELETE FROM options")
    duckdb.sql("DELETE FROM products")
    duckdb.sql("DELETE FROM members")

    duckdb.sql("INSERT INTO members SELECT * FROM _members_view")
    duckdb.sql("INSERT INTO products SELECT * FROM _products_view")
    duckdb.sql("INSERT INTO options SELECT * FROM _options_view")
    duckdb.sql("INSERT INTO orders SELECT * FROM _orders_view")
    duckdb.sql("INSERT INTO order_lines SELECT * FROM _order_lines_view")
    duckdb.sql("INSERT INTO line_options SELECT * FROM _line_options_view")
    duckdb.sql("INSERT INTO payments SELECT * FROM _payments_view")

    print("loaded members:", len(_members))
    print("loaded products:", len(_products))
    print("loaded options:", len(_options))
    print("loaded orders:", len(_orders))
    print("loaded order_lines:", len(_order_lines))
    print("loaded line_options:", len(_line_options))
    print("loaded payments:", len(_payments))


    _bad_price = _products.filter(pl.col("price") < pl.col("cost"))
    print()
    print(f"products where price < cost ({len(_bad_price)} rows):")
    print(_bad_price)

    _bad_method = _payments.filter(~pl.col("method").is_in(["cash", "card", "app", "points"]))
    print()
    print(f"payments with a method not in (cash, card, app, points) ({len(_bad_method)} rows):")
    print(_bad_method)
    return


@app.cell
def _(database, duckdb):
    # write the in-memory tables out to a real file on disk, so the ask()
    # function (which opens the file itself) can see this data too; ATTACH
    # lets one connection reach into a second database file at the same time.
    # We use duckdb.query(...) here instead of duckdb.sql(...), because marimo
    # reads .sql(...) calls to build its dataflow graph, and this step is only
    # a one-way export, not a definition this notebook should track as data.
    _file_path = str(database)

    duckdb.query(f"ATTACH '{_file_path}' AS filedb")
    duckdb.query("DROP TABLE IF EXISTS filedb.payments")
    duckdb.query("DROP TABLE IF EXISTS filedb.line_options")
    duckdb.query("DROP TABLE IF EXISTS filedb.order_lines")
    duckdb.query("DROP TABLE IF EXISTS filedb.orders")
    duckdb.query("DROP TABLE IF EXISTS filedb.options")
    duckdb.query("DROP TABLE IF EXISTS filedb.products")
    duckdb.query("DROP TABLE IF EXISTS filedb.members")

    duckdb.query("CREATE TABLE filedb.members AS SELECT * FROM members")
    duckdb.query("CREATE TABLE filedb.products AS SELECT * FROM products")
    duckdb.query("CREATE TABLE filedb.options AS SELECT * FROM options")
    duckdb.query("CREATE TABLE filedb.orders AS SELECT * FROM orders")
    duckdb.query("CREATE TABLE filedb.order_lines AS SELECT * FROM order_lines")
    duckdb.query("CREATE TABLE filedb.line_options AS SELECT * FROM line_options")
    duckdb.query("CREATE TABLE filedb.payments AS SELECT * FROM payments")

    duckdb.query("DETACH filedb")
    print("wrote tables to", _file_path)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##A Look at the Data
    """)
    return


@app.cell
def _(mo):
    import polars as pl

    orders_raw = pl.read_csv(mo.notebook_dir() / "data" / "orders.csv", try_parse_dates=True)
    orders_raw.head()
    return orders_raw, pl


@app.cell
def _(orders_raw, pl):
    orders_by_hour = (
        orders_raw
        .with_columns(pl.col("order_datetime").dt.hour().alias("hour"))
        .group_by("hour")
        .agg(pl.len().alias("num_orders"))
        .sort("hour")
    )
    orders_by_hour
    return (orders_by_hour,)


@app.cell
def _(orders_by_hour):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.bar(orders_by_hour["hour"], orders_by_hour["num_orders"])
    ax.set_xlabel("hour of day")
    ax.set_ylabel("number of orders")
    ax.set_title("Orders by hour of day")
    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Real business data for a cafe would not look like this the origional data, you would expect sharp spikes in the morning and early afternoon, this is mostly flat, I changed the make data file to generate more realistic data by adding weighting to typical peak periods. Once that change was made the data looks more true to life.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##Row Counts
    """)
    return


@app.cell
def _(
    line_options,
    members,
    mo,
    options,
    order_lines,
    orders,
    payments,
    products,
):
    row_counts = mo.sql(
        f"""
        SELECT 'members' AS table_name, COUNT(*) AS num_rows FROM members
        UNION ALL SELECT 'products', COUNT(*) FROM products
        UNION ALL SELECT 'options', COUNT(*) FROM options
        UNION ALL SELECT 'orders', COUNT(*) FROM orders
        UNION ALL SELECT 'order_lines', COUNT(*) FROM order_lines
        UNION ALL SELECT 'line_options', COUNT(*) FROM line_options
        UNION ALL SELECT 'payments', COUNT(*) FROM payments
        ORDER BY table_name
        """
    )
    return


if __name__ == "__main__":
    app.run()
