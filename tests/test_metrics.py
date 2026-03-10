from simulst_edu.metrics import average_lagging, average_proportion, token_f1


def test_average_proportion_matches_manual_value() -> None:
    positions = [2, 4, 5, 5]
    assert average_proportion(positions, source_length=5) == 0.8


def test_average_lagging_matches_reference_example() -> None:
    positions = [2, 4, 5, 5]
    assert abs(average_lagging(positions, source_length=5) - 2.4166666667) < 1e-6


def test_token_f1_uses_bag_overlap() -> None:
    reference = ["mi", "apfel", "essen"]
    hypothesis = ["mi", "brot", "essen"]
    assert abs(token_f1(reference, hypothesis) - (2 / 3)) < 1e-6
