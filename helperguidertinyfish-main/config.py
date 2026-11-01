"""Edit this file to point your radar at your own companies and goals."""
import os

from dotenv import load_dotenv

# Reads TINYFISH_API_KEY from your .env file (the SDK then picks it up on its own)
load_dotenv()

if not os.getenv("TINYFISH_API_KEY"):
    raise SystemExit(
        "TINYFISH_API_KEY is not set.\n"
        "Copy .env.example to .env and paste your key from agent.tinyfish.ai/api-keys"
    )

# What you want, in plain English. Naming the fields gives cleaner JSON.
GOAL = (
    "Find software or AI internships for students. "
    "Return JSON: a list of role, location, deadline, link."
)

# Company name -> careers page. Add your own!
PAGES = {
    "Jane Street": "https://www.janestreet.com/join-jane-street/open-roles/",
    "[Company B]": "https://[careers-page-b]",  # TODO: replace with a real careers URL
}

# Used by stage 4: Search decides which pages to open
SEARCH_QUERY = "software engineering internship apply"
MAX_SEARCH_PAGES = 5

OUTPUT_FILE = "internships.json"
