from to_minisat import to_minisat, write_minisat_file
import os


def assert_minisat_file_is_correct():
    with open("temp.cnt") as fp:
        lines = []
        for line in fp.readlines():
            lines.append(line)

    os.remove("temp.cnt")

    assert len(lines) == 4
    assert lines[0].strip() == "p cnf 2 3"
    assert lines[1].strip() == "1 2 0"
    assert lines[2].strip() == "1 -2 0"
    assert lines[3].strip() == "-1 -2 0"


def test_write_minisat_file():
    n_variables = 2
    formula = [
        [1, 2, 0],
        [1, -2, 0],
        [-1, -2, 0]
    ]
    write_minisat_file(formula, n_variables, "temp.cnt")
    assert_minisat_file_is_correct()


def test_write_minisat_file_add_zeros():
    n_variables = 2
    formula = [
        [1, 2],
        [1, -2],
        [-1, -2]
    ]
    write_minisat_file(formula, n_variables,
                       "temp.cnt", add_zeros=True)
    assert_minisat_file_is_correct()


def test_to_minisat_satisfiable_formula():

    n_variables = 2
    formula = [
        [1, 2, 0],
        [1, -2, 0],
        [-1, -2, 0],
    ]
    result = to_minisat(formula, n_variables)
    assert "SAT" in result


def test_to_minisat_unsatisfiable_formula():
    n_variables = 2
    formula = [
        [1, 2, 0],
        [1, -2, 0],
        [-1, -2, 0],
        [-1, 2, 0],
    ]
    result = to_minisat(formula, n_variables)

    assert "UNSAT" in result
