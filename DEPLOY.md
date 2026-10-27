# Publish this

Two things can be published: the profile README, and the documentation site. The profile README is the important one.

## Part 1: the profile README

GitHub shows a special README on your profile page when a repository has **exactly the same name as your username**. Yours would be `MonaRose1/MonaRose1`.

### 1. Create the repository

1. Open <https://github.com/new>.
2. Owner: `MonaRose1`. Repository name: `MonaRose1`.
3. Set it to **Public**. A private profile repository does not render on your profile.
4. Do **not** initialize with a README, a license or a `.gitignore`. This folder already has all three concerns handled.

### 2. Push this folder

From inside this folder:

```bash
git init
git add .
git commit -m "Add technical writing portfolio"
git branch -M main
git remote add origin https://github.com/MonaRose1/MonaRose1.git
git push -u origin main
```

If Git asks for credentials, use a personal access token as the password, or sign in through the browser prompt.

### 3. Check it

- <https://github.com/MonaRose1> shows the README at the top of the profile.
- <https://github.com/MonaRose1/MonaRose1> renders the same page.
- Click each sample link. They point at files in `docs/`, which GitHub renders as pages.

**Note:** the profile README keeps the repository reachable only while the repository is public. If you switch it private, the profile block disappears with no error.

## Part 2: the documentation site (optional)

A site is a nicer reading experience for a hiring manager than forty Markdown files, and it costs nothing.

1. In the new repository, open **Settings → Pages**.
2. Under **Build and deployment → Source**, choose **GitHub Actions**.
3. Push any commit to `main`. The `publish docs site` workflow builds and deploys.
4. The site appears at `https://monarose1.github.io/MonaRose1/`.

The workflow uses `mkdocs build --strict`, so a broken internal link fails the build instead of shipping.

### Preview locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install mkdocs mkdocs-material pymdown-extensions
mkdocs serve
```

Then open <http://127.0.0.1:8000>.

## Part 3: keep it current

| When | What to update |
| --- | --- |
| You publish new writing | Add a row to the table in `README.md` and a page under `docs/samples/` |
| A repository changes | Re-check the sample that documents it; fix the claims that went stale |
| You apply somewhere | Tailor the positioning line to the role, keep the samples identical |
| Quarterly | Run the link check and the lint, and reread the top of the README as a stranger |

## What to trim before publishing

Everything in `docs/` is written to be published. Before the first push, confirm:

- [ ] No client names, credentials or personal data anywhere in the tree
- [ ] No screenshots of a product you do not own
- [ ] The email address in `README.md` is one you want public
- [ ] The audit report and the samples it references are your own repositories
