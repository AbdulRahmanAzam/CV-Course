# Sample nested dictionary database
student_records = {
    "S101": {"Name": "Alice", "Major": "Computer Science", "Grades": [85, 90, 92]},
    "S102": {"Name": "Bob", "Major": "Mathematics", "Grades": [70, 75, 80]},
    "S103": {
        "Name": "Charlie",
        "Major": "Computer Science",
        "Grades": [95, 98, 100],
    },
}


def get_top_student(records):
    """Returns the name of the student with the highest average grade."""
    highest_avg = -1
    top_student_name = ""

    for student_id, info in records.items():
        grades = info["Grades"]
        if grades:  # Avoid division by zero if list is empty
            avg_grade = sum(grades) / len(grades)

            if avg_grade > highest_avg:
                highest_avg = avg_grade
                top_student_name = info["Name"]

    return top_student_name


def find_students_by_major(records, target_major):
    """Prints all students enrolled in a specific major."""
    print(f"\n--- Students in '{target_major}' ---")
    found = False

    for student_id, info in records.items():
        if info["Major"].lower() == target_major.lower():
            print(f"- {info['Name']} (ID: {student_id})")
            found = True

    if not found:
        print(f"No students found in {target_major}.")


# --- Example Usage for Task 2 ---
top_student = get_top_student(student_records)
print(f"Top Student with Highest Average: {top_student}")

find_students_by_major(student_records, "Computer Science")
find_students_by_major(student_records, "Physics")
