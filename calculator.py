import asyncio

class Calculator:
    def __init__(self):
        self.stack = []

    async def calculate_async(self, expression):
        tokens = expression.split()
        for token in tokens:
            if token.isdigit():
                self.stack.append(int(token))
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
                        raise ValueError("Division by zero error")
                    result = operand1 / operand2
                self.stack.append(result)
            else:
                raise ValueError("Invalid expression: unknown token")
        if len(self.stack) != 1:
            raise ValueError("Invalid expression: too many operands")
        return self.stack[0]

async def main():
    calc = Calculator()
    result = await calc.calculate_async("3 4 + 5 *")
    print("Résultat:", result)

asyncio.run(main())


