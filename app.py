from fastapi import FastAPI, Form
from starlette.responses import HTMLResponse
from calculator import Calculator

app = FastAPI()
calc = Calculator()


@app.get("/", response_class=HTMLResponse)
async def home_page():
    return """
    <html>
    <head>
        <title>Calculator</title>
    </head>
    <body>
        <h1>Calculator</h1>
        <form action="/" method="post">
            <input type="text" name="expression" placeholder="Enter expression">
            <input type="submit" value="Calculate">
        </form>
    </body>
    </html>
    """


@app.post("/", response_class=HTMLResponse)
def calculate(expression: str = Form(...)):
    result = calc.evaluate_expression(expression)
    return f"<h2>Result: {result} ( ͡° ͜ʖ ͡°)</h2>"
