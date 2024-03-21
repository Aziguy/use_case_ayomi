import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models
from calculator import Calculator
from app import app

# Create a db session
SQLALCHEMY_DATABASE_URL = "sqlite:///./rpn_calculator_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Configure db for test
models.Base.metadata.create_all(bind=engine)

client = TestClient(app)


class TestCalculatorAPI:
    @pytest.fixture
    def calculator(self):
        return Calculator()

    @pytest.fixture
    def test_db(self):
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

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
        with pytest.raises(ZeroDivisionError):
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

    def test_negative_numbers(self, calculator):
        result = calculator.evaluate_expression("-5 3 +")
        assert result == -2

    def test_all_operators_only(self, calculator):
        with pytest.raises(ValueError, match="Invalid expression: not enough operands"):
            calculator.evaluate_expression("+ - * / %")

    def test_single_operation(self, calculator):
        result = calculator.evaluate_expression("5")
        assert result == 5

    def test_multiple_same_type_operators(self, calculator):
        result = calculator.evaluate_expression("10 5 5 5 + + +")
        assert result == 25

    def test_home_page(self, test_db):
        test_db.add(models.Calculation(expression="2 2 +", result=4))
        test_db.commit()

        response = client.get("/")
        assert response.status_code == 200
        assert "Calculations History" in response.text
        assert "2 2 +" in response.text
        assert "4" in response.text

    def test_calculate_valid_expression(self):
        expression_data = {"expression": "2.5 3.1 +"}
        response = client.post("/calculate/", json=expression_data)
        assert response.status_code == 200
        assert response.json() == {"result": 5.6}

    def test_calculate_invalid_expression(self, calculator):
        with pytest.raises(ZeroDivisionError) as exc_info:
            expression_data = {"expression": "10 0 /"}
            client.post("/calculate/", json=expression_data)

        assert exc_info.type == ZeroDivisionError
        assert str(exc_info.value) == "Division by zero error"

    def test_export_to_csv(self):
        response = client.get("/export-to-csv/")
        assert response.status_code == 200
        assert "message" in response.json()
        assert "Data exported to CSV successfully" in response.json()["message"]
