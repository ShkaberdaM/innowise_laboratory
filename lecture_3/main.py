students = []
"""
This module provides functionality for managing student grades,
calculating averages, and generating reports.
"""
def calculate_average(grades):
    """
    Calculate the average of grades.
    """
    try:
        return sum(grades) / len(grades)
    except ZeroDivisionError:
        return None


def add_student():
    """Add a new student to the system."""
    name = input("Enter student name: ").strip().title()

    if any(s['name'] == name for s in students):
        print(f"Student '{name}' already exists.")
    else:
        students.append({'name': name, 'grades': []})
        print(f"Student '{name}' added successfully.")


def add_grades():
    """Add grades for an existing student."""
    name = input("Enter student name: ").strip().title()

    student = next((s for s in students if s['name'] == name), None)

    if not student:
        print(f"Student '{name}' not found.")
        return

    print(f"Adding grades for {name}. Type 'done' to finish.")
    while True:
        grade_input = input("Enter a grade (or 'done'): ").strip().lower()
        if grade_input == 'done':
            break

        try:
            grade = int(grade_input)
            if 0 <= grade <= 100:
                student['grades'].append(grade)
            else:
                print("Grade must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def show_report():
    """Generate a comprehensive report of all students."""
    if not students:
        print("No students recorded.")
        return

    all_averages = []
    for student in students:
        avg = calculate_average(student['grades'])

        if avg is not None:
            print(f"{student['name']}'s average grade is {avg:.1f}.")
            all_averages.append(avg)
        else:
            print(f"{student['name']}'s average grade is N/A.")

    print("-" * 30)

    if all_averages:
        print(f"Max Average: {max(all_averages):.1f}")
        print(f"Min Average: {min(all_averages):.1f}")
        overall_avg = sum(all_averages) / len(all_averages)
        print(f"Overall Average: {overall_avg:.1f}")
    else:
        print("No grades available for summary stats.")


def find_top_students():
    """Find and display the student with the highest average."""
    valid_students = [s for s in students if calculate_average(s['grades']) is not None]

    if not valid_students:
        print("No students with grades to evaluate.")
    else:
        top_student = max(valid_students, key=lambda s: calculate_average(s['grades']))
        top_avg = calculate_average(top_student['grades'])
        print(f"The student with the highest average is {top_student['name']} "
              f"with a grade of {top_avg:.1f}.")


def display_menu():
    """Display the main menu options."""
    return """
1. Add a new student
2. Add grades for a student
3. Generate a full report
4. Find the top student
5. Exit
"""


def main():
    """Main function to run the Student Grade Analyzer."""

    # Infinite loop to keep the program running
    while True:
        print("--- Student Grade Analyzer ---")
        print(display_menu())

        # Handle menu selection with error checking
        try:
            number = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        # Add a new student
        if number == 1:
            add_student()

        # Add grades for a student
        elif number == 2:
            add_grades()

        # Full Report
        elif number == 3:
            show_report()

        # Find top performer
        elif number == 4:
            find_top_students()

        # Exit
        elif number == 5:
            print("Exiting program.")
            break

        else:
            print("Please select a valid option (1-5).")


if __name__ == "__main__":
    main()

