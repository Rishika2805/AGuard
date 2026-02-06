from agents.orchestrator import collect_all_data
from agents.preprocessor import preprocessor

def main():
    items = collect_all_data()

    for item in items:
        item = preprocessor(item)
        print(item["source"], item["word_count"], item["has_links"])


if __name__ == "__main__":
    main()