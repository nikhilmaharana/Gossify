# Deploying Gossiphy to PythonAnywhere

This guide walks through deploying the Django project to PythonAnywhere (free tier). Follow the steps below.

## 1) Prepare locally

1. Activate your virtualenv (PowerShell):

```powershell
& .\myenv\Scripts\Activate.ps1
```

2. Install recommended packages (if not already installed):

```powershell
& .\myenv\Scripts\python.exe -m pip install whitenoise gunicorn
```

3. Create `requirements.txt`:

```powershell
& .\myenv\Scripts\python.exe -m pip freeze > requirements.txt
```

4. Commit and push to your GitHub repo:

```powershell
git add requirements.txt
git commit -m "Add requirements for deployment"
git push
```

## 2) Create a PythonAnywhere account and new web app

1. Sign up or log in at https://www.pythonanywhere.com/
2. Go to the "Web" tab and click "Add a new web app" → choose "Manual configuration" → select the same Python version as your virtualenv.
3. Set the **Working directory** to your project root (the folder containing `manage.py`).

## 3) Set up a virtualenv on PythonAnywhere and install deps

1. Open a **Bash** console on PythonAnywhere (from the Consoles tab).
2. Create a virtualenv (example; adjust Python version):

```bash
python3.11 -m venv --copies ~/venvs/gossiphy-venv
source ~/venvs/gossiphy-venv/bin/activate
pip install --upgrade pip
pip install -r ~/yourgithubrepo/path/to/requirements.txt
```

(If you imported from GitHub, `requirements.txt` will be in your project directory.)

## 4) Configure environment variables

In the PythonAnywhere Web tab, find "Environment Variables" and set:

- `SECRET_KEY` : a secure random string
- `DEBUG` : `False`
- `ALLOWED_HOSTS` : `yourusername.pythonanywhere.com` (or comma-separated list)

Example:

```
SECRET_KEY=your-long-secret
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
```

## 5) Static files and media

1. In the Web tab, scroll to the "Static files" section and add mappings:

- URL `/static/` → `/home/yourusername/yourproject/staticfiles/`
- URL `/media/` → `/home/yourusername/yourproject/media/`

2. Run collectstatic on the PythonAnywhere Bash console:

```bash
cd ~/yourproject
source ~/venvs/gossiphy-venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```

## 6) Database & superuser

Run (on the Bash console):

```bash
python manage.py migrate
python manage.py createsuperuser
```

## 7) WSGI configuration and reload

1. In the Web tab, update the WSGI configuration if needed (it should point to your project's `wsgi.py`).
2. Reload the web app from the Web tab.

## Troubleshooting & notes

- If you see static files 404, ensure `STATIC_ROOT` on the server contains your collected files and static mapping in the Web tab points to it.
- Keep `DEBUG=False` in production.
- SQLite is fine for small projects; consider Postgres for scale.
- If you used WhiteNoise, static files will be served without additional mapping, but PythonAnywhere's static mapping is also fine.

If you want, I can now:
- Patch `requirements.txt` automatically (by running a pip freeze in your environment), or
- Create a `start.sh`/`Procfile` or update the repo README.

Tell me which you want next and I will proceed with the change or give exact commands to run locally.
