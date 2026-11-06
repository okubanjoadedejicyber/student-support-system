# Student Support System
A web-based platform developed with Flask to allow students to submit academic or administrative support requests and track their progress using a unique reference number.

## Features
- Submit academic and administrative support requests.
- Generate a unique tracking ID for each request.
- Track requests using matriculation number and reference number.
- Prevent accidental duplicate submissions(Client side only for now).
- Store request information in a PostgreSQL database.
- User-friendly interface.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/student-support-system.git
   ```

2. Enter the project directory:
   ```bash
   cd student-support-system
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file and configure:
   ```env
   DATABASE_URL=your_database_url
   SECRET_KEY=your_secret_key
   ```

6. Run the application:
   ```bash
   flask --app app run --debug
   ```

7. Open `http://127.0.0.1:5000` in your browser.

## Limitations
- No dedicated administrator dashboard for managing requests.
- No email or SMS notifications.
- Request tracking depends on the student's matriculation number and reference number.
- Limited reporting and request analytics.
- Duplicate submission prevention is not a complete substitute for server-side request validation.

## Future Improvements
- Develop an administrator dashboard to manage and update requests.
- Add email and SMS notifications.
- Introduce student and administrator authentication.
- Add request status updates and response history.
- Implement improved validation and security.
- Include analytics and report generation.

## Technologies Used
Python, Flask, Flask-SQLAlchemy, PostgreSQL, HTML, CSS, JavaScript and Jinja2.
