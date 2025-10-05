import csv
import json
import pandas as pd


# PART 1: ACQUISITION AND FLEXIBLE FORMATTING

# Task 1: Create Tabular CSV Data (with intentional type issues)
print("Creating raw_survey_data.csv...")

survey_data = [
    ['student_id', 'major', 'GPA', 'is_cs_major', 'credits_taken'],
    [1001, 'Computer Science', 3.8, 'Yes', '45.0'],
    [1002, 'Data Science', 3, 'Yes', '42.5'],
    [1003, 'Mathematics', 3.5, 'No', '38.0'],
    [1004, 'Commerce', 3, 'No', '50.5'],
    [1005, 'Computer Science', 3.9, 'Yes', '47.0']
]

with open('raw_survey_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(survey_data)

print("✓ raw_survey_data.csv created successfully!\n")

# Task 2: Create Hierarchical JSON Data
print("Creating raw_course_catalog.json...")

course_catalog = [
    {
        "course_id": "DS2002",
        "section": "001",
        "title": "Data Science Systems",
        "level": 200,
        "instructors": [
            {"name": "Austin Rivera", "role": "Primary"},
            {"name": "Heywood Williams-Tracy", "role": "TA"}
        ]
    },
    {
        "course_id": "CS2100",
        "section": "002",
        "title": "Data Structures and Algorithms 1",
        "level": 200,
        "instructors": [
            {"name": "Briana Morrison", "role": "Primary"}
        ]
    },
    {
        "course_id": "CS3130",
        "section": "001",
        "title": "Computer Systems and Organization 2",
        "level": 300,
        "instructors": [
            {"name": "Charles Reiss", "role": "Primary"}
        ]
    }
]

with open('raw_course_catalog.json', 'w') as file:
    json.dump(course_catalog, file, indent=2)

print("✓ raw_course_catalog.json created successfully!\n")

# PART 2: DATA VALIDATION AND TYPE CASTING

# Task 3: Clean and Validate the CSV Data
print("Cleaning survey data...")

df_survey = pd.read_csv('raw_survey_data.csv')

print("Original data types:")
print(df_survey.dtypes)
print("\nOriginal data:")
print(df_survey)

df_survey['is_cs_major'] = df_survey['is_cs_major'].replace({
    'Yes': True,
    'No': False
})

df_survey = df_survey.astype({
    'credits_taken': 'float64',
    'GPA': 'float64'
})

print("\n✓ Data cleaned!")
print("\nCleaned data types:")
print(df_survey.dtypes)
print("\nCleaned data:")
print(df_survey)

df_survey.to_csv('clean_survey_data.csv', index=False)
print("\n✓ clean_survey_data.csv saved successfully!\n")

# Task 4: Normalize the JSON Data
print("Normalizing course catalog data...")

with open('raw_course_catalog.json', 'r') as file:
    courses = json.load(file)

print("Original hierarchical structure (first course):")
print(json.dumps(courses[0], indent=2))

df_catalog = pd.json_normalize(
    courses,
    record_path=['instructors'],
    meta=['course_id', 'section', 'title', 'level']
)

print("\n✓ Data normalized!")
print("\nNormalized DataFrame:")
print(df_catalog)
print("\nNormalized data types:")
print(df_catalog.dtypes)

df_catalog.to_csv('clean_course_catalog.csv', index=False)
print("\n✓ clean_course_catalog.csv saved successfully!\n")

print("=" * 60)
print("ALL TASKS COMPLETED SUCCESSFULLY!")
print("=" * 60)