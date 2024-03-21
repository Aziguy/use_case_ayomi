class Calculator:
    """This is our calculator class for arithmetic operations that we'll use from our API."""

    def __init__(self):
        """Initializes the calculator with an empty stack."""
        self.stack = []

    def evaluate_expression(self, expression):
        """
        Evaluates a mathematical expression in Reverse Polish Notation (RPN) and returns the result.

        Args:
            expression (str): The mathematical expression in RPN format to evaluate.

        Returns:
            float: The calculated result.

        Raises:
            ValueError: If the expression is invalid (example: not enough operands,
                         unknown token).
            ZeroDivisionError: If a division by zero is attempted.
        """
        tokens = expression.split()
        for token in tokens:
            try:
                operand = float(token)
                self.stack.append(operand)
            except ValueError:
                if token == '%':
                    if len(self.stack) < 2:
                        raise ValueError("Invalid expression: not enough operands")
                    operand2 = self.stack.pop()
                    operand1 = self.stack.pop()
                    if operand2 == 0:
                        raise ZeroDivisionError("Division by zero error")
                    result = operand1 % operand2
                    self.stack.append(result)
                elif token in ['+', '-', '*', '/']:
                    if len(self.stack) < 2:
                        raise ValueError("Invalid expression: not enough operands")
                    operand2 = self.stack.pop()
                    operand1 = self.stack.pop()
                    if token == '+':
                        result = operand1 + operand2
                    elif token == '-':
                        result = operand1 - operand2
                    elif token == '*':
                        result = operand1 * operand2
                    elif token == '/':
                        if operand2 == 0:
                            raise ZeroDivisionError("Division by zero error")
                        result = operand1 / operand2
                    self.stack.append(result)
                else:
                    raise ValueError("Invalid expression: unknown token")
        if len(self.stack) != 1:
            raise ValueError("Invalid expression: too many operands")
        return self.stack[0]
