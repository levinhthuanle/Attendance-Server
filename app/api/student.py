from fastapi import APIRouter, Depends, HTTPException
from app.db.deps import get_db
from sqlalchemy.orm import Session, joinedload
from app.models.record import Record
from app.models.user import User
from app.schemas.record import RecordCreate, RecordOut
from app.models.student import Student
from app.models.session import Session as SessionModel
from app.models.enrollment import Enrollment
from app.schemas.session import AttendanceRequest
from app.schemas.student import StudentRecordOut, StudentFull
from app.schemas.enrollment import EnrollmentCheckResponse
from app.core.security import get_current_user

router = APIRouter(prefix="/student", tags=["Student"])

@router.get("/", response_model=list[StudentRecordOut])
async def get_students(db: Session = Depends(get_db)):
    students = (
        db.query(
            Student.student_id,
            User.first_name,
            User.last_name
        )
        .join(User, Student.user_id == User.user_id)
        .all()
    )
    return [
        StudentRecordOut(
            student_id=s.student_id,
            first_name=s.first_name,
            last_name=s.last_name
        )
        for s in students
    ]

@router.get("/{student_id}/records", response_model=list[RecordOut])
async def get_student_records(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student.records

@router.post("/record", response_model=RecordOut)
async def create_student_record(record: RecordCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == record.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.records.append(record)
    db.commit()
    db.refresh(student)
    return student.records

@router.get("/current", response_model=StudentFull)
async def get_current_student(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "Student" and current_user.role != "student":
        raise HTTPException(status_code=403, detail="Access denied: not a student")
    
    student = db.query(Student).filter(Student.user_id == current_user.user_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return StudentFull(
        student_id=student.student_id,
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        DOB=current_user.DOB,
        school_year=student.school_year,
        department_id=current_user.department_id
    )

@router.get("/all/attendance_records", response_model=list[RecordOut])
async def get_attendance_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "Student" and current_user.role != "student":
        raise HTTPException(status_code=403, detail="Access denied: not a student")

    student = db.query(Student).filter(Student.user_id == current_user.user_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student.records

@router.get("/check-enrollment/{class_id}", response_model=EnrollmentCheckResponse)
async def check_enrollment(
    class_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "Student" and current_user.role != "student":
        raise HTTPException(status_code=403, detail="Access denied: not a student")


    student = db.query(Student).filter(Student.user_id == current_user.user_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")


    enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == student.student_id,
            Enrollment.class_id == class_id
        )
        .first()
    )

    return EnrollmentCheckResponse(
        student_id=student.student_id,
        class_id=class_id,
        enrolled=enrollment is not None
    )
    
@router.get("/all/class/enroll")
async def get_all_class_enrollments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "Student"   and current_user.role != "student":
        raise HTTPException(status_code=403, detail="Access denied: not a student")

    student = db.query(Student).filter(Student.user_id == current_user.user_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    enrollments = (
        db.query(Enrollment)
        .filter(Enrollment.student_id == student.student_id)
        .all()
    )

    return [
        EnrollmentCheckResponse(
            student_id=student.student_id,
            class_id=enrollment.class_id,
            enrolled=True
        )
        for enrollment in enrollments
    ]

@router.get("/{class_id}/all/attendance_records", response_model=list[RecordOut])
async def get_all_attendance_records(
    class_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "Student" and current_user.role != "student":
        raise HTTPException(status_code=403, detail="Access denied: not a student")

    student = db.query(Student).filter(Student.user_id == current_user.user_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")


    records = (
        db.query(Record)
        .join(SessionModel, Record.session_id == SessionModel.session_id)
        .filter(
            Record.student_id == student.student_id,
            SessionModel.class_id == class_id
        )
        .all()
    )

    return records

@router.post("/roll_call", response_model=RecordOut)
async def student_roll_call(
    data: AttendanceRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "Student" and current_user.role != "student":
        raise HTTPException(status_code=403, detail="Access denied: not a student")


    student = db.query(Student).filter(Student.user_id == current_user.user_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")


    session = db.query(SessionModel).filter(SessionModel.session_id == data.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Kiểm tra enrollment (student phải học trong class này)
    enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == student.student_id,
            Enrollment.class_id == session.class_id
        )
        .first()
    )
    if not enrollment:
        raise HTTPException(status_code=403, detail="Student not enrolled in this class")

    # Kiểm tra đã có record chưa
    record = (
        db.query(Record)
        .filter(
            Record.student_id == student.student_id,
            Record.session_id == session.session_id
        )
        .first()
    )

    if record:
        record.status = data.status
    else:
        record = Record(
            student_id=student.student_id,
            session_id=session.session_id,
            status=data.status
        )
        db.add(record)

    db.commit()
    db.refresh(record)

    return record

@router.get("/{student_id}/full", response_model=StudentFull)
async def get_full_student(
    student_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    user = db.query(User).filter(User.user_id == student.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found for this student")

    return StudentFull(
        student_id=student.student_id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        DOB=user.DOB,
        school_year=student.school_year,
        department_id=user.department_id
    )
