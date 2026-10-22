
from Catalog_Data import BOOKS, validate_book_ids



def find_Book(records, book_id):
    for book in records:
        if book["id"] == book_id:
            return book
    return None


def build_index(records):
    index = {}
    for book in records:
        index[book["id"]] = book
    return index


def indexed_lookup(index, book_id):

    if book_id in index:
        return index[book_id]
    return None


def record_builder(size):
    return [{"id": book_id} for book_id in range(size)]


def find_Book(records, book_id):
    comparisons = 0
    for book in records:
        if book["id"] == book_id:
            return book
    return None


def main():
    validate_book_ids(BOOKS)
    index = build_index(BOOKS)

    for book in BOOKS:
        book_id = book["id"]
        scan_result = find_Book(BOOKS, book_id)
        index_result = indexed_lookup(index, book_id)
        print("Looking up", book_id)
        print("  Same answer from both lookups:", scan_result == index_result)
        if scan_result is None:
            print("  Not found.")
        else:
            print("  ID:", scan_result["id"])
            print("  Title:", scan_result["title"])
            print("  Author:", scan_result["author"])

    print("\nWhen every query misses:")
    # Two fixed queries stay O(n); n queries become O(n^2).
    for size in (4, 8):
        scan_result = find_Book(record_builder(size), -1)
        print(
            f"n={size}: 2 fixed queries -> {2}; n queries -> {size * 1}"
        )
    print("Fixed q: O(n). If q grows with n: O(n^2).")





if __name__ == "__main__":
    main()