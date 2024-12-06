
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.controllers.employee import (
    create_employee,
    update_employee,
    discactivate_employee,
    create_employees_from_csv,
    get_employee,
    get_employees,
)
from typing import Union
from app import utils
from sqlalchemy import func
from core.database import get_db
from app.exceptions.employee import user_already_exist, employee_not_found
from app.services.token import oauth2_scheme, RoleChecker
from app.enums import Role
from app.schemas.employee import UserOut,OurBaseModelOut,UsersOut,RoleOut,User,EmployeeUpdate,RolesOut
from app import models

allow_action_by_roles = RoleChecker([ Role.SUPER_USER,Role.ADMIN])

router = APIRouter(
    dependencies=[Depends(oauth2_scheme) , Depends(allow_action_by_roles)]
)

@router.get('/get_all_employee', response_model=Union[UsersOut,OurBaseModelOut])
def get_all(
    db: Session = Depends(get_db),
    page_size: int = 10,
    page_number: int = 1,
    name_substr: str = None
):
    query = db.query(models.Employee)

    if name_substr:
        query = query.filter(func.lower(func.CONCAT(models.User.first_name, " ", models.User.last_name)).contains(func.lower(name_substr)))

    total_records = query.count()
    total_pages = utils.div_ceil(total_records, page_size)
    users = query.limit(page_size).offset((page_number-1)*page_size).all()

    user_out_list = []
    for user in users:
        roles_out = []
        for role in user.Employee_roles:
            roles_out.append(role.role.name)
        user_out = UserOut(
            id=user.id,
            firstname=user.firstname,
            lastname=user.lastname,
            number=user.number,
            gender=user.gender,
            account_status=user.status.name,
            phone_number=user.phone_number,
            email=user.email,
            birthdate=user.birthdate,
            contract_type=user.contract_type,
            cnss_number=user.cnss_number,
            roles=roles_out,
            message=None,
            status=None,
        )
        user_out_list.append(user_out)

    return UsersOut(
        total_pages=total_pages,
        total_records=total_records,
        page_number=page_number,
        page_size=page_size,
        list=user_out_list,
        message="All users",
        status=status.HTTP_200_OK
    )


@router.get("/{employee_id}" , response_model=Union[UserOut,OurBaseModelOut])
def get_employee_by_id(
    employee_id: int,
    db: Session = Depends(get_db),
):
    try:
        employee  = get_employee(db, employee_id)
        employee_roles = employee.Employee_roles
        employee_fields = employee.__dict__
        employee_fields.pop('status')
        employee_fields.pop('password')


    except employee_not_found:
        return OurBaseModelOut(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            messege="something went wrong."
        )
    roles_out = []
    for role in employee_roles:
        roles_out.append(role.role.name)

    return UserOut(
        **employee_fields,
        roles=roles_out,
        message="Employee found",
        status=status.HTTP_200_OK
    )


@router.post("/", response_model=OurBaseModelOut)
async def create_employe(
    employee: User,
    db: Session = Depends(get_db),
    ):
    try:
        result = await create_employee(db, employee)
        return result
    except Exception as e:
        db.rollback()
        return OurBaseModelOut(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Error creating user. "
        )



@router.post("/csv", response_model=dict)
async def upload_employees(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return await create_employees_from_csv(file, db)




@router.patch("/disactivate/{employee_id}", response_model=bool)
def disactivate_employe(
    employee_id: int,
    db: Session = Depends(get_db),
):
    #[TODO] modify the function to return a response model
    return discactivate_employee(db, employee_id=employee_id)




@router.put("/{employee_id}", response_model=OurBaseModelOut)
async def update_employe(
    employee: EmployeeUpdate,
    employee_id: int,
    db: Session = Depends(get_db),
):
    try:
        result = await update_employee(db, employee_id=employee_id, employee_data=employee.dict(exclude_unset=True))

    except HTTPException as e:
        return OurBaseModelOut(
            status=e.status_code,
            message=e.detail
        )
    except Exception as e:
        return OurBaseModelOut(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="An error occurred during employee update."
        )

    return OurBaseModelOut(
            status=status.HTTP_200_OK,
            message="Employee updated successfully.",
        )




