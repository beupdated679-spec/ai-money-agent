import json
from pathlib import Path
from datetime import datetime

# Change these words to match the work you can actually do.
SKILLS = [
    "video editing",
    "youtube shorts",
    "shorts",
    "reels",
    "captions",
    "subtitles",
    "educational video",
    "premiere pro",
    "capcut",
    "after effects",
    "social media video",
]

# Jobs with at least this many matching skill words are shortlisted.
MIN_SCORE = 1


def load_latest_jobs():
    reports = Path("reports")
    files = sorted(reports.glob("jobs-*.json"))

    if not files:
        print("No jobs JSON found.")
        print("Run this first: python job_finder.py")
        return []

    latest_file = files[-1]
    print("Reading jobs from:", latest_file)

    try:
        with latest_file.open("r", encoding="utf-8") as f:
            jobs = json.load(f)
        return jobs if isinstance(jobs, list) else []
    except (json.JSONDecodeError, OSError) as error:
        print("Could not read jobs file:", error)
        return []


def score_job(job):
    title = str(job.get("title") or "")
    description = str(job.get("description") or "")
    text = (title + " " + description).lower()

    matched = [skill for skill in SKILLS if skill.lower() in text]
    return len(matched), matched


def create_proposal(title, description, matched_skills):
    skills_text = ", ".join(matched_skills[:5]) or "video editing"

    return f"""Hello,

I’m interested in your project, "{title}".

I can help create engaging video content with clear pacing,
clean cuts, captions/subtitles, and an editing style suited
to your target audience. Relevant areas include {skills_text}.

Before starting, I would confirm the video length, preferred
style, format, footage/assets, deadline, and any examples
you would like me to follow.

I’d be happy to discuss your requirements and deliver a
sample or first draft if appropriate.

Best regards
"""


def main():
    jobs = load_latest_jobs()

    if not jobs:
        print("No jobs available to process.")
        return

    shortlisted = []

    for job in jobs:
        if not isinstance(job, dict):
            continue

        score, matched = score_job(job)

        if score >= MIN_SCORE:
            title = str(job.get("title") or "Untitled")
            description = str(job.get("description") or "")
            project_id = str(job.get("id") or "")
            seo_url = str(job.get("seo_url") or project_id)

            if seo_url.startswith("http"):
                link = seo_url
            else:
                link = "https://www.freelancer.com/projects/" + seo_url

            shortlisted.append({
                "id": project_id,
                "title": title,
                "description": description,
                "link": link,
                "score": score,
                "matched_skills": matched,
                "proposal": create_proposal(title, description, matched),
            })

    shortlisted.sort(key=lambda item: item["score"], reverse=True)

    reports = Path("reports")
    reports.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")

    json_path = reports / f"proposals-{today}.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(shortlisted, f, indent=2, ensure_ascii=False)

    md_path = reports / f"proposals-{today}.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Shortlisted Freelance Jobs & Proposal Drafts\\n\\n")
        f.write(f"Date: {today}\\n")
        f.write(f"Jobs reviewed: {len(jobs)}\\n")
        f.write(f"Jobs shortlisted: {len(shortlisted)}\\n\\n")

        if not shortlisted:
            f.write("No jobs matched the current skill keywords.\\n")

        for item in shortlisted:
            f.write("---\\n\\n")
            f.write(f"## {item['title']}\\n\\n")
            f.write(f"Score: {item['score']}\\n\\n")
            f.write("Matched skills: " + ", ".join(item["matched_skills"]) + "\\n\\n")
            f.write(f"Link: {item['link']}\\n\\n")
            f.write("### Description\\n\\n")
            f.write(item["description"][:1500] + "\\n\\n")
            f.write("### Proposal draft (review before sending)\\n\\n")
            f.write(item["proposal"] + "\\n\\n")

    print("Jobs reviewed:", len(jobs))
    print("Jobs shortlisted:", len(shortlisted))
    print("Saved:", md_path)
    print("Saved:", json_path)
    print("Review proposals manually before submitting them.")


if __name__ == "__main__":
    main()
