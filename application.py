from flask import Flask, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import traceback
from werkzeug.security import generate_password_hash, check_password_hash
from src.data.doctors import DOCTORS_BY_STATE
from src.pipelines.prediction_pipeline import CustomData, PredictPipeline
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from flask import send_file
import io


# -------------------------------
# Flask App Configuration
# -------------------------------
application = Flask(__name__)
application.secret_key = "minor_project_secret_key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "app.db")

application.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(application)
app = application


# -------------------------------
# Database Models
# -------------------------------
class PredictionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100))
    prediction = db.Column(db.String(50))
    confidence = db.Column(db.Float)
    state = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# -------------------------------
# Auth Helper (STEP 5.6)
# -------------------------------
def login_required():
    return "user_id" in session


# -------------------------------
# AUTH ROUTES (STEP 5.3–5.5)
# -------------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        if User.query.filter_by(email=email).first():
            return "User already exists"

        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_name"] = user.name
            return redirect(url_for("home"))

        return "Invalid credentials"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# -------------------------------
# PUBLIC ROUTES
# -------------------------------
@app.route("/")
def home():
    return render_template("home.html")


# -------------------------------
# PROTECTED ROUTES (STEP 5.6)
# -------------------------------
@app.route("/assessment")
def assessment():
    if not login_required():
        return redirect(url_for("login"))
    return render_template("form.html")


@app.route("/history")
def history():
    if not login_required():
        return redirect(url_for("login"))

    records = PredictionHistory.query.order_by(
        PredictionHistory.timestamp.desc()
    ).all()
    return render_template("history.html", records=records)
@app.route("/download-report")
def download_report():

    report = session.get("report_data")

    if not report:
        return "No report data available"

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "Breast Cancer Risk Assessment Report")
    y -= 40

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Patient Name: {report['patient_name']}")
    y -= 20
    pdf.drawString(50, y, f"State: {report['state']}")
    y -= 20
    pdf.drawString(50, y, f"Date & Time: {report['timestamp']}")
    y -= 30

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Prediction Result:")
    y -= 20

    pdf.setFont("Helvetica", 11)
    pdf.drawString(70, y, report["result"])
    y -= 20
    pdf.drawString(70, y, f"Confidence Score: {report['confidence']}%")
    y -= 30

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Tumor Feature Inputs:")
    y -= 20

    pdf.setFont("Helvetica", 9)

    for key, value in report["inputs"].items():
        if key in ["patient_name", "state"]:
            continue

        pdf.drawString(70, y, f"{key.replace('_',' ').title()}: {value}")
        y -= 14

        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 9)
            y = height - 50

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Breast_Cancer_Report.pdf",
        mimetype="application/pdf"
    )


@app.route("/care-support")
def care_support():
    if not login_required():
        return redirect(url_for("login"))

    selected_state = session.get("state")
    doctors = DOCTORS_BY_STATE.get(selected_state, [])

    return render_template(
        "care_support.html",
        doctors=doctors,
        state=selected_state
    )

@app.route("/hospital/<int:index>")
def hospital_details(index):
    if not login_required():
        return redirect(url_for("login"))

    state = session.get("state")
    hospitals = DOCTORS_BY_STATE.get(state, [])

    if index >= len(hospitals):
        return "Invalid hospital"

    hospital = hospitals[index]

    return render_template("hospital_details.html", hospital=hospital)
# -------------------------------
# Helper: Safe Float Fetch
# -------------------------------
def get_float(name):
    if name not in request.form or request.form[name] == "":
        raise ValueError(f"Invalid input for {name}")
    return float(request.form[name])


# -------------------------------
# Prediction Route (PROTECTED)
# -------------------------------
@app.route("/predict", methods=["POST"])
def predict_datapoint():
    if not login_required():
        return redirect(url_for("login"))

    try:
        session["patient_name"] = request.form.get("patient_name")
        session["state"] = request.form.get("state")

        data = CustomData(
            mean_radius=get_float("mean_radius"),
            mean_texture=get_float("mean_texture"),
            mean_perimeter=get_float("mean_perimeter"),
            mean_area=get_float("mean_area"),
            mean_smoothness=get_float("mean_smoothness"),
            mean_compactness=get_float("mean_compactness"),
            mean_concavity=get_float("mean_concavity"),
            mean_concave_points=get_float("mean_concave_points"),
            mean_symmetry=get_float("mean_symmetry"),
            mean_fractal_dimension=get_float("mean_fractal_dimension"),

            radius_error=get_float("radius_error"),
            texture_error=get_float("texture_error"),
            perimeter_error=get_float("perimeter_error"),
            area_error=get_float("area_error"),
            smoothness_error=get_float("smoothness_error"),
            compactness_error=get_float("compactness_error"),
            concavity_error=get_float("concavity_error"),
            concave_points_error=get_float("concave_points_error"),
            symmetry_error=get_float("symmetry_error"),
            fractal_dimension_error=get_float("fractal_dimension_error"),

            worst_radius=get_float("worst_radius"),
            worst_texture=get_float("worst_texture"),
            worst_perimeter=get_float("worst_perimeter"),
            worst_area=get_float("worst_area"),
            worst_smoothness=get_float("worst_smoothness"),
            worst_compactness=get_float("worst_compactness"),
            worst_concavity=get_float("worst_concavity"),
            worst_concave_points=get_float("worst_concave_points"),
            worst_symmetry=get_float("worst_symmetry"),
            worst_fractal_dimension=get_float("worst_fractal_dimension")
        )

        final_data = data.get_data_as_dataframe()
        pipeline = PredictPipeline()
        pred, proba = pipeline.predict(final_data)
        print("RAW MODEL PREDICTION:", pred[0])
        print("PROBABILITIES:", proba[0])

        confidence = round(max(proba[0]) * 100, 2)
        if pred[0] == 0:
            result = "Breast Cancer Detected"
        elif pred[0] == 1:
            result = "Breast Cancer Not Detected"
        else:
            result = "Prediction Error"
        record = PredictionHistory(
            patient_name=session["patient_name"],
            prediction=result,
            confidence=confidence,
            state=session["state"]
        )
        db.session.add(record)
        db.session.commit()
        # -------------------------------
        # Store data for PDF 
        # # -------------------------------
        session["report_data"] = {
             "patient_name": session.get("patient_name"),
             "state": session.get("state"),
             "result": result,
             "confidence": confidence,
             "inputs": dict(request.form),
             "timestamp": datetime.utcnow().strftime("%d-%m-%Y %H:%M")
             }

        return render_template("result.html", result=result, confidence=confidence)

    except Exception:
        traceback.print_exc()
        return "Prediction error occurred"

# -------------------------------
# Run Application
# -------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True, port=5001)
