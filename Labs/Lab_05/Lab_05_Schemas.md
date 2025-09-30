# Lab 5: The Data Contract Enforcer

<img width="233" height="150" alt="image" src="https://github.com/user-attachments/assets/6fd8c9ee-10ec-4ae5-9a64-09fb5b713644" />
<img width="193" height="150" alt="image" src="https://github.com/user-attachments/assets/4ff82e6a-c741-4660-b3c9-8d8f3d650b2d" />
<img width="150" height="150" alt="image" src="https://github.com/user-attachments/assets/7a0ccd4f-0470-437d-927c-24300ee2b725" />


In this lab, you'll move from simply extracting and transforming data to the critical Data Management step of **Data Validation and Schema Enforcement**. You will create two separate synthetic datasets, enforce strict data typing on the resulting data, and formally document the final, clean schema for each.

The goal is to understand that clean data is not the default; it must be **enforced** via a schema, and that data structure (tabular vs. hierarchical) dictates how that enforcement works.

<br>

## Step 0. Setup

### Navigate to your `DS-2002-F25` directory, update your `main` branch.

1.  Open your Git Bash (Windows) or Terminal (macOS).

2.  Navigate to your `DS-2002-F25` directory. For example: `cd ~/Documents/GitHub/DS-2002-F25/` (yours may differ)

3.  Make sure that you do not have any unstaged or uncommitted stages by running `git status`. If you do, `add` and `commit` them.

4.  Switch to your `main` branch `git checkout main`.

5.  Run `git remote -v`:
    * If your upstream lists my repo `austin-t-rivera/DS-2002-F25.git` and your origin list your repo `<your-github-id>/DS-2002-F25.git`, proceed to step 6.
    * If your upstream lists your repo or does not exist, set my repo by running `git remote add upstream git@github.com:austin-t-rivera/DS-2002-F25.git` and continue in step 5.
        * Run `git fetch upstream` and continue in step 5.
        * Run `git merge upstream/main main` and proceed to step 6.

6.  Run the `update_repo.sh` file.

7.  Use `cd` to further navigate to your `/Labs/Lab_05` directory to confirm your `main` branch is up to date.

<br>

### Open up a new Codespace in GitHub

1.  Go to **your** `DS-2002-F25` repo in GitHub and make sure you are looking at your `main` branch.

2.  Create a new branch named `Lab_5` by typing in "Lab_5" and clicking on "Create branch Lab_5 from main".

3.  To open your first codespace, to the right, you can click on `<> Code`, then `Codespaces`, and lastly `Create codespace on Lab_5`.

4.  NOTE: You are now in your VS Code Codespace! This is a container that is built for you to work in that has essentially all of the functionality of a high-powered IDE, in this case VS Code, but is also fully integrated into your GitHub!

5.  Within your Codespace, in the Terminal (bottom center), use `cd` to navigate to your `/Labs/Lab_05` directory.

6.  Create a new directory for this project and navigate into it:
    ```bash
    mkdir Schema_Enforcer && cd Schema_Enforcer
    ```

<br>

### Install Dependencies and Create Script

1.  In your Terminal, run:
    ```bash
    pip install pandas
    ```

2.  Create a new Python file (`.py`) or Jupyter Notebook (`.ipynb`) named **`lab_script`** (e.g., `lab_script.py` or `lab_script.ipynb`). All code for Parts 1 and 2 will go here.

---

## Part 1: Acquisition and Flexible Formatting

**Goal:** Simulate receiving two different streams of data that intentionally have structural and data-type issues.

### Task 1: Create the Tabular CSV Data (Requires Cleaning)

1.  In your `lab_script`, use Python to create a list of data that is **tabular** but contains type inconsistencies. You can use the standard `csv` module or just Python's built-in file writing.

2.  **Data Requirements:** Create a dataset with at least two records and four columns:
    * `student_id` (Should be $\text{INT}$)
    * `major` (Should be $\text{STRING}$)
    * `is_cs_major` (Should be $\text{BOOL}$): **Intentionally use the strings 'Yes' or 'No'.**
    * `credits_taken` (Should be $\text{FLOAT}$): **Intentionally save the value as a string (e.g., `'10.5'`).**

3.  Write this data to a CSV file named **`raw_survey_data.csv`**.

### Task 2: Create the Hierarchical JSON Data (Requires Normalization)

1.  In your `lab_script`, define a list of dictionaries that is **hierarchical** (nested) using the structure below.

2.  **Data Requirements:** Use the following structure for at least two courses:
    ```json
    [
      {
        "course_id": "DS3001",
        "title": "Data Systems",
        "level": 300,
        "instructors": [
          {"name": "Alice", "role": "Primary"}, 
          {"name": "Bob", "role": "TA"} 
        ]
      },
      {
        "course_id": "DS3002",
        "title": "Visual Analytics",
        "level": 300,
        "instructors": [
          {"name": "Charlie", "role": "Primary"}
        ]
      }
    ]
    ```

3.  Write this structure to a JSON file named **`raw_course_catalog.json`**.

---

## Part 2: Data Validation and Type Casting

**Goal:** Use Python and Pandas to enforce a clean, rigid schema, preparing the data for a database.

### Task 3: Clean and Validate the CSV Data

1.  In your `lab_script`, use `pandas` to load `raw_survey_data.csv` into a DataFrame.

2.  **Enforce Boolean Type:** Write a function or use a custom map/replace to convert the values in the `is_cs_major` column from the strings (`'Yes'`, `'No'`) to proper Python Boolean types (`True`, `False`).

3.  **Enforce Numeric Type:** Use the appropriate `pandas` function (e.g., `.astype()`) to explicitly ensure the `credits_taken` column is stored as a **float** type.

4.  Save the cleaned DataFrame to a new file named **`clean_survey_data.csv`**.

### Task 4: Normalize the JSON Data

1.  In your `lab_script`, use the standard `json` module to load the `raw_course_catalog.json` file.

2.  **Normalize:** Use **`pd.json_normalize`** to flatten the hierarchical data into a single, wide DataFrame.
    * **CRITICAL:** Use the **`record_path`** argument to specifically extract the nested **`instructors`** list. This will result in multiple rows for the courses that have multiple instructors (one row per instructor).

3.  Save the normalized DataFrame to a new file named **`clean_course_catalog.csv`**.

---

## Part 3: The Schema Contract

**Goal:** Formally document the final, clean, and enforced schema for your data. This is what you would hand to a database administrator.

### Task 5: Document the Tabular Schema

1.  Examine the final, cleaned data in your `clean_survey_data.csv`.

2.  In a new text file named **`survey_schema.txt`**, formally document the final, clean schema using the format below. Use the standard database types listed (INT, VARCHAR, BOOL, FLOAT).

| Column Name | Required Data Type | Brief Description |
| :--- | :--- | :--- |
| `student_id` | `INT` | Unique identifier for the student. |
| `major` | `VARCHAR(50)` | The student's primary academic major. |
| `is_cs_major` | `BOOL` | True if the student is a CS major, False otherwise. |
| `credits_taken` | `FLOAT` | Total cumulative credits completed by the student. |

### Task 6: Document the Normalized Catalog Schema

1.  Examine the flattened data in your `clean_course_catalog.csv`. Note the column names created by the `json_normalize` function (e.g., `instructors.name` might become `instructors.name` or `name` depending on the arguments you used).

2.  In a text file named **`catalog_schema.txt`**, document the schema for this **normalized** data. You must include **all** columns in your final DataFrame.

---

## Step 5: Add, Commit, Push, and Submit on Canvas!

1.  Stage all of your changes at once: `git add .`.
2.  Commit your staged changes to your local `Lab_5` branch **with a message**: `git commit -m "Completed Lab 5: Schema Contract Enforcer"`
3.  Push your local branch to your remote repository: `git push --set-upstream origin Lab_5`
4.  Exit your Codespace and navigate to your forked repository on GitHub.
5.  Switch to your `Lab_5` branch on GitHub.
6.  Navigate to your `Schema_Enforcer` directory.
7.  Copy the URL to your `Schema_Enforcer` directory on your `Lab_5` branch, and paste the URL into the Lab 5 assignment on Canvas.

**Expected Files in the `Schema_Enforcer` Directory:**

* **`lab_script.py`** or **`lab_script.ipynb`**
* `raw_survey_data.csv`
* `raw_course_catalog.json`
* **`clean_survey_data.csv`**
* **`clean_course_catalog.csv`**
* **`survey_schema.txt`**
* **`catalog_schema.txt`**
