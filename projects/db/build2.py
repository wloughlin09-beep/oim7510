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
        available_today  BOOLEAN NOT NULL DEFAULT TRUE,
        CHECK (price >= cost)
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
        method      VARCHAR NOT NULL CHECK (method IN ('cash', 'card', 'app', 'points')),
        amount      DECIMAL(10,2) NOT NULL CHECK (amount > 0)
    );""")
    return


if __name__ == "__main__":
    app.run()
