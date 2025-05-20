# ai_agent/processor.py

import re
from docx import Document
import csv
import os
from ai_agent.problem_extractor import extract_problem_data


def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        return [para.text for para in doc.paragraphs if para.text.strip()]
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return []


def extract_week_from_path(path):
    match = re.search(r"[\\/]week[\s_]*(\d+)", path, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return 0


def process_docx_file(file_path, week, level):
    lines = extract_text_from_docx(file_path)
    print(f"Detected week from path: {week}")  # ✅ Add this for debug
    return extract_problem_data(lines, week=week, level=level)


def export_problems_to_csv(problems, filename, output_folder):
    base_name = os.path.splitext(os.path.basename(filename))[0]
    output_file = os.path.join(output_folder, f"{base_name}_problems.csv")

    file_exists = os.path.exists(output_file)

    with open(output_file, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "url", "level", "week"])

        if not file_exists:
            writer.writeheader()

        for problem in problems:
            writer.writerow(problem)

    return output_file
