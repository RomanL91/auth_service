from typing import Annotated
from fastapi import Depends

from core.BASE_unit_of_work import IUnitOfWork, UnitOfWork


UOF_Depends = Annotated[IUnitOfWork, Depends(UnitOfWork)]
