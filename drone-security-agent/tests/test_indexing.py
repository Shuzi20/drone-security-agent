import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from storage.db_handler import init_db, insert_frame, search_frames, get_all_frames

def test_insert_and_retrieve():
    init_db()
    insert_frame(99, "01:00", "Test Gate", "A red car parked outside", "car", "LOW")
    results = get_all_frames()
    ids = [r[0] for r in results]
    assert 99 in ids
    print("PASS — test_insert_and_retrieve")

def test_search_by_keyword():
    init_db()
    insert_frame(98, "02:00", "Garage", "Blue truck seen entering", "truck", "MEDIUM")
    results = search_frames("truck")
    assert len(results) > 0
    print("PASS — test_search_by_keyword")

def test_search_no_result():
    init_db()
    results = search_frames("elephant")
    assert len(results) == 0
    print("PASS — test_search_no_result")

if __name__ == "__main__":
    test_insert_and_retrieve()
    test_search_by_keyword()
    test_search_no_result()
    print("\nAll indexing tests passed!")