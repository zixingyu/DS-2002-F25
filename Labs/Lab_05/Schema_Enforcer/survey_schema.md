# Survey Data Schema

This document defines the schema for the cleaned survey data.

## Table: Student Survey

| Column Name | Required Data Type | Brief Description |
| :--- | :--- | :--- |
| `student_id` | `INT` | Unique identifier for the student. |
| `major` | `VARCHAR(100)` | The student's declared major field of study. |
| `GPA` | `FLOAT` | The student's grade point average on a 4.0 scale. |
| `is_cs_major` | `BOOL` | Boolean flag indicating whether the student is a Computer Science major. |
| `credits_taken` | `FLOAT` | Total number of academic credits the student has completed. |