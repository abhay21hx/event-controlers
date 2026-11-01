# Internship Radar: Starter Template

Workshop template for **Building with Web Agents** (TinyFish x GITM).
Copy this folder (or click **Use this template** on GitHub), and you'll have a working radar in about 15 minutes.

You build it in four stages. Each stage is its own file, so if you get stuck you can jump ahead.

| Stage | File | What it does |
|---|---|---|
| 1 | `stage1_single.py` | One agent reads one careers page and prints JSON |
| 2 | `stage2_loop.py` | A loop over many pages, saved to `internships.json` |
| 3 | `stage3_parallel.py` | All pages at once with `asyncio.gather` |
| 4 | `stage4_search.py` | Search finds the pages, agents work them |

`config.py` holds the pages and the goal, so you only edit one file to point the radar at your own companies.

## 1. Get set up (5 min)

1. Sign up at **tinyfish.ai/students** with your **school email + password**.
   "Continue with Google" does **not** give you the $35 credit.
2. Create an API key at **agent.tinyfish.ai/api-keys**.
3. In this folder:

**Mac / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

4. Open `.env` and paste your key:

```
TINYFISH_API_KEY=paste-your-key-here
```

`.env` is in `.gitignore`, so it won't be committed. **Never paste your key into a public repo, a screenshot or a WhatsApp group.**

## 2. Run the stages

```bash
python stage1_single.py
python stage2_loop.py
python stage3_parallel.py
python stage4_search.py
```

A run takes **30 to 90 seconds**. That is normal. A sync run stops at 2 minutes.

> **Always look at the result.** A run can say `COMPLETED` and still return an empty list. The goal can fail while the run succeeds. Every stage here prints the result so you can tell.

## 3. Make it yours

Edit `config.py`:

- Add your own companies to `PAGES`.
- Change `GOAL` to what you care about, for example *"Find AI or data internships in India or remote."*
- Name the fields you want in the goal for cleaner JSON.

## 4. Put it on autopilot (Monitor)

No code needed:

1. Go to **agent.tinyfish.ai/monitor**.
2. New monitor, then Page monitor, and paste a careers page.
3. Run it daily and turn on email on changes.

Costs about $0.15 a month from your $35.

## 5. Give your coding agent the live web (MCP)

```bash
# Claude Code
claude mcp add --transport http tinyfish https://agent.tinyfish.ai/mcp

# Codex
codex mcp add tinyfish --url https://agent.tinyfish.ai/mcp
```

Cursor: add this to your MCP config.

```json
{ "mcpServers": { "tinyfish": { "url": "https://agent.tinyfish.ai/mcp" } } }
```

The first connection opens your browser to sign in. Then ask your agent: *"Use the TinyFish tools to find AI internships and save them to a JSON file."*

## Stuck? Try this first

| If this happens | Try this |
|---|---|
| `401` or "unauthorized" | Check `.env` has `TINYFISH_API_KEY`, or export it in this terminal again |
| It's taking ages | 30 to 90 seconds is normal. Sync runs stop at 2 minutes |
| "Blocked" or empty result | That site blocks bots. Set `browser_profile` to `"stealth"`, or try another page |
| Wrong or messy JSON | Name the fields you want in the goal, or pass an `output_schema` |
| Agent didn't use TinyFish | Start with "Use the TinyFish tools to…" and check the MCP server is connected |
| No $35 in your wallet | Check you signed up with your school email and a password |
| `source` not found on Windows | Use `.venv\Scripts\activate` |
| Still stuck | Hand up. Someone will come to help |

Docs: **docs.tinyfish.ai**. Coding agents can read **docs.tinyfish.ai/for-coding-agents**.
Paste that link into ChatGPT, Claude or Cursor and ask it anything.

## Run the Mission Control frontend and backend

The dashboard is served by `Hackathon project\main.py`; the backend keeps
missions in memory, so keep it running while using the dashboard.

1. Make sure `Hackathon project\.env` contains `TINYFISH_API_KEY=your-key`.
   Do not put the API key in the HTML or share it publicly.
2. Double-click `Hackathon project\start_backend.bat`. It checks/install
   dependencies, checks the API key, starts the backend in its own terminal,
   waits until it is ready, and opens the dashboard. Keep the backend terminal
   open while using the dashboard. Alternatively, start it from PowerShell:

   ```powershell
   cd "Hackathon project"
   pip install -r ..\requirements.txt
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

3. Use `http://127.0.0.1:8000` in your browser. This serves the dashboard and
   API from the same origin. If you open `frontend.html` directly, it will
   redirect to the served dashboard when the backend is up, or tell you to
   start it with the batch file. Check `http://127.0.0.1:8000/health` returns
   `{"status":"ok"}`.

If the dashboard reports a connection error, confirm the terminal window is
still running and the browser is open to `http://127.0.0.1:8000`. The TinyFish
API key must be configured only on the backend.

## Bounty

Submit on **tinybounties.com** with the event code from the room.
A valid submission includes a LinkedIn post and an X post, both tagging TinyFish.
"# helperguidertinyfish" 

# event-controlers
