
import json
from pathlib import Path
from datetime import datetime

REPORTS = Path("reports")
REPORTS.mkdir(exist_ok=True)

SKILLS = [
    "video editing",
    "youtube shorts",
    "captions",
    "subtitles",
    "reels",
    "educational videos",
    "short form video",
    "social media videos"
]

def score_job(title, description):
    text = (str(title) + " " + str(description)).lower()
    score = sum(1 for skill in SKILLS if skill in text)
    return score

def generate_proposal(title, description):
    text = str(description).lower()

    services = []

    if "caption" in text or "subtitle" in text:
        services.append("accurate captions and subtitles")

    if "youtube" in text or "short" in text:
        services.append("engaging short-form video editing")

    if "educational" in text:
        services.append("clear educational video presentation")

    if "reels" in text or "instagram" in text:
        services.append("social-media-ready video formatting")

    if not services:
        services.append("professional video editing")

    service_text = ", ".join(services)

    return f"""Hello,

I reviewed your project: {title}

I can help you with {service_text}.

My workflow focuses on clean editing, suitable pacing,
and a professional final result.

Before starting, I would confirm your preferred style,
video duration, delivery format, and deadline.

I would be happy to discuss your requirements.

Best regards
"""

def main():
    files = sorted(REPORTS.glob("freelance-*.md"))

    if not files:
        print("No freelance reports found.")
        print("Run job_finder.py first.")
        return

    latest = files[-1]
    content = latest.read_text(encoding="utf-8")

    # Read the structured jobs from the saved JSON if available.
    jobs = []
    json_files = sorted(REPORTS.glob("jobs-*.json"))

    if json_files:
        jobs = json.loads(json_files[-1].read_text())

    output = REPORTS / (
        "proposals-" + datetime.now().strftime("%Y-%m-%d") + ".md"
    )

    with output.open("w", encoding="utf-8") as f:
        f.write("# Proposal Agent Report\n\n")
        f.write("These are drafts. Review before sending.\n\n")

        for job in jobs:
            title = job.get("title") or "Untitled"
            description = job.get("description") or ""
            score = score_job(title, description)

            if score == 0:
                continue

            f.write("---\n\n")
            f.write(f"## {title}\n\n")
            f.write(f"Match score: {score}/8\n\n")
            f.write(generate_proposal(title, description))
            f.write("\n\n")

    print("Proposal drafts saved:", output)

if __name__ == "__main__":
    main()
