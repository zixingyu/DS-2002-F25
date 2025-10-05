# Course Catalog Schema

This document defines the schema for the normalized course catalog data.

## Table: Course Instructors

| Column Name | Required Data Type | Brief Description |
| :--- | :--- | :--- |
| `name` | `VARCHAR(100)` | Full name of the instructor. |
| `role` | `VARCHAR(50)` | Role of the instructor (e.g., Primary, TA). |
| `course_id` | `VARCHAR(20)` | Unique identifier for the course. |
| `section` | `VARCHAR(10)` | Section number of the course. |
| `title` | `VARCHAR(200)` | Full title/name of the course. |
| `level` | `INT` | Course level (e.g., 200, 300, 400). |