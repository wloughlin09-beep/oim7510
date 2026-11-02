##C · Babson Bean Café

'''mermaid
erDiagram
    MEMBERS ||--o{ ORDERS : places
    ORDERS ||--|{ ORDER_LINES : contains
    PRODUCTS ||--o{ ORDER_LINES : purchased_as


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
'''
    