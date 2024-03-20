from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from calculator import Calculator
from starlette.responses import HTMLResponse

app = FastAPI()
calculator = Calculator()


class Expression(BaseModel):
    expression: str


@app.get("/", response_class=HTMLResponse)
async def home_page():
    return """
    <html>
    <head>
        <title>RPN Calculator</title>
    </head>
    <body>
        <h1>Calculator</h1>
        <form action="/calculate/" method="post">
            <input type="text" name="expression" placeholder="Enter expression">
            <button type="submit">Calculate</button>
        </form>
    </body>
    </html>
    """


@app.post("/calculate/")
async def calculate(expression: str = Form(...)):
    try:
        result = calculator.evaluate_expression(expression)
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
