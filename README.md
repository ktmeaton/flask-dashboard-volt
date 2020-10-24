# flowdash-bio

Workflow Dashboard for Bioinformatics

## Run

```bash
# Get the code
git clone https://github.com/ktmeaton/flowdash-bio.git
cd flowdash-bio

# Install environment
conda env create -f environment.yaml
conda activate flowdash-bio

# Start the app
flask run --host=0.0.0.0 --port=5000
# Access the dashboard in browser: http://127.0.0.1:5000/

```

## Deploy

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

# Create the Heroku project, staging and production
heroku create flowdash-bio
heroku create flowdash-bio-stage

# Add production and staging remotes
git remote add production git@heroku.com:flowdash-bio.git
git remote add staging git@heroku.com:flowdash-bio-stage.git

# Configure database
heroku addons:create --remote production heroku-postgresql:hobby-dev
heroku addons:create --remote staging heroku-postgresql:hobby-dev

# Setup env var for heroku
# First edit heroku-config.sh with your information
./heroku-config.sh

# Check the new config
heroku config --remote staging
heroku config --remote production

# Trigger the LIVE deploy
git push heroku staging

$ # Open the LIVE app in browser
heroku open
```

> Note, you may need to export the variable BROWSER which points to the executable for your web browser.

```bash
export BROWSER="/mnt/c/Program\ Files\ \(x86\)/Google/Chrome/Application/chrome.exe"
```

### Local PostgreSQL

> Configure a local postgresql database instead of sqlite

```bash
# Initialize the general database
initdb -D local-psql-db

# Start the database server
pg_ctl -D local-psql-db -l logfile start

# Create a postgres user
createuser --encrypted --pwprompt postgres

# Create the flowdash-bio database
createdb --owner=postgres flowdash-bio

# List databases to confirm theirs a db called "flowdash-bio" owned by postgres
psql -U postgres -c "\l"

# Go register a new account via the web app, and check if they show up in the database
psql -U postgres flowdash-bio -c "SELECT * FROM \"User\""

# Stop database server when finished
pg_ctl -D local-psql-db -l stop
```

## Credits & Links

- [Flask Framework](https://www.palletsprojects.com/p/flask/) - The offcial website
- [Boilerplate Code](https://appseed.us/boilerplate-code) - Index provided by **AppSeed**
- [Boilerplate Code](https://github.com/app-generator/boilerplate-code) - Index published on Github
- [Flask Dashboard Volt](https://appseed.us/admin-dashboards/flask-dashboard-volt) - Provided by **AppSeed** [Web App Generator](https://appseed.us/app-generator).
