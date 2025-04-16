# import os

# # Define the folder structure and room details
# blocks = {"A": ["1010", "1011", "1012", "1013"], "B": ["3401", "3402", "3403", "3404"]}
# base_folder = "templates/allocation/"

# # Create the directory structure if it doesn't exist
# if not os.path.exists(base_folder):
#     os.makedirs(base_folder)

# for block, room_nos in blocks.items():
#     block_folder = os.path.join(base_folder, block)
#     if not os.path.exists(block_folder):
#         os.makedirs(block_folder)

#     for room_no in room_nos:
#         room_folder = os.path.join(block_folder, room_no)
#         if not os.path.exists(room_folder):
#             os.makedirs(room_folder)

#         html_file = os.path.join(room_folder, f"{room_no}.html")
#         with open(html_file, "w") as f:
#             f.write(
#                 """<!DOCTYPE html>
# <html lang="en">

# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>{{title}}</title>
#     <style>
#         body {
#             font-family: Arial, sans-serif;
#             padding: 20px;
#         }

#         table {
#             width: 100%;
#             border-collapse: collapse;
#             margin-top: 20px;
#         }

#         th,
#         td {
#             border: 1px solid #ccc;
#             padding: 8px;
#             text-align: center;
#         }

#         th {
#             background-color: #f2f2f2;
#         }

#         .column-group {
#             text-align: center;
#         }
#     </style>
# </head>

# <body>
#     <h1>Room Number: {{ room_number }}</h1>
#     <h2>Faculty Invigilator: {{ faculty_name }}</h2>
#     <table>
#         <thead>
#             <tr>
#                 <th colspan="2" class="column-group">{{ block_A }}</th>
#                 <th colspan="2" class="column-group">{{ block_B }}</th>
#                 <th colspan="2" class="column-group">{{ block_C }}</th>
#             </tr>
#             <tr>
#                 <th>L</th>
#                 <th>R</th>
#                 <th>L</th>
#                 <th>R</th>
#                 <th>L</th>
#                 <th>R</th>
#             </tr>
#         </thead>
#         <tbody>
#             {% for row in seating_plan %}
#             <tr>
#                 {% for seat in row %}
#                 <td>{{ seat }}</td>
#                 {% endfor %}
#             </tr>
#             {% endfor %}
#         </tbody>
#     </table>
# </body>

# </html>"""
#             )

# print("HTML files created successfully.")
import os

# Define the folder structure and room details
blocks = {"A": ["1010", "1011", "1012", "1013"], "B": ["3401", "3402", "3403", "3404"]}
base_folder = "templates/allocation/"

# Create the directory structure if it doesn't exist
if not os.path.exists(base_folder):
    os.makedirs(base_folder)

for block, room_nos in blocks.items():
    block_folder = os.path.join(base_folder, block)
    if not os.path.exists(block_folder):
        os.makedirs(block_folder)

    for room_no in room_nos:
        room_folder = os.path.join(block_folder, room_no)
        if not os.path.exists(room_folder):
            os.makedirs(room_folder)

        html_file = os.path.join(room_folder, f"{room_no}.html")
        with open(html_file, "w") as f:
            f.write(
                """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        th,
        td {
            border: 1px solid #ccc;
            padding: 8px;
            text-align: center;
        }

        th {
            background-color: #f2f2f2;
        }

        .column-group {
            text-align: center;
        }
    </style>
</head>

<body>
    <h1>Room Number: {{ room_number }}</h1>
    <h2>Faculty Invigilator: {{ faculty_name }}</h2>
    <table>
        <thead>
            <tr>
                <th>Seat ID</th>
                <th>Name</th>
                <th>Roll</th>
                <th>Subject Code</th>
                <th>Branch</th>
                <th>Row</th>
                <th>Column</th>
            </tr>
        </thead>
        <tbody>
            {% for seat in seating_plan %}
            <tr>
                <td>{{ seat["seat_id"] }}</td>
                <td>{{ seat["name"] }}</td>
                <td>{{ seat["roll"] }}</td>
                <td>{{ seat["subject_code"] }}</td>
                <td>{{ seat["branch"] }}</td>
                <td>{{ seat["row"] }}</td>
                <td>{{ seat["column"] }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>

</html>"""
            )

print("HTML files created successfully.")
