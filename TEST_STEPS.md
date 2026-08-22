# End-to-end test runbook: cra-demo + Code Review Assistant

Do these steps **in order**. Replace `YOUR_GITHUB_USER` with your GitHub username (e.g. `atharvKagit`).

---

## A. Local CRA stack (must be running)

From `/home/atharv/Code_Review_Assistant`:

### A1. Infra

```bash
docker compose up -d
docker compose ps
```

Wait until `cra-postgres` and `cra-kafka` are **healthy**.

### A2. Migrate (if not already)

```bash
npm run migrate
```

### A3. Three app terminals

```bash
npm run dev:api
```

```bash
npm run dev:worker
```

```bash
npm run dev:dashboard
```

### A4. ngrok (fourth terminal)

```bash
ngrok http 3000
```

Copy the HTTPS URL, e.g. `https://abc123.ngrok-free.app`.

Confirm:

```bash
curl http://localhost:3000/health
```

---

## B. Create the GitHub repo

### B1. On GitHub.com

1. New repository → name: **`cra-demo`**
2. Public or private (private needs a PAT that can read that repo)
3. **Do not** add README/license via GitHub UI (we already have local files)
4. Create repository

### B2. Push local `test_repos/cra-demo` as `main`

```bash
cd /home/atharv/Code_Review_Assistant/test_repos/cra-demo
git init
git checkout -b main
git add .
git commit -m "chore: initial cra-demo main branch"
git remote add origin https://github.com/YOUR_GITHUB_USER/cra-demo.git
git push -u origin main
```

If HTTPS push is denied (403), use SSH or GitHub Desktop / browser upload with your login that has write access.

---

## C. Webhook on cra-demo

Repo → **Settings → Webhooks → Add webhook**

| Field | Value |
|-------|--------|
| Payload URL | `https://YOUR_NGROK_HOST/webhooks/github` |
| Content type | `application/json` |
| Secret | Same as `GITHUB_WEBHOOK_SECRET` in CRA `.env` |
| Events | **Let me select** → enable **Pull requests** and **Pushes** |
| Active | checked |

Save. GitHub may send a ping; API should return 200 ignored for non-PR/push.

---

## D. PAT / token check

Your CRA `GITHUB_TOKEN` must be able to:

- Read `YOUR_GITHUB_USER/cra-demo`
- Comment on PRs
- Open issues (for repo scans)

If the token cannot push from this machine, that is OK for *running* CRA — you only need the token for the **worker**. Push with your browser/SSH login.

---

## E. Test 1 — Pull request review (titles + impact)

Goal: dashboard shows `#1 Some title` and worker finds `api.py` as a caller.

### E1. Confirm `api.py` is on main

Already true after the initial push.

### E2. Create a feature branch and change only `app.py`

```bash
cd /home/atharv/Code_Review_Assistant/test_repos/cra-demo
git checkout -b feature/dashboard-title-demo
```

Edit `app.py` — add a small intentional change, for example a comment and a slightly worse query:

```python
def get_user(user_id):
    """Return a user row. Intentionally builds SQL with string concat for demos."""
    safe_id = clean_user_id(user_id)
    # DEMO: still unsafe for CRA scanners / LLM
    return query(f"SELECT * FROM users WHERE id = '{safe_id}' OR 1=1")
```

Then:

```bash
git add app.py
git commit -m "fix: demonstrate unsafe get_user for CRA review"
git push -u origin feature/dashboard-title-demo
```

### E3. Open PR on GitHub

- Base: `main`
- Compare: `feature/dashboard-title-demo`
- **Title (important):** `Demo: unsafe get_user for dashboard title`
- Create pull request

### E4. Watch worker logs

You should see roughly:

```text
Published PR_REVIEW_REQUESTED   (API)
Starting PR review              (worker)
Built impact context            (callers include api.py)
Review completed
```

### E5. Check GitHub PR

A CRA comment should appear on the PR.

### E6. Check dashboard

1. Open `http://localhost:5173`
2. Sign in with GitHub (re-login if `cra-demo` is new so grants refresh)
3. Open **Repositories** → `YOUR_GITHUB_USER/cra-demo`
4. **Reviews** tab: primary line should be

   `#1 Demo: unsafe get_user for dashboard title`

   Secondary: `Review #N · <shortsha>`

If the repo list is empty: sign out/in after the first webhook ingested the repo.

---

## F. Test 2 — Full repo scan (Scans tab)

### F1. Merge the PR (or push a tiny commit on main)

Either merge the PR on GitHub, or:

```bash
git checkout main
git pull
# optional tiny change
echo "# scan-demo" >> config.py
git add config.py
git commit -m "chore: trigger default-branch repo scan"
git push origin main
```

### F2. Worker logs

```text
Published REPO_SCAN_REQUESTED
Starting repo scan
Repo scan analysis completed
```

### F3. GitHub

A new **Issue** may open with scan findings (if any).

### F4. Dashboard

**Scans** tab: primary line should be **`main`** (branch), secondary `Scan #N · <shortsha>`.

---

## G. Checklist

| Check | Expected |
|-------|----------|
| Webhook delivery green on GitHub | 200 |
| Worker PR review completed | yes |
| PR comment on GitHub | yes |
| Dashboard review shows **PR title** | yes |
| Impact / caller `api.py` in worker or comment | yes |
| Push to main → scan row | yes |
| Dashboard scan shows **main** | yes |

---

## H. Troubleshooting

| Problem | Fix |
|---------|-----|
| No webhook deliveries | ngrok URL changed → update webhook; events = PR + Pushes |
| Worker silent | Kafka healthy? `npm run dev:worker` running? |
| 401 on GitHub API | PAT scopes / access to private repo |
| Dashboard empty repos | Re-login after first ingest; confirm OAuth scopes |
| Review shows `#1` without title | Ensure API/worker restarted with latest code; new PR after that |
| Push 403 from this environment | Push from your own Git credentials / GitHub UI |

---

## Files created for you

Local path: `/home/atharv/Code_Review_Assistant/test_repos/cra-demo/`

You still must: create GitHub repo → push → webhook → open PR (steps B–F).
