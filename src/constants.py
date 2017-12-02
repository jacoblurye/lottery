"""Defines constants for use throughout.
"""

N_SUBJECTS = 10

# Possible course subjects
SUBJECTS = [
    "Math",
    "Economics",
    "Computer Science",
    "Folklore & Mythology",
    "History & Literature",
    "Comparative Literature",
    "VES",
    "Humanities",
    "Philosophy",
    "Religion",
    "Government",
    "Social Studies",
    "Chemistry",
    "Physics",
    "History of Art & Architecture",
    "African American Studies",
    "Biology",
    "History",
    "East Asian Studies",
    "Psychology"
][:N_SUBJECTS]

# Number of students
N_STUDENTS = 1000

# Number of courses
N_COURSES = 50

# Max and min number of subjects students are interested in
MIN_SUBJECTS = 5
MAX_SUBJECTS = min(5, N_SUBJECTS)

# Max number of courses students can enroll in (min is 0)
MAX_COURSES = 4

# How much noise to include in student preferences (stdev of a normal distribution)
NOISE = 5