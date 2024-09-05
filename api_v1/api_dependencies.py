from typing import Annotated
from fastapi import Depends

from core.BASE_unit_of_work import IUnitOfWork, UnitOfWork
from social_acc_app.schemas import CodeFromGoogle


UOF_Depends = Annotated[IUnitOfWork, Depends(UnitOfWork)]
CodeFromGoogle_Depends = Annotated[CodeFromGoogle, Depends(CodeFromGoogle)]