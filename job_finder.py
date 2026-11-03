
import json
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime

KEYWORDS = [
    "video editing",
    "youtube shorts",
    "video editor",
    "reels editing",
    "educational video"
]

def search_jobs(keyword):
    url = (
        "https://www.freelancer.com/api/projects/0.1/projects/active/"
        "?" + urllib.parse.urlencode({
            "query": keyword,
            "limit": 20
        })
    )

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "AI-Money-Agent/1.0"}
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))

        projects = data.get("result", {}).get("projects", [])
        if isinstance(projects, dict):
            projects = list(projects.values())

        return projects

    except Exception as error:
        print(f"Search failed for {keyword}: {error}")
        return []

def make_proposal(title, description):
    return f"""
Hello,

I reviewed your project: {title}

I can help you create engaging, professional video content
with clean editing, captions, suitable pacing, and attention
to your target audience.

I would first confirm your preferred style, duration,
format, and deadline before beginning.

I would be happy to discuss your requirements.

Best regards
"""

def main():
    jobs = {}
    for keyword in KEYWORDS:
        print("Searching:", keyword)
        for job in search_jobs(keyword):
            job_id = str(job.get("id", ""))
            if job_id:
                jobs[job_id] = job
    
with open(
    "reports/jobs-" + datetime.now().strftime("%Y-%m-%d") + ".json",
    "w",
    encoding="utf-8"
) as jf:
    json.dump(list(jobs.values()), jf, indent=2)

    output = Path("reports")
    output.mkdir(exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    file = output / f"freelance-{today}.md"

    with file.open("w", encoding="utf-8") as f:
        f.write("# Freelance Opportunities\n\n")
        f.write(f"Date: {today}\n\n")
        f.write(f"Jobs found: {len(jobs)}\n\n")

        if not jobs:
            f.write("No jobs returned. API may be unavailable or "
                    "the search parameters may need adjustment.\n")

        for job in jobs.values():
            title = job.get("title", "Untitled")
            description = job.get("description") or ""
            link = (
                "https://www.freelancer.com/projects/"
                + str(job.get("seo_url", job.get("id", "")))
            )

            f.write("---\n\n")
            f.write(f"## {title}\n\n")
            f.write(f"Link: {link}\n\n")
            f.write(f"Description: {str(description)[:1500]}\n\n")
            f.write("### Proposal draft\n\n")
            f.write(make_proposal(title, description))
            f.write("\n\n")

    print("Saved:", file)
    print("Total opportunities:", len(jobs))

if __name__ == "__main__":
    main()
