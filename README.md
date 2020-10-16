# flowdash-bio

Workflow Dashboard for Bioinformatics

## Setup

```bash
# Get the code
git clone https://github.com/ktmeaton/flowdash-bio.git
cd flowdash-bio

# Install environment
conda env create -f environment.yaml
conda activate flowdash-bio

# Configure the app
export FLASK_APP=run.py
export FLASK_ENV=development

# Start the app
flask run --host=0.0.0.0 --port=5000
# Access the dashboard in browser: http://127.0.0.1:5000/
```

## Deployment

The app is provided with a basic configuration to be executed in [Docker](https://www.docker.com/), [Heroku](https://www.heroku.com/), [Gunicorn](https://gunicorn.org/), and [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/).

### [Heroku](https://www.heroku.com/)

---

Steps to deploy on **Heroku**

- [Create a FREE account](https://signup.heroku.com/) on Heroku platform
- [Install the Heroku CLI](https://devcenter.heroku.com/articles/getting-started-with-python#set-up) that match your OS: Mac, Unix or Windows
- Open a terminal window and authenticate via `heroku login` command
- Clone the sources and push the project for LIVE deployment

```bash
# Check Heroku CLI is installed
heroku -v
heroku/7.25.0 win32-x64 node-v12.13.0 # <-- All good

# Check Heroku CLI is installed
heroku login
# this commaond will open a browser window - click the login button (in browser)

# Create the Heroku project
heroku create

# Trigger the LIVE deploy
git push heroku master

$ # Open the LIVE app in browser
heroku open
```

> Note, you may need to export the variable BROWSER which points to the executable for your web browser.

```bash
export BROWSER="/mnt/c/Program\ Files\ \(x86\)/Google/Chrome/Application/chrome.exe"
```

### [Gunicorn](https://gunicorn.org/)

---

Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX.

> Start the app using gunicorn binary

```bash
gunicorn --bind 0.0.0.0:8001 run:app
```

Visit `http://localhost:8001` in your browser. The app should be up & running.

### [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/)

---

> Start the app using [waitress-serve](https://docs.pylonsproject.org/projects/waitress/en/stable/runner.html).

```bash
waitress-serve --port=8001 run:app
```

Visit `http://localhost:8001` in your browser. The app should be up & running.

### [Docker](https://www.docker.com/) execution

---

The application can be easily executed in a docker container. The steps:

> Start the app in Docker

```bash
sudo docker-compose pull && sudo docker-compose build && sudo docker-compose up -d
```

Visit `http://localhost:5005` in your browser. The app should be up & running.

## Credits & Links

- [Flask Framework](https://www.palletsprojects.com/p/flask/) - The offcial website
- [Boilerplate Code](https://appseed.us/boilerplate-code) - Index provided by **AppSeed**
- [Boilerplate Code](https://github.com/app-generator/boilerplate-code) - Index published on Github
- [Flask Dashboard Volt](https://appseed.us/admin-dashboards/flask-dashboard-volt) - Provided by **AppSeed** [Web App Generator](https://appseed.us/app-generator).
