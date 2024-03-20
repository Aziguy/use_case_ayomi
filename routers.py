from fastapi import APIRouter, Form, HTTPException, Depends, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from sqlalchemy.orm import Session
from calculator import Calculator
import models
from database import get_db
import csv

router = APIRouter()
calculator = Calculator()


templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request, db: Session = Depends(get_db)):
    """
    Displays the home page of the API.

    Returns:
    - str: HTML of the home page.
    """
    calculations = db.query(models.Calculation).all()
    return templates.TemplateResponse("home_page.html", {"request": request, "calculations": calculations})


@router.post("/calculate/")
async def calculate(expression: str = Form(...), db: Session = Depends(get_db)):
    """
    Calculates the result of a mathematical expression.

    Args:
    - expression (str): The mathematical expression to evaluate.

    Returns:
    - CalculationResult: Object containing the result of the calculation.
    """
    try:
        result = calculator.evaluate_expression(expression)
        calculation_model = models.Calculation(expression=expression, result=result)
        db.add(calculation_model)
        db.commit()
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/export-to-csv/")
def export_to_csv(db: Session = Depends(get_db)):
    """
    Exports data from the database to a CSV file.

    Returns:
    - dict: Dictionary with a message indicating successful export.
    """
    try:
        calculations = db.query(models.Calculation).all()
        with open('calculations.csv', 'w', newline='') as csvfile:
            fieldnames = ['id', 'expression', 'result']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for calculation in calculations:
                writer.writerow({'id': calculation.id, 'expression': calculation.expression, 'result': calculation.result})
        return {"message": "Data exported to CSV successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")