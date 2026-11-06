from flask import Flask, render_template, request, redirect, url_for, flash, session

import os
import secrets
from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Create Flask application
app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

database_url = os.getenv("DATABASE_URL")

if not app.config["SECRET_KEY"]:
    raise RuntimeError("SECRET_KEY is not set in your .env file.")

if not database_url:
    raise RuntimeError("DATABASE_URL is not set in your .env file.")

# Configure PostgreSQL driver
if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://",
        "postgresql+psycopg://",
        1
    )
elif database_url.startswith("postgresql://"):
    database_url = database_url.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True
}


db = SQLAlchemy(app)


class SupportRequest(db.Model):

    __tablename__ = "support_requests"

    id = db.Column(db.Integer, primary_key=True)

    reference_number = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    student_name = db.Column(
        db.String(120),
        nullable=False
    )

    matric_number = db.Column(
        db.String(30),
        nullable=False
    )

    category = db.Column(
        db.String(60),
        nullable=False
    )

    subject = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="Submitted"
    )

    admin_response = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )



CATEGORIES = [
    "Academic Support",
    "Registration Issues",
    "Examination Issues",
    "Financial Issues",
    "Technical Support",
    "Other Administrative Issues"
]


@app.route("/")
def index():
    submitted_reference = session.pop("submitted_reference", None)

    support_request = None

    if submitted_reference:
        support_request = SupportRequest.query.filter_by(
            reference_number=submitted_reference
        ).first()

    return render_template(
        "index.html",
        submitted=bool(support_request),
        support_request=support_request
    )


@app.route("/submit", methods=["GET", "POST"])
def submit_request():

    if request.method == "POST":

        student_name = request.form.get("student_name", "").strip()
        matric_number = request.form.get("matric_number", "").strip().upper()
        category = request.form.get("category", "").strip()
        subject = request.form.get("subject", "").strip()
        description = request.form.get("description", "").strip()

        
        if not all([student_name, matric_number, category, subject, description]):
            flash("Please fill in all fields.", "error")
            return render_template(
                "submit_request.html",
                categories=CATEGORIES
            )

        
        if category not in CATEGORIES:
            flash("Please select a valid category.", "error")
            return render_template(
                "submit_request.html",
                categories=CATEGORIES
            )

        
        if len(description) < 10:
            flash("Description must be at least 10 characters.", "error")
            return render_template(
                "submit_request.html",
                categories=CATEGORIES
            )

        # Generate unique reference number
        reference_number = "SSR-" + secrets.token_hex(4).upper()

        new_request = SupportRequest(
            reference_number=reference_number,
            student_name=student_name,
            matric_number=matric_number,
            category=category,
            subject=subject,
            description=description
        )

        try:
            db.session.add(new_request)
            db.session.commit()

            
            return redirect(
                url_for(
                    "request_submitted",
                    reference_number=reference_number
                )
            )

        except Exception:
            db.session.rollback()

            app.logger.exception("Error submitting support request")

            flash(
                "Your request could not be submitted. Please try again.",
                "error"
            )

            return render_template(
                "submit_request.html",
                categories=CATEGORIES
            )

    
    return render_template(
        "submit_request.html",
        categories=CATEGORIES
    )


@app.route("/request-submitted/<reference_number>")
def request_submitted(reference_number):

    support_request = SupportRequest.query.filter_by(
        reference_number=reference_number
    ).first_or_404()

    return render_template(
        "request_submitted.html",
        support_request=support_request
    )


# Track a support request
@app.route("/track", methods=["GET", "POST"])
def track_request():

    support_request = None

    if request.method == "POST":

        matric_number = request.form.get(
            "matric_number", ""
        ).strip().upper()

        reference_number = request.form.get(
            "reference_number", ""
        ).strip().upper()

        if not matric_number or not reference_number:

            flash(
                "Please enter your matric number and reference number.",
                "error"
            )

        else:

            support_request = SupportRequest.query.filter_by(
                matric_number=matric_number,
                reference_number=reference_number
            ).first()

            if support_request is None:

                flash(
                    "No request found. Please check your details.",
                    "error"
                )

    return render_template(
        "track_request.html",
        support_request=support_request
    )


# Run application
if __name__ == "__main__":
    app.run(debug=True)
