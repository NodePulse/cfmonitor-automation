# ai_agent/problem_extractor.py


def extract_problem_data(lines, week=1, level=1):
    problems = []

    for url in lines:
        url = url.strip()
        if "codeforces" not in url:
            print(f"Skipping: {url}")
            continue

        parts = [p for p in url.split("/") if p]
        try:
            if "group" in parts:
                problem_id = parts[-3] + parts[-1]
            else:
                problem_id = parts[-2] + parts[-1]

            problems.append(
                {"id": problem_id, "url": url, "level": level, "week": week}
            )

        except IndexError:
            print(f"Invalid URL format: {url}")
            continue

    return problems
