from typing import Annotated
from fastapi import Depends

from core.BASE_unit_of_work import IUnitOfWork, UnitOfWork
from social_acc_app.schemas import CodeFromGoogle, ParamsFormVK
from sms_app.schemas import SMSCOdeSchemaForm


UOF_Depends = Annotated[IUnitOfWork, Depends(UnitOfWork)]
CodeFromGoogle_Depends = Annotated[CodeFromGoogle, Depends(CodeFromGoogle)]
ParamsVK_Depends = Annotated[ParamsFormVK, Depends(ParamsFormVK)]
SMSCode_Depends = Annotated[SMSCOdeSchemaForm, Depends(SMSCOdeSchemaForm)]
