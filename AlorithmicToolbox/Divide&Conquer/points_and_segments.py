from collections import namedtuple
import bisect


def count_segments_binary(starts, ends, points):
    """ Faster algorithm for counting the number of segments each 
        point is contained in by using binary search.
    """
    assert len(starts) == len(ends)

    count = [0] * len(points)
    starts = sorted(starts)
    ends = sorted(ends)

    total_segments = len(starts)
    # Find the number of segments that do not cover the point
    for index, pnt in enumerate(points):
        right_segments = bisect.bisect_left(ends, pnt)
        left_segments = total_segments - bisect.bisect_right(starts, pnt)
        count[index] = total_segments - right_segments - left_segments

    return count


# Named tuple to store a point, left or right segment. Type can be
# l if is the start of a segment, r if is the end of a segment and
# p if it's a point.
Event = namedtuple("Event", ["coordinate", "type", "index"]) 


def count_segments_sort(starts, ends, points):
    """ Faster algorithm for counting the number of segments each 
        point is contained in by sorting all points.
    """
    assert len(starts) == len(ends)

    count = [0] * len(points)
    events = []
    for ii in range(len(starts)):
        events.append(Event(starts[ii], "l", ii))
        events.append(Event(ends[ii], "r", ii))
    for ii in range(len(points)):
        events.append(Event(points[ii], "p", ii))

    events = sorted(events)
    num_segments = 0
    for e in events:
        if e.type == "l":
            num_segments += 1
        elif e.type == "p":
            count[e.index] = num_segments
        elif e.type == "r":
            num_segments -= 1

    return count


def naive_count_segments(starts, ends, points):
    """ Brute force algorithm for counting the number of segments each 
        point is contained in.
    """
    count = [0] * len(points)
    for ii in range(len(points)):
        for jj in range(len(starts)):
            if starts[jj] <= points[ii] <= ends[jj]:
                count[ii] += 1
    return count


def test_count_segments(count_function):

    print(f"\nTesting count segments {count_function.__name__}")

    starts = [0, 7]
    ends = [5, 10]
    points = [1, 6, 11]
    count = count_function(starts, ends, points)
    assert count == [1, 0, 0], f"Wrong count expected {[1, 0, 0]} got {count}"
    print("Test Case 1 success")

    starts = [-10]
    ends = [10]
    points = [-100, 100, 0]
    count = count_function(starts, ends, points)
    assert count == [0, 0, 1], f"Wrong count expected {[0, 0, 1]} got {count}"
    print("Test Case 2 success")

    starts = [0, -3, 7]
    ends = [5, 2, 10]
    points = [1, 6]
    count = count_function(starts, ends, points)
    assert count == [2, 0], f"Wrong count expected {[2, 0]} got {count}"
    print("Test Case 3 success")

    starts = [4, 1]
    ends = [10, 8]
    points = [11, 7, 3]
    count = count_function(starts, ends, points)
    assert count == [0, 2, 1], f"Wrong count expected {[1, 2, 0]} got {count}"
    print("Test Case 4 success")

    starts = [1, 3]
    ends = [3, 7]
    points = [3]
    count = count_function(starts, ends, points)
    assert count == [2], f"Wrong count expected {[2]} got {count}"
    print("Test Case 5 success")


def main():
    
    test_count_segments(naive_count_segments)
    test_count_segments(count_segments_sort)
    test_count_segments(count_segments_binary)
    

if __name__ == '__main__':
    main()
