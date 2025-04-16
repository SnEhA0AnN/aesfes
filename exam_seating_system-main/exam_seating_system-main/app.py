from flask import Flask, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask, request, render_template, jsonify
import os
import json
import csv
import openpyxl
from flask import send_file


# if os.name == "nt":
#     tmp = "tmp"
#     if not os.path.exists(tmp):
#         os.makedirs(tmp)
# else:
#     tmp = "/tmp"

tmp = "tmp"


app = Flask(__name__)
import base64, sys

sys.path.append("firebase")
from firebase_comm import Firebase

fb = Firebase()
CORS(app, origins="http://127.0.0.1:3000", supports_credentials=True)
app.secret_key = "secret key"  # for session

blocks = {"A": ["1010", "1011", "1012", "1013"], "B": ["3401", "3402", "3403", "3404"]}
base_folder = "templates/allocation/"


if os.name == "nt":
    UPLOAD_FOLDER = "uploads"
else:
    UPLOAD_FOLDER = f"{tmp}/uploads/DB"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


if not os.path.exists(f"{tmp}/alloc/A"):
    os.makedirs(f"{tmp}/alloc/A")

if not os.path.exists(f"{tmp}/alloc/B"):
    os.makedirs(f"{tmp}/alloc/B")

if not os.path.exists(f"{tmp}/DB"):
    os.makedirs(f"{tmp}/DB")


@app.route("/")
def home():
    if session.get("logged_in"):
        return render_template("home.html", logged_in=True)
    else:
        return render_template("home.html", logged_in=False)


@app.route("/seatingplan")
def seating_plan():
    if session.get("logged_in"):
        return render_template("seatingplan.html", blocks=blocks, logged_in=True)
    else:
        return render_template("not_logged_in.html")


@app.route("/updatedb", methods=["GET", "POST"])
# render updatedb.html
def updatedb():
    if session.get("logged_in"):
        return render_template("updatedb.html", logged_in=True)
    else:
        return render_template("not_logged_in.html")


@app.route("/upload", methods=["POST"])
def upload_files():
    # Check if the POST request has files part
    if "files" not in request.files:
        return "No file part"

    files = request.files.getlist("files")

    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])

    try:
        for file in files:
            if file.filename == "":
                return "No selected file"

            # Save the file to the upload folder
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))

            print(f"File saved: {file.filename}")

            # go to update_seat_plan route

        # if student_db.json, faculty_data.csv and room_db.json are uploaded
        if (
            "student_db.json" in os.listdir(app.config["UPLOAD_FOLDER"])
            and "faculty_data.csv" in os.listdir(app.config["UPLOAD_FOLDER"])
            and "room_db.json" in os.listdir(app.config["UPLOAD_FOLDER"])
        ):

            return redirect(url_for("update_seating_plan"))

        return render_template(
            "updatedb.html",
            error="Please upload all these files - student_db.json, faculty_data.csv and room_db.json",
        )
    except Exception as e:
        return f"An error occurred: {e}"


def load_allocation_data(block, room_no):
    # Assuming JSON files are named as per the format "alloc/{block}/{roomnum.json}"
    json_file = f"{tmp}/alloc/{block}/{room_no}.json"
    with open(json_file) as f:
        data = json.load(f)
    return data


@app.route("/<block>/<room>/", methods=["POST"])
def room_details(block, room):
    # Example logic, you can modify this as per your needs
    if request.method == "POST":
        return redirect(url_for(f"room_route_{block}_{room}"))


def create_room_route(block, room_no):
    # room_number = "6001"  # Example room number
    seating_plan = load_allocation_data(block, room_no)

    # print(f"Seating plan for {block} {room_no}: {seating_plan}")

    room_number = room_no
    try:
        faculty_name = seating_plan[-1]["invigilator"]
    except:
        faculty_name = "No invigilator assigned to this room"

    def room_route():
        return render_template(
            f"allocation/{block}/{room_no}/{room_no}.html",
            room_number=room_number,
            faculty_name=faculty_name,
            seating_plan=seating_plan,
        )

    room_route.__name__ = f"room_route_{block}_{room_no}"  # Unique function name
    print(f"{room_route.__name__} created")

    return room_route


try:
    for block, room_nos in blocks.items():
        for room_no in room_nos:
            if os.path.exists(f"{tmp}/alloc/{block}/{room_no}.json"):
                app.route(f"/{block}/{room_no}/")(create_room_route(block, room_no))
            else:
                # Render a template indicating that the database is missing for this room
                def db_missing():
                    return render_template("dbmissing.html")

                app.route(
                    f"/{block}/{room_no}/", endpoint=f"room_route_{block}_{room_no}"
                )(db_missing)

except Exception as e:
    print(f"An error occurred: {e}")


@app.route("/student_data", methods=["GET", "POST"])  # change to local if needed
def display_stu_json():
    if session.get("logged_in"):
        if os.path.exists(os.path.join(UPLOAD_FOLDER, "student_db.json")):
            with open(os.path.join(UPLOAD_FOLDER, "student_db.json"), "r") as json_file:
                json_data = json.load(json_file)
            print(json_data)

            return render_template("db.html", json_data=json_data, title="Student Data")
        else:
            return jsonify({"error": "student_db.json not found"})
    else:
        return render_template("not_logged_in.html")


@app.route("/auth-login", methods=["POST"])
def login_user():
    # get elemtn from form
    email = request.form.get("email")
    password = request.form.get("psw")
    print(f"Emailid: {email}, Password: {password}")
    print(f"Type of email: {type(email)} and password: {type(password)}")
    # Assuming fb.sign_in is a function in your authentication module
    user = fb.sign_in(email, password)

    print(f"User: {user}")

    if user == -1:
        return jsonify(success=False, message="Wrong credentials!"), 200
    elif user:
        session["logged_in"] = True
        return render_template("login.html", logged_in=True)
    else:
        return jsonify(success=False, message="User does not exist!"), 200

    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #     return jsonify(success=False, message="An error occurred on the server."), 500


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("home"))


def fetch_room_info(roll):
    roll = str(roll)
    for block in blocks:
        for room in blocks[block]:
            with open(f"{tmp}/alloc/{block}/{room}.json") as json_file:
                file_contents = json.load(json_file)
                print(type(file_contents))
                # convert from list of dicts to dict
                for i in file_contents:
                    try:
                        print(
                            f"i[roll]: {i['roll']} and roll: {roll} and type: {type(i['roll'])}"
                        )
                        if i["roll"] == roll:
                            return {
                                "block": block,
                                "room": room,
                                "seatid": i["seat_id"],
                                "row": i["row"],
                                "column": i["column"],
                                "name": i["name"],
                                "roll": i["roll"],
                                "subject_code": i["subject_code"],
                                "branch": i["branch"],
                            }
                    except KeyError:
                        pass


@app.route("/send_roll_number", methods=["POST"])
def send_roll_number():
    roll_number = request.form.get("rollnumber")
    room_info_data = fetch_room_info(roll_number)

    if room_info_data:
        # Render the roominfo.html template and pass the data to it
        return render_template(
            "roominfo.html",
            block=room_info_data["block"],
            roomno=room_info_data["room"],
            seat_id=room_info_data["seatid"],
            row=room_info_data["row"],
            column=room_info_data["column"],
            name=room_info_data["name"],
            roll=roll_number,
            subject_code=room_info_data["subject_code"],
            branch=room_info_data["branch"],
        )
    else:
        # Handle the case where room info is not found
        return (
            jsonify({"error": "Room information not found for this roll number"}),
            404,
        )


@app.route("/room_data", methods=["GET", "POST"])
def display_room_json():
    if os.path.exists("room_db.json"):
        with open("room_db.json", "r") as json_file:
            json_data = json.load(json_file)

        return render_template("db.html", json_data=json_data, title="Room Data")
    else:
        return jsonify({"error": "room_db.json not found"})


@app.route("/aboutus/")
def about():
    return render_template("aboutus.html", logged_in=session.get("logged_in"))


@app.route("/login/")
def login():
    if session.get("logged_in"):
        return render_template("login.html", logged_in=True)
    else:
        return render_template("login.html", logged_in=False)


@app.route("/update_seating_plan", methods=["GET"])
def update_seating_plan():
    with open(f"{tmp}/uploads/DB/student_db.json", "r") as student_file:
        students = json.load(student_file)

    with open(f"{tmp}/uploads/DB/room_db.json", "r") as room_file:
        rooms = json.load(room_file)

    # students.sort(key=lambda x: x["subject_code"])
    # print(rooms[0]["seats"][0]["row"])
    # print(students[0])
    student_iter = 0

    # print number of rooms
    print(f"Number of rooms: {len(rooms)}")
    print(type(students))
    print(type(students[student_iter]))
    print(students[student_iter])
    # while students isnt empty

    while student_iter < len(students):

        for room in rooms:

            room_dir = os.path.join(tmp, "alloc", room["block"])
            os.makedirs(room_dir, exist_ok=True)
            room_alloc = {}
            room_alloc["seats"] = []
            seat_iter = 0
            for i in range(1, 5):  # rows in a room

                col = 1
                print(f"row : {i}, col: {col}")

                swap_var = 1
                previous_col = None
                previous_student = None
                if student_iter >= len(students):
                    break
                student = students[student_iter]
                while col < 7:
                    if col > 1:
                        if student_iter >= len(students):
                            break
                        student = students[student_iter]
                        if (
                            student["subject_code"] == previous_student["subject_code"]
                        ) and previous_col == col:
                            if swap_var >= len(students) - student_iter:
                                col += 1
                                continue
                            print(
                                f"swap_var: {swap_var}, student_iter: {student_iter}, len(students): {len(students)}"
                            )
                            (
                                students[student_iter],
                                students[student_iter + swap_var],
                            ) = (
                                students[student_iter + swap_var],
                                students[student_iter],
                            )
                            swap_var += 1

                            continue
                    # empty room seats

                    room_alloc["seats"].append(
                        {
                            "seat_id": f"{room['seats'][seat_iter]['seat_id']}",
                            "name": student["name"],
                            "roll": student["roll"],
                            "subject_code": student["subject_code"],
                            "branch": student["branch"],
                            "row": i,
                            "column": col,
                        }
                    )
                    previous_student = student
                    col += 1
                    previous_col = col
                    student_iter += 1
                    swap_var = 1

                    seat_iter += 1

            with open(
                f"{tmp}/alloc/{room['block']}/{room['room_no']}.json", "w"
            ) as json_file:
                json.dump(room_alloc["seats"], json_file, indent=4)

    faculty_data = {}
    with open(f"{tmp}/uploads/DB/faculty_data.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            name, hrs_served, specialisation = row
            faculty_data[name] = {
                "hrs_served": int(hrs_served),
                "specialisation": specialisation.strip(),
            }

    invigilator_assignments = {}  # Track assigned invigilators
    # open alloc/block/room.json files

    for block in blocks:
        for room in blocks[block]:
            invigilator_assignments[room] = []
            with open(f"{tmp}/alloc/{block}/{room}.json") as json_file:
                room_data = json.load(json_file)
                # if room is empty, dont assign invigilator
                if len(room_data) == 0:
                    continue

                subject_codes = set(
                    [
                        seat["subject_code"]
                        for seat in room_data
                        if "subject_code" in seat
                    ]
                )
                for faculty in faculty_data:
                    # fetch names of faculty who are in invigilator_assignments irrespective of room
                    assigned_faculties = [
                        faculty
                        for faculties in invigilator_assignments.values()
                        for faculty in faculties
                    ]
                    if faculty not in assigned_faculties:
                        if faculty_data[faculty]["hrs_served"] < 40:

                            if (
                                faculty_data[faculty]["specialisation"]
                                not in subject_codes
                            ):
                                invigilator_assignments[room].append(faculty)
                                # faculty_data[faculty]["hrs_served"] += 4
                                # update json_file
                                room_data.append({"invigilator": faculty})
                                with open(
                                    f"{tmp}/alloc/{block}/{room}.json", "w"
                                ) as json_file:
                                    json.dump(room_data, json_file, indent=4)
                                    break
    wb = openpyxl.Workbook()

    rooms = []
    for block in blocks:
        for room in blocks[block]:
            json_file_path = os.path.join(tmp, "alloc", block, f"{room}.json")
            if os.path.exists(json_file_path):
                with open(json_file_path) as json_file:
                    room_data = json.load(json_file)
                    rooms.append(
                        {
                            "block": block,
                            "room_no": int(room),  # Convert room to an integer
                            "seats": room_data,
                        }
                    )

    for room in rooms:
        ws = wb.create_sheet(title=f"{room['block']}_{room['room_no']}")

        # Add headers to the worksheet
        ws.append(
            ["Name", "Roll", "Subject Code", "Branch", "Invigilator", "row", "column"]
        )
        # invigilator_assignments[room].append(faculty)
        try:
            curr_inv = invigilator_assignments[str(room["room_no"])][0]
        except:
            pass
        for seat in room["seats"][0:-1]:

            ws.append(
                [
                    seat.get("name", ""),
                    seat.get("roll", ""),
                    seat.get("subject_code", ""),
                    seat.get("branch", ""),
                    curr_inv,
                    seat.get("row", ""),
                    seat.get("column", ""),
                ]
            )

    wb.remove(wb["Sheet"])
    wb.save(f"{tmp}/alloc/seating_plan.xlsx")

    with open(f"{tmp}/DB/invigilator_assignments.json", "w") as json_file:
        json.dump(invigilator_assignments, json_file, indent=4)

    print("Seating plan updated successfully!")
    return render_template("restartserver.html", blocks=blocks, logged_in=True)
    # return redirect(url_for("seating_plan"))


@app.route("/download_excel")
def download_excel():
    excel_path = f"{tmp}/alloc/seating_plan.xlsx"

    return send_file(excel_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, port=3000)
