import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from storage.db_handler import init_db, insert_frame, search_frames, get_all_frames

def test_db_initializes():
    init_db()
    frames = get_all_frames()
    assert isinstance(frames, list)
    print("PASS — test_db_initializes")

def test_insert_frame1():
    init_db()
    insert_frame(1, "00:01", "Main Gate",
                 "A person in dark clothing standing near main gate",
                 "person", "MEDIUM")
    results = get_all_frames()
    ids = [r[0] for r in results]
    assert 1 in ids
    print("PASS — test_insert_frame1")

def test_insert_frame6():
    init_db()
    insert_frame(6, "23:58", "Main Gate",
                 "Unknown person attempting to open the main gate at night",
                 "person, main gate", "HIGH")
    results = get_all_frames()
    ids = [r[0] for r in results]
    assert 6 in ids
    print("PASS — test_insert_frame6")

def test_search_by_person():
    init_db()
    insert_frame(1, "00:01", "Main Gate",
                 "A person in dark clothing standing near main gate",
                 "person", "MEDIUM")
    results = search_frames("person")
    assert len(results) > 0
    print("PASS — test_search_by_person")

def test_search_by_truck():
    init_db()
    insert_frame(2, "00:03", "Garage",
                 "A blue Ford F150 truck entered the garage",
                 "blue Ford F150 truck", "NONE")
    results = search_frames("truck")
    assert len(results) > 0
    print("PASS — test_search_by_truck")

def test_search_by_location():
    init_db()
    insert_frame(1, "00:01", "Main Gate",
                 "Person loitering at main gate",
                 "person", "MEDIUM")
    results = search_frames("Main Gate")
    assert len(results) > 0
    print("PASS — test_search_by_location")

def test_search_no_result():
    init_db()
    results = search_frames("elephant")
    assert len(results) == 0
    print("PASS — test_search_no_result")

def test_insert_replace_same_frame():
    init_db()
    insert_frame(99, "01:00", "Backyard", "First insert", "people", "NONE")
    insert_frame(99, "01:00", "Backyard", "Updated insert", "people", "LOW")
    results = [r for r in get_all_frames() if r[0] == 99]
    assert len(results) == 1
    assert results[0][5] == "LOW"
    print("PASS — test_insert_replace_same_frame")

if __name__ == "__main__":
    test_db_initializes()
    test_insert_frame1()
    test_insert_frame6()
    test_search_by_person()
    test_search_by_truck()
    test_search_by_location()
    test_search_no_result()
    test_insert_replace_same_frame()
    print("\nAll indexing tests passed!")