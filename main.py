from re import findall

from agents.orchestrator import collect_all_data
from database.repos.content_repo import insert_content
from database.db import get_connection

def main():
    items = collect_all_data()

    conn = get_connection()
    cursor = conn.cursor()

    inserted = 0
    skipped = 0
    try:
        for item in items:
            if insert_content(item,cursor):
                inserted += 1
            else:
                skipped += 1

        conn.commit()
    finally:
        cursor.close()
        conn.close()

    print(f'\n\nInserted : {inserted}')
    print(f'Skipped : {skipped}')


if __name__ == "__main__":
    main()