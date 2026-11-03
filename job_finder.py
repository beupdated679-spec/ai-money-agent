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
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; AI-Money-Agent/1.0)"
        }
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))

        result = data.get("result") or {}
        projects = result.get("projects") or []

        if isinstance(projects, dict):
            projects = list(projects.values())

        if not isinstance(projects, list):
            print(f"Unexpected API response for: {keyword}")
            return []

        return projects

    except Exception as error:
        print(f"Search failed for {keyword}: {error}")
        return []


def make_proposal(title, description):
    return f"""Hello,

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

    # Search all keywords and remove duplicate projects
    for keyword in KEYWORDS:
        print("Searching:", keyword)

        for job in search_jobs(keyword):
            if not isinstance(job, dict):
                continue

            job_id = str(job.get("id") or "")
            if job_id:
                jobs[job_id] = job

    # Create reports folder
    output = Path("reports")
    output.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")

    # Save JSON file for proposal_agent.py
    json_file = output / f"jobs-{today}.json"

    with json_file.open("w", encoding="utf-8") as jf:
        json.dump(list(jobs.values()), jf, indent=2, ensure_ascii=False)

    print("Saved jobs JSON:", json_file)

    # Save readable Markdown report
    markdown_file = output / f"freelance-{today}.md"

    with markdown_file.open("w", encoding="utf-8") as f:
        f.write("# Freelance Opportunities\n\n")
        f.write(f"Date: {today}\n\n")
        f.write(f"Jobs found: {len(jobs)}\n\n")

        if not jobs:
            f.write(
                "No jobs returned. The API may be unavailable, "
                "or the search parameters may need adjustment.\n"
            )

        for job in jobs.values():
            title = str(job.get("title") or "Untitled")
            description = str(job.get("description") or "")
            project_id = str(job.get("id") or "")
            seo_url = str(job.get("seo_url") or project_id)

            if seo_url.startswith("http"):
                link = seo_url
            else:
                link = "https://www.freelancer.com/projects/" + seo_url

            f.write("---\n\n")
            f.write(f"## {title}\n\n")
            f.write(f"Link: {link}\n\n")
            f.write(f"Description: {description[:1500]}\n\n")
            f.write("### Proposal draft\n\n")
            f.write(make_proposal(title, description))
            f.write("\n\n")

    print("Saved Markdown report:", markdown_file)
    print("Total opportunities:", len(jobs))


if __name__ == "__main__":
    main()
