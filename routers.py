from fastapi import APIRouter, Form, HTTPException, Depends, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from sqlalchemy.orm import Session
from calculator import Calculator
import models
from database import get_db

router = APIRouter()
calculator = Calculator()


templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request, db: Session = Depends(get_db)):
    calculations = db.query(models.Calculation).all()
    return templates.TemplateResponse("home_page.html", {"request": request, "calculations": calculations})


@router.post("/calculate/")
async def calculate(expression: str = Form(...), db: Session = Depends(get_db)):
    try:
        result = calculator.evaluate_expression(expression)
        calculation_model = models.Calculation(expression=expression, result=result)
        db.add(calculation_model)
        db.commit()
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
