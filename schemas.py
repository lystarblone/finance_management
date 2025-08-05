from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

class TransactionCreate(BaseModel):
    amount: float
    type: TransactionType
    category_id: int
    description: Optional[str] = None

class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: TransactionType
    category_id: int
    description: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

class CategoryCreate(BaseModel):
    name: str
    type: TransactionType

class CategoryResponse(BaseModel):
    id: int
    name: str
    type: TransactionType

    class Config:
        orm_mode = True

class StatisticsResponse(BaseModel):
    total_income: float
    total_expense: float
    balance: float
    by_category: Dict[str, Dict[str, float]]