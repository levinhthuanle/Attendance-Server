# 📱 Bluetooth Attendance System



A secure, scalable, and BLE-powered mobile attendance system designed for universities and classrooms. The system supports role-based functionalities for **students** and **teachers**, ensuring accurate, real-time attendance tracking using Bluetooth Low Energy (BLE) technology.



---



## 🚀 1. System Overview



### A. Infrastructure & Technology



- **API Backend**: RESTful FastAPI service with JWT/OAuth2 authentication.

- **Database**: Relational schema with key tables:

&nbsp; - `Users` (students, teachers)

&nbsp; - `Classes`, `Sessions` (individual lectures)

&nbsp; - `AttendanceRecords`, `Configs`

- **BLE (Bluetooth Low Energy)**:

&nbsp; - Peripheral mode for teachers (advertising)

&nbsp; - Central mode for students (scanning)

&nbsp; - Unique UUIDs for session identification

- **Security**:

&nbsp; - Role-based access control (RBAC)

&nbsp; - Encrypted transmission (TLS for API, AES for BLE payloads)

&nbsp; - Runtime permission handling (Bluetooth, Location)



---



## 🎓 2. Student Role



### 2.1 Must-Have Features



- **Authentication**:

&nbsp; - Sign up / Login with email-password or SSO (Google, Facebook)

&nbsp; - Optional email verification



- **Bluetooth Scanning**:

&nbsp; - Scan BLE signals from nearby teachers

&nbsp; - Automatic scan or manual "Start Scan"



- **Auto Check-in**:

&nbsp; - Mark attendance when a valid BLE signal is detected

&nbsp; - Timestamped records

&nbsp; - UI indicator for check-in status



- **Attendance History**:

&nbsp; - View past attendance by class and month

&nbsp; - Status: Present / Absent / Late



- **Notifications**:

&nbsp; - Push notifications for session start/end

&nbsp; - Alerts for missed check-ins when leaving BLE zone



- **Profile**:

&nbsp; - Avatar, personal details

&nbsp; - Attendance statistics and visualizations



### 2.2 Nice-to-Have Features



- **Manual Override**:

&nbsp; - Request manual check-in if BLE fails (with reason)

&nbsp; - Teacher reviews and approves



- **Offline Mode**:

&nbsp; - Store attendance locally and sync when back online



- **Reminders & Calendar Sync**:

&nbsp; - Pre-class reminders

&nbsp; - Google Calendar / iCal integration



- **Gamification**:

&nbsp; - Badges: "100% Attendance", "Early Bird"

&nbsp; - Leaderboards within class



- **In-Class Chat / Q&A**:

&nbsp; - Submit questions to instructor during session



---



## 👩‍🏫 3. Teacher Role



### 3.1 Must-Have Features



- **Secure Login**:

&nbsp; - Email-password login with optional 2FA (OTP via SMS/email)



- **Class Management**:

&nbsp; - Create, edit, delete classes

&nbsp; - Manage student lists



- **Attendance Session Control**:

&nbsp; - Create attendance sessions with start/end time

&nbsp; - Define grace period / late thresholds

&nbsp; - Start BLE advertising with unique UUID



- **Live Dashboard**:

&nbsp; - Real-time list of checked-in students

&nbsp; - Visual statistics of session progress



- **Reporting**:

&nbsp; - Export session/class attendance data (CSV/Excel)

&nbsp; - Filters by date, student, status



### 3.2 Nice-to-Have Features



- **Edit Attendance**:

&nbsp; - Change student status post-session

&nbsp; - Add comments for absences



- **Advanced BLE Settings**:

&nbsp; - Rotating UUIDs to prevent spoofing

&nbsp; - Limit scan count per session to prevent abuse



- **Communication Tools**:

&nbsp; - Send notifications to students (e.g. session results, reminders)



- **Analytics**:

&nbsp; - Monthly attendance heatmaps

&nbsp; - Semester summary reports (exportable as PDF/PPT)



- **TA/Class Rep Delegation**:

&nbsp; - Assign teaching assistants or class leaders to manage check-ins



---



## 📈 4. Supporting Modules



- **Notifications**:

&nbsp; - Firebase Cloud Messaging (FCM)

&nbsp; - User-controlled toggle for notification types



- **Settings & Help Center**:

&nbsp; - Light/dark mode

&nbsp; - FAQ, user guides, contact support



- **Logging & Monitoring**:

&nbsp; - Security audits and action logs

&nbsp; - Crash tracking (e.g., Sentry)

&nbsp; - User behavior analytics



- **CI/CD & Testing**:

&nbsp; - Unit tests for BLE logic, API integration tests

&nbsp; - Automated deployment pipelines (e.g., GitLab CI)



---



