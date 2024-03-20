from calculator import Calculator

import pytest


class TestCalculator:
    @pytest.fixture
    def calculator(self):
        return Calculator()

    def test_valid_expression(self, calculator):
        result = calculator.evaluate_expression("3 4 + 5 *")
        assert result == 35

    def test_valid_expression_with_whitespace(self, calculator):
        result = calculator.evaluate_expression("  3   4 +    5   *  ")
        assert result == 35

    def test_decimal_numbers(self, calculator):
        result = calculator.evaluate_expression("2.5 3.1 +")
        assert result == 5.6

    def test_addition(self, calculator):
        result = calculator.evaluate_expression("10 5 +")
        assert result == 15

    def test_subtraction(self, calculator):
        result = calculator.evaluate_expression("10 5 -")
        assert result == 5

    def test_multiplication(self, calculator):
        result = calculator.evaluate_expression("10 5 *")
        assert result == 50

    def test_division(self, calculator):
        result = calculator.evaluate_expression("10 5 /")
        assert result == 2

    def test_complex_expression(self, calculator):
        result = calculator.evaluate_expression("10 2 3 + * 7 -")
        assert result == 43

    def test_division_by_zero(self, calculator):
        with pytest.raises(ValueError, match="Division by zero error"):
            calculator.evaluate_expression("10 0 /")

    def test_invalid_expression_unknown_token(self, calculator):
        with pytest.raises(ValueError, match="Invalid expression: unknown token"):
            calculator.evaluate_expression("10 & 5 +")

    def test_invalid_expression_unknown_operator(self, calculator):
        with pytest.raises(ValueError, match="Invalid expression: unknown token"):
            calculator.evaluate_expression("10 5 &")

    def test_invalid_expression_not_enough_operands(self, calculator):
        with pytest.raises(ValueError, match="Invalid expression: not enough operands"):
            calculator.evaluate_expression("10 +")

    def test_invalid_expression_too_many_operands(self, calculator):
        with pytest.raises(ValueError, match="Invalid expression: too many operands"):
            calculator.evaluate_expression("10 5 3 +")

    def test_modulo_operator(self, calculator):
        result = calculator.evaluate_expression("10 3 %")
        assert result == 1
