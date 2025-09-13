import requests
import random
from faker import Faker
from datetime import timedelta

BASE_URL = "http://127.0.0.1:8000/api/v1"
HEADERS = {"Content-Type": "application/json"}
fake = Faker()

DEPARTMENTS = [
    ("MCS", "Faculty of Mathematics and Computer Science"),
    ("FIT", "Faculty of Information Technology"),
    ("PHYS", "Faculty of Physics and Engineering Physics"),
    ("FETEL", "Faculty of Electronics and Telecommunications"),
    ("CHEM", "Faculty of Chemistry"),
    ("FBB", "Faculty of Biology and Biotechnology"),
    ("ENV", "Faculty of Environment"),
    ("GEO", "Faculty of Geology"),
    ("MST", "Faculty of Materials Science and Technology"),
    ("FIS", "Faculty of Interdisciplinary Science"),
]

COURSES = [
    ("CS101", "Introduction to Computer Science", "MCS"),
    ("CS102", "Data Structures", "MCS"),
    ("CS103", "Algorithms", "MCS"),
    ("IT101", "Information Technology Basics", "FIT"),
    ("IT102", "Web Development", "FIT"),
    ("IT103", "Database Management", "FIT"),
    ("PH101", "Physics I", "PHYS"),
    ("PH102", "Physics II", "PHYS"),
    ("PH103", "Engineering Physics", "PHYS"),
    ("EE101", "Circuit Analysis", "FETEL"),
    ("EE102", "Digital Systems", "FETEL"),
    ("EE103", "Microprocessors", "FETEL"),
    ("CHEM101", "General Chemistry", "CHEM"),
    ("CHEM102", "Organic Chemistry", "CHEM"),
    ("CHEM103", "Physical Chemistry", "CHEM"),
    ("BIO101", "General Biology", "FBB"),
    ("BIO102", "Genetics", "FBB"),
    ("BIO103", "Microbiology", "FBB"),
    ("ENV101", "Environmental Science", "ENV"),
    ("ENV102", "Sustainable Development", "ENV"),
    ("ENV103", "Ecology", "ENV"),
    ("GEO101", "Physical Geography", "GEO"),
    ("GEO102", "Human Geography", "GEO"),
    ("GEO103", "Geographic Information Systems", "GEO"),
    ("MST101", "Materials Science", "MST"),
    ("MST102", "Nanotechnology", "MST"),
    ("MST103", "Polymer Science", "MST"),
    ("FIS101", "Interdisciplinary Science", "FIS"),
    ("FIS102", "Science and Society", "FIS"),
    ("FIS103", "Research Methods", "FIS"),
]

def create_sessions(class_ids, teacher_ids, n_sessions_per_class=5):
    sessions = []
    for class_id in class_ids:
        teacher_id = random.choice(teacher_ids)
        for i in range(n_sessions_per_class):
            start_time = fake.date_time_this_year()
            end_time = start_time + timedelta(hours=random.randint(1, 3))
            session_data = {
                "class_id": class_id,
                "teacher_id": teacher_id,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat()
            }
            resp = requests.post(f"{BASE_URL}/session/", json=session_data, headers=HEADERS)
            sessions.append(resp.json())
    return sessions


def make_email(first_name, last_name):
    parts = (first_name + " " + last_name).split()
    if len(parts) >= 2:
        email = parts[0][0].lower() + parts[1][0].lower() + last_name.lower() + "@example.com"
    else:
        email = first_name.lower() + last_name.lower() + "@example.com"
    return email


def create_departments():
    for dept_id, dept_name in DEPARTMENTS:
        data = {"department_id": dept_id, "department_name": dept_name}
        try:
            requests.post(f"{BASE_URL}/department/", json=data, headers=HEADERS)
        except Exception:
            print(f"Failed to create department {dept_id}")


def create_courses():
    for course_id, course_name, dept_id in COURSES:
        data = {"course_id": course_id, "course_name": course_name, "department_id": dept_id}
        try:
            requests.post(f"{BASE_URL}/course/", json=data, headers=HEADERS)
        except Exception:
            print(f"Failed to create course {course_id}")


def create_users(n_students=100, n_teachers=100, n_admins=10):
    users = []
    student_ids = []
    teacher_ids = []

    # --- Student ---
    for i in range(n_students):
        print("Create student", i)
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = make_email(first_name, last_name)

        # student_id format: 23125xxx
        student_id = f"23125{i+1:03d}"   # 23125001, 23125002, ...

        school_year = f"{random.randint(2020,2025)}-{random.randint(2026,2030)}"
        user = {
            "email": email,
            "password": "string",
            "role": "student",
            "first_name": first_name,
            "last_name": last_name,
            "department_id": random.choice([d[0] for d in DEPARTMENTS]),
            "DOB": fake.date_of_birth(minimum_age=18, maximum_age=25).isoformat(),
            "student_id": student_id,
            "school_year": school_year
        }
        resp = requests.post(f"{BASE_URL}/user/", json=user, headers=HEADERS)
        if resp.status_code >= 200 and resp.status_code < 300:
            users.append(resp.json())
            student_ids.append(student_id)
        else:
            print(f"Student user failed: {resp.status_code} {resp.text}")

    # --- Teacher ---
    for i in range(n_teachers):
        print("Create teacher", i)
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = make_email(first_name, last_name)

        teacher_id = f"T{i+1000:05d}"
        user = {
            "email": email,
            "password": "string",
            "role": "teacher",
            "first_name": first_name,
            "last_name": last_name,
            "department_id": random.choice([d[0] for d in DEPARTMENTS]),
            "DOB": fake.date_of_birth(minimum_age=30, maximum_age=60).isoformat(),
            "teacher_id": teacher_id
        }
        resp = requests.post(f"{BASE_URL}/user/", json=user, headers=HEADERS)
        if resp.status_code >= 200 and resp.status_code < 300:
            users.append(resp.json())
            teacher_ids.append(teacher_id)
        else:
            print(f"Teacher user failed: {resp.status_code} {resp.text}")

    # --- Admin ---
    for i in range(n_admins):
        print("Create admin", i)
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = make_email(first_name, last_name)
        user = {
            "email": email,
            "password": "string",
            "role": "admin",
            "first_name": first_name,
            "last_name": last_name,
            "department_id": random.choice([d[0] for d in DEPARTMENTS]),
            "DOB": fake.date_of_birth(minimum_age=30, maximum_age=60).isoformat()
        }
        resp = requests.post(f"{BASE_URL}/user/", json=user, headers=HEADERS)
        if resp.status_code >= 200 and resp.status_code < 300:
            users.append(resp.json())
        else:
            print(f"Admin user failed: {resp.status_code} {resp.text}")

    return users, student_ids, teacher_ids


def create_classes(n_classes=100, teacher_ids=None, course_ids=None):
    classes = []
    for i in range(n_classes):
        class_data = {
            "class_name": f"Class {i+1:03d}",
            "course_id": random.choice(course_ids),
            "semester": random.choice(["2024A", "2024B", "2025A", "2025B"]),
            "year": random.choice([2024, 2025]),
            "teacher_id": random.choice(teacher_ids)
        }
        resp = requests.post(f"{BASE_URL}/class/", json=class_data, headers=HEADERS)
        if resp.status_code >= 200 and resp.status_code < 300:
            classes.append(i + 1)
        else:
            print(f"Class failed: {resp.status_code} {resp.text}")
    return classes


def create_enrollments(student_ids, class_ids):
    enrollments = []
    for student_id in student_ids:
        enrolled_classes = random.sample(class_ids, k=random.randint(5, 15))
        for class_id in enrolled_classes:
            enrollment = {
                "student_id": student_id,
                "class_id": class_id
            }
            resp = requests.post(f"{BASE_URL}/enrollment/", json=enrollment, headers=HEADERS)
            enrollments.append(resp.json())
    return enrollments

def create_records(student_ids, session_objs):
    records = []
    session_ids = [s.get("session_id") for s in session_objs if s.get("session_id")]
    n_sessions = len(session_ids)
    for student_id in student_ids:
        max_k = min(n_sessions, 30)
        min_k = min(n_sessions, 10)
        k = random.randint(min_k, max_k) if n_sessions >= 10 else n_sessions
        for session_id in random.sample(session_ids, k=k):
            record = {
                "student_id": student_id,
                "session_id": session_id,
                "status": random.choice(["present", "absent"])
            }
            resp = requests.post(f"{BASE_URL}/record/", json=record, headers=HEADERS)
            if resp.status_code >= 200 and resp.status_code < 300:
                records.append(resp.json())
            else:
                print(f"Record failed: {resp.status_code} {resp.text}")
    return records


users = []
student_ids = []
teacher_ids = []
admin_ids = []

classes = []
class_ids = []

enrollments = []

sessions = []

records = []

if __name__ == "__main__":
    print("Starting sample data creation...")
    
    print("Creating departments...")
    create_departments()
    print("Departments created.")
    
    print("Creating courses...")
    create_courses()
    print("Courses created.")
    
    print("Creating users...")
    users, student_ids, teacher_ids = create_users(100, 100, 1)
    print("Student IDs size: ", len(student_ids))
    print("Teacher IDs size: ", len(teacher_ids))
    print("Users created.")

    print("Creating classes...")
    # 4. Create classes
    classes = create_classes(n_classes=10, teacher_ids=teacher_ids, course_ids=[c[0] for c in COURSES])
    class_ids = classes
    print("Class IDs size: ", len(class_ids))
    print("Classes created.")
    # 5. Create enrollments
    
    print("Creating enrollments...")
    enrollments = create_enrollments(student_ids, class_ids)
    print("Enrollments created.")
    
    print("Creating sessions...")
    # 6. Create sessions
    sessions = create_sessions(class_ids, teacher_ids, n_sessions_per_class=5)
    print("Sessions created.")
    
    print("Creating attendance records...")
    # 7. Create attendance records
    records = create_records(student_ids, sessions)
    print("Attendance records created.")
    print("Sample data creation completed!")
