import os
from flask import Flask, render_template, request, redirect, session
from flask_session import Session

app = Flask(__name__)

# Flask-Session configuration
app.config["SESSION_TYPE"] = "filesystem"  # Store sessions in the filesystem
app.secret_key = "your_secret_key"         # Replace with a strong secret key
Session(app)

# Automatically clear session files on server start
session_dir = app.config.get("SESSION_FILE_DIR", "flask_session")
if os.path.exists(session_dir):
    for file in os.listdir(session_dir):
        os.remove(os.path.join(session_dir, file))

# In-memory list of students
students = []  # Replace with database integration if needed

@app.route("/", methods=["GET", "POST"])
def index():
    """Home route to display and manage student attendance."""
    if request.method == "POST":
        student_id_to_delete = int(request.form["student_id"])
        for student in students:
            if student["id"] == student_id_to_delete:
                students.remove(student)
                break
    return render_template("index.html", students=students)

@app.route("/add_manually", methods=["GET"])
def add_manually():
    """Render the manual attendance form."""
    return render_template("index1.html")

@app.route("/submitted", methods=["GET"])
def submitted():
    """Render the attendance submission confirmation."""
    return render_template("submitted.html")

@app.route("/add_manually_post", methods=["POST"])
def add_manually_post():
    """Handle attendance submission from a form."""
    # Check if attendance has already been submitted from this session
    if session.get("has_submitted"):
        return "Attendance has already been submitted from this device!", 403

    # Get the selected student's name from the form
    selected_student = request.form.get("student")
    if selected_student:
        # Add the student to the list
        students.append({"id": len(students) + 1, "name": selected_student})
        session["has_submitted"] = True  # Mark this session as submitted

    return redirect("/submitted")

@app.route("/reset", methods=["GET"])
def reset_sessions():
    """Endpoint to clear all session data."""
    session.clear()  # Clear the current session
    # Clear the session directory if using the filesystem
    if os.path.exists(session_dir):
        for file in os.listdir(session_dir):
            os.remove(os.path.join(session_dir, file))
    return "All sessions have been reset successfully!", 200

if __name__ == "__main__":
    # Ensure session directory exists
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)
    app.run(host="0.0.0.0", port=5000, debug=True)
