from agents.orchestrator import collect_all_data
from database.repos.content_repo import insert_content

def main():
    items = collect_all_data()

    inserted = 0
    skipped = 0

    for item in items:
        if insert_content(item):
            inserted += 1
        else:
            skipped += 1

    print(f'\n\nInserted : {inserted}')
    print(f'Skipped : {skipped}')

if __name__ == "__main__":
    main()