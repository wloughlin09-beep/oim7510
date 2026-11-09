##C · Babson Bean Café

```mermaid
erDiagram
    MEMBERS |o--o{ ORDERS : places
    ORDERS ||--|{ ORDER_LINES : contains
    PRODUCTS ||--o{ ORDER_LINES : purchased_as
    ORDER_LINES ||--o{ LINE_OPTIONS : carries
    OPTIONS ||--o{ LINE_OPTIONS : applied_on
    ORDERS ||--|{ PAYMENTS : paid_by

    MEMBERS {
        string member_id PK
        string first_name
        string mobile_number
        string email
        date join_date
        int points_balance
    }

    PRODUCTS {
        string product_id PK
        string product_name
        string category
        decimal price
        decimal cost
        boolean available_today
    }

    OPTIONS {
        string option_id PK
        string option_name
        decimal price
        decimal cost
    }

    ORDERS {
        string order_id PK
        datetime order_datetime
        string member_id FK
        string channel
    }

    ORDER_LINES {
        string order_line_id PK
        string order_id FK
        string product_id FK
        int quantity
        decimal unit_price
    }

    LINE_OPTIONS {
        string order_line_id PK, FK
        string option_id PK, FK
        decimal unit_price
    }

    PAYMENTS {
        string payment_id PK
        string order_id FK
        string method
        decimal amount
    }
```
    
## One row of members is one loyalty member and their contact and points info.
## One row of products is one item on the menu.
## One row of options is one add-on a drink can carry.
## One row of orders is one order, placed by a member or not.
## One row of order_lines is one product ordered on one order.
## One row of line_options is one option charged on one order line.
## One row of payments is one amount paid toward one order.

Which key you chose where the business already had one, such as an email or a ticker, and why. - I chose differnet keys from what the business already had in the case of members, where an email or phone number because those can change with time and thus are not appropriate as a pk which shoudl be stataic. 
Which relationships are optional, and what in the scenario tells you so. - Members to orders is an optional relationship because not all customers to the shop will be members and thus can have a null value. Also Order_lines to Line_options is optional because a none is also a valid response where there is no customization 
Which of the scenario's rules your tables cannot hold, and how you will check it instead. -- The biggest is the order's payments must add to the order's total, because it spans several tables CHECK constriant can't work so this must be checked with a Query that sums the order_id's payment amount against the order_lines quanitiy ordered and the product's price. 
And one thing your agent proposed for the design that you changed or did not take - the agest wanted Line_Options to have its own surrogate PK but I went to a composite key of order_line_ID and option_id to reduce the amount of id's to manage. 