from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..schemas import StatisticsResponse
from ..models import Transaction, Category
from ..database import get_db

router = APIRouter(prefix="/statistics", tags=["statistics"])

@router.get("/", response_model=StatisticsResponse)
def get_statistics(db: Session = Depends(get_db)):
    total_income = db.query(func.sum(Transaction.amount)).filter(Transaction.type == "income").scalar() or 0
    total_expense = db.query(func.sum(Transaction.amount)).filter(Transaction.type == "expense").scalar() or 0
    
    category_stats = db.query(
        Category.name,
        Transaction.type,
        func.sum(Transaction.amount).label("total")
    ).join(Category).group_by(Category.name, Transaction.type).all()
    
    by_category = {}
    for name, type, total in category_stats:
        if name not in by_category:
            by_category[name] = {"income": 0, "expense": 0}
        by_category[name][type] = float(total)
    
    return {
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "balance": float(total_income - total_expense),
        "by_category": by_category
    }