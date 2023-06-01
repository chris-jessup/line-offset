import sys
from itertools import count # An infinite list to zip against
from bisect import bisect_right


def make_forward_index(data):
    """
    Returns a sortd list that allows you to query
    which line and column an offset is in a file
    """

    data = data.splitlines(keepends=True)

    cumulative = 0
    ret = []
    for line, lineno in zip(data, count(1)):
        ret.append(cumulative)
        cumulative += len(line)

    return data, ret

def find_lineno_col(idx, offset):
    assert offset >= 0
    index = bisect_right(idx, offset) - 1

    lineno, colno = index + 1, offset - idx[index]
    return lineno, colno

def make_reverse_index(data):
    """
    Returns a sorted list that allows you to query
    the offset of a line, col pair
    """

    data = data.splitlines(keepends=True)

    cumulative = 0
    ret = []
    for line, lineno in zip(data, count(1)):
        # The zero here allows us to directly compare (lineno, col) to 
        # the elements of the list. Interestingly, Python allows you to
        # compare tuples of different sizes.
        ret.append((lineno, 0, cumulative))
        cumulative += len(line)

    return data, ret

def find_offset(idx, lineno, col):
    assert (lineno, col) >= (1, 0)

    index = bisect_right(idx, (lineno, col)) - 1

    _, _, cumulative = idx[index]
    return col + cumulative

def test_forward_index(data):

    lines, idx = make_forward_index(data)

    for offset in range(len(data)):
        if dat := find_lineno_col(idx, offset):
            lineno, col = dat
            line = lines[lineno -1]
            # print(f"{lineno=} {col=}")
            print(">> ", line.replace('\n', '.'))
            print(">> ", " " * col + "^")

def test_reverse_index(data):
    data, ridx = make_reverse_index(original_data)

    for line, lineno in zip(data, count(1)):
        for col, _ in enumerate(line):
            offset = find_offset(ridx, lineno, col)
            print(">> ", line.replace('\n', '.'))
            # print(">> ", " " * col + "^")
            print(">> ", " " * col + original_data[offset].replace("\n",".") )


if __name__ == '__main__':

    with open(sys.argv[0]) as fp:
        # Open it's own source code
        original_data = fp.read()

    test_forward_index(original_data)
    test_reverse_index(original_data)
