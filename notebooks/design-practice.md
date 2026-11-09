    ```mermaid
erDiagram
    SHOW ||--o{ SHOW_GENRE : "categorized as"
    GENRE ||--o{ SHOW_GENRE : "includes"

    SHOW ||--o{ SHOW_CREW : "involves"
    PERSON ||--o{ SHOW_CREW : "participates in"
    ROLE ||--o{ SHOW_CREW : "defines capacity"

    SHOW {
        int show_id PK
        string title
        int release_year
        string show_type "e.g., TV series"
        string genre
        int episode_count
        decimal rating "nullable"
        int vote_count "default 0"
    }

    PERSON {
        int person_id PK
        string full_name
        int birth_date "nullable"
    }

    ROLE {
        int role_id PK
        string role_name "e.g., 'Star', 'Writer', 'Director'"
    }

    SHOW_CREW {
        int show_id PK, FK
        int person_id PK, FK
        int role_id PK, FK
    }

    GENRE {
        int genre_id PK
        string genre_name "e.g., 'Comedy'"
    }

    SHOW_GENRE {
        int show_id PK, FK
        int genre_id PK, FK
    }
   ```