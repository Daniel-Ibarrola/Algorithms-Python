from to_minisat import to_minisat


def two_color_graph_with_two_edges_cnf():
    # Graph with three vertices
    formula = [
        [1, 2, 0],
        [-1, -2, 0],
        [3, 4, 0],
        [-3, -4, 0],
        [5, 6, 0],
        [-5, -6, 0],
        [1, 3, 0],
        [2, 4, 0],
        [1, 5, 0],
        [2, 6, 0],
    ]
    return formula


def test_two_colors_cnf_satisfied():

    # Graph with two vertices
    n_variables = 4
    formula = [
        [1, 2, 0],
        [-1, -2, 0],
        [3, 4, 0],
        [-3, -4, 0],
        [1, 3, 0],
        [2, 4, 0]
    ]
    result = to_minisat(formula, n_variables)

    assert "SAT" in result

    n_variables = 6
    formula = two_color_graph_with_two_edges_cnf()
    result = to_minisat(formula, n_variables)

    assert "SAT" in result


def test_two_colors_cnf_not_satisfied():

    # Graph with three vertices (C3). Cannot be colored by just two colors
    n_variables = 3
    formula = two_color_graph_with_two_edges_cnf()
    formula.append([3, 5, 0])
    formula.append([4, 6, 0])
    result = to_minisat(formula, n_variables)

    assert "SAT" in result


def test_three_colors_cnf_satisfied():

    n_variables = 9
    formula = [
        [1, 2, 3, 0]
    ]
    assert "SAT" in result


def test_three_colors_cnf_not_satisfied():
    pass


def test_graph_to_cnf_formula():
    pass

