import random
import json

# Read names from "names.txt" file
with open("names.txt", "r") as txt_file:
    names = [name.strip() for name in txt_file.readlines()]

# List of branch names
branches = ["CSE", "ELE", "MEC", "CIV"]

subjects_per_branch = {
    "CSE": ["CSE101", "CSE102", "CSE103"],
    "ELE": ["EE101", "EE102", "EE103"],
    "MEC": ["ME101", "ME102", "ME103"],
    "CIV": ["CE101", "CE102", "CE103"],
}

students = []
roll_counter = {branch: 1 for branch in branches}  # Track roll numbers for each branch

for branch in branches:
    # roll = f"{branch}{str(roll_counter[branch]).zfill(3)}"  # Roll number format: {branchname}001, {branchname}002, ...
    # subject_code = random.choice(subjects_per_branch[branch])
    # students.append(
    #     {"name": name, "roll": roll, "subject_code": subject_code, "branch": branch}
    # )
    # roll_counter[branch] += 1
    # if (
    #     roll_counter[branch] > 15
    # ):  # Reset roll numbers after 15 students in a branch
    #     roll_counter[branch] = 1
    # total 120 students.30 students per branch.
    for i in range(1, 39):
        roll = f"{branch}{str(roll_counter[branch]).zfill(3)}"
        subject_code = random.choice(subjects_per_branch[branch])
        name = names.pop(0)
        students.append(
            {"name": name, "roll": roll, "subject_code": subject_code, "branch": branch}
        )
        roll_counter[branch] += 1
        if roll_counter[branch] > 39:
            roll_counter[branch] = 1


with open("student_db.json", "w") as json_file:
    json.dump(students, json_file, indent=4)

print("Student data saved to student_db.json")
