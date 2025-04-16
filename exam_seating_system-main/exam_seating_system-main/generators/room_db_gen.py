import json

rooms = []
blocks = {"A": ["1010", "1011", "1012", "1013"], "B": ["3401", "3402", "3403", "3404"]}

#  Each room has 12 benches and each bench has 2 seats and are arranged in 4 rows and 3 columns and has unique seat_id

for block in blocks:
    for room_no in blocks[block]:
        room = {
            "room_no": room_no,
            "block": block,
            "seats": [],
        }

        for column in range(1, 7):
            for row in range(1, 5):
                seat_id = (row - 1) * 6 + column
                seat = {
                    "seat_id": seat_id,
                    "row": row,
                    "column": column,
                }
                room["seats"].append(seat)
        rooms.append(room)

        #     for seat_in_bench in range(1, 3):  # Each bench has 2 seats
        #         seat_id = (bench - 1) * 2 + seat_in_bench
        #         seat = {
        #             "seat_id": seat_id,
        #             "row": seat_in_bench,
        #             "column": bench,
        #             "bench": bench,
        #         }
        #         room["seats"].append(seat)
        # rooms.append(room)

# Save room data to JSON file
with open("room_db.json", "w") as json_file:
    json.dump(rooms, json_file, indent=4)

print("Room data saved to room_db.json")
