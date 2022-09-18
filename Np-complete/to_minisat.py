import os


def write_minisat_file(formula: list[list[int]],
                       n_variables: int, name: str, add_zeros=False) -> None:
    """ Writes a file with a boolean formula in CNF that can be
        read by the minisat program to check its satisfiability.
    """
    n_clauses = len(formula)
    with open(name, "w") as fp:
        # Write the header
        fp.write(f"p cnf {n_variables} {n_clauses}\n")
        # Write each clause
        for clause in formula:
            line = " ".join([str(num) for num in clause])
            if add_zeros:
                line += " 0"
            line += "\n"
            fp.write(line)


def to_minisat(formula: list[list[int]],
               n_variables: int, add_zeros=False) -> str:
    """ Returns a string with the results of the given formula
        in the minisat program.
    """

    formula_file = "./tmp.cnt"
    write_minisat_file(formula, n_variables, formula_file, add_zeros)
    result_file = "./tmp.sat"
    os.system(f"minisat {formula_file} {result_file}")

    with open(result_file) as fp:
        result = fp.read()

    os.remove(formula_file)
    os.remove(result_file)
    return result
