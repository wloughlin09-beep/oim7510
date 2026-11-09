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

    _file_path = str(database)

    duckdb.query(f"ATTACH '{_file_path}' AS filedb")
    duckdb.query("USE filedb")

    duckdb.query("DROP TABLE IF EXISTS payments")
    duckdb.query("DROP TABLE IF EXISTS line_options")
    duckdb.query("DROP TABLE IF EXISTS order_lines")
    duckdb.query("DROP TABLE IF EXISTS orders")
    duckdb.query("DROP TABLE IF EXISTS options")
    duckdb.query("DROP TABLE IF EXISTS products")
    duckdb.query("DROP TABLE IF EXISTS members")

    duckdb.query("""
        CREATE TABLE members (
            member_id       VARCHAR PRIMARY KEY,
            first_name      VARCHAR NOT NULL,
            mobile_number   VARCHAR NOT NULL,
            email           VARCHAR,
            join_date       DATE NOT NULL,
            points_balance  INTEGER NOT NULL DEFAULT 0
        )
    """)

    duckdb.query("""
        CREATE TABLE products (
            product_id       VARCHAR PRIMARY KEY,
            product_name     VARCHAR NOT NULL,
            category         VARCHAR NOT NULL CHECK (category IN ('coffee', 'tea', 'food', 'other')),
            price            DECIMAL(10,2) NOT NULL,
            cost             DECIMAL(10,2) NOT NULL,
            available_today  BOOLEAN NOT NULL DEFAULT TRUE
        )
    """)

    duckdb.query("""
        CREATE TABLE options (
            option_id    VARCHAR PRIMARY KEY,
            option_name  VARCHAR NOT NULL,
            price        DECIMAL(10,2) NOT NULL CHECK (price >= 0),
            cost         DECIMAL(10,2) NOT NULL
        )
    """)

    duckdb.query("""
        CREATE TABLE orders (
            order_id        VARCHAR PRIMARY KEY,
            order_datetime  TIMESTAMP NOT NULL,
            member_id       VARCHAR REFERENCES members(member_id),
            channel         VARCHAR NOT NULL CHECK (channel IN ('counter', 'app'))
        )
    """)

    duckdb.query("""
        CREATE TABLE order_lines (
            order_line_id  VARCHAR PRIMARY KEY,
            order_id       VARCHAR NOT NULL REFERENCES orders(order_id),
            product_id     VARCHAR NOT NULL REFERENCES products(product_id),
            quantity       INTEGER NOT NULL CHECK (quantity > 0),
            unit_price     DECIMAL(10,2) NOT NULL
        )
    """)

    duckdb.query("""
        CREATE TABLE line_options (
            order_line_id  VARCHAR NOT NULL REFERENCES order_lines(order_line_id),
            option_id      VARCHAR NOT NULL REFERENCES options(option_id),
            unit_price     DECIMAL(10,2) NOT NULL,
            PRIMARY KEY (order_line_id, option_id)
        )
    """)

    duckdb.query("""
        CREATE TABLE payments (
            payment_id  VARCHAR PRIMARY KEY,
            order_id    VARCHAR NOT NULL REFERENCES orders(order_id),
            method      VARCHAR NOT NULL,
            amount      DECIMAL(10,2) NOT NULL CHECK (amount > 0)
        )
    """)

    # load in an order that respects every foreign key above; "memory" is the
    # name duckdb gives the notebook's original in-memory database
    duckdb.query("INSERT INTO members SELECT * FROM memory.members")
    duckdb.query("INSERT INTO products SELECT * FROM memory.products")
    duckdb.query("INSERT INTO options SELECT * FROM memory.options")
    duckdb.query("INSERT INTO orders SELECT * FROM memory.orders")
    duckdb.query("INSERT INTO order_lines SELECT * FROM memory.order_lines")
    duckdb.query("INSERT INTO line_options SELECT * FROM memory.line_options")
    duckdb.query("INSERT INTO payments SELECT * FROM memory.payments")

    duckdb.query("USE memory")
    duckdb.query("DETACH filedb")
    print("wrote tables (with their rules) to", _file_path)
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


@app.cell
def _(mo):
    mo.md(r"""
    ##A Row It Refuses
    """)
    return


@app.cell
def _(database, duckdb):
    # A row it refuses: try to insert an order line with quantity 0, which
    # breaks the rule "a quantity is more than zero". ask() only reads, using
    # a read-only connection, so this insert opens its own short write
    # connection instead, and closes it right away.
    try:
        with duckdb.connect(database) as _con:
            _con.execute("""
                INSERT INTO order_lines (order_line_id, order_id, product_id, quantity, unit_price)
                VALUES ('OL999999', 'OR00001', 'PR001', 0, 3.50)
            """)
        rejected_row_message = "no error: the row was inserted (unexpected)"
    except Exception as e:
        rejected_row_message = str(e)

    print(rejected_row_message)
    return


if __name__ == "__main__":
    app.run()
