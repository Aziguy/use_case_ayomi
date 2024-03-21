# Calculator in Reverse Polish Notation (RPN).

This is an API for a Reverse Polish Notation (RPN) calculator. It allows users to perform arithmetic calculations by providing mathematical expressions in RPN format.

## Calculator Class

The `Calculator` class is responsible for evaluating mathematical expressions in Reverse Polish Notation. It contains the following methods:

### `__init__()`

- Initializes the calculator with an empty stack.

### `evaluate_expression(expression: str) -> float`

- Evaluates a mathematical expression provided in RPN format.
- Args:
  - `expression` (str): The mathematical expression in RPN format to evaluate.
- Returns:
  - `float`: The calculated result.
- Raises:
  - `ValueError`: If the expression is invalid (e.g., not enough operands, unknown token, division by zero).

## API Routes

### POST /calculate/

- Endpoint for calculating the result of a mathematical expression.
- Request Body:
  - `expression` (str): The mathematical expression in RPN format.
- Response:
  - `result` (float): The calculated result.
- Example:
  ```
  POST /calculate/
  {
    "expression": "2 3 +"
  }
  Response: {"result": 5.0}
  ```

### GET /

- Endpoint for displaying the home page of the API.
- Response:
  - HTML page containing the calculations history.
- Example:
  ```
  GET /
  Response: HTML page with calculations history
  ```

## Getting Started

1. Clone this repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the API server using `uvicorn app:app --reload`.
4. Access the API endpoints using an HTTP client or web browser.


## DEMO

You can check RPN using curl like

⚠️ please make sure you have cURL install in your computer ⚠️


```
curl -X 'POST' \
  'http://127.0.0.1:8000/calculate/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "expression": "8 9 +"
}'
```

You should get **17**

```
{
  "result": 17
}
```

See the documentation interface from [here](http://127.0.0.1:8000/docs) or [here](http://127.0.0.1:8000/redoc)
