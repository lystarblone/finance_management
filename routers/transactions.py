from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from schemas import TransactionCreate, TransactionResponse, TransactionType
from models import Transaction, Category
from database import get_db

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == transaction.category_id).first()
    if not category or category.type != transaction.type:
        raise HTTPException(status_code=400, detail="Invalid category for transaction type")
    
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/", response_model=List[TransactionResponse])
def get_transactions(type: Optional[TransactionType] = None, db: Session = Depends(get_db)):
    query = db.query(Transaction)
    if type:
        query = query.filter(Transaction.type == type)
    return query.all()