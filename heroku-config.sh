#!/bin/bash

for heroku_env in Staging Production;
do
  remote=`echo "${heroku_env}" | awk '{print tolower($0)}'`;
  heroku config:set FLASK_APP=run.py --remote $remote;
  heroku config:set APP_SETTINGS=config.${heroku_env}Config --remote $remote;
  heroku config:set APP_MAIL_USERNAME="myEmailUsername" --remote $remote;
  heroku config:set APP_MAIL_PASSWORD="myEmailPassword" --remote $remote;
  heroku config:set SECRET_KEY="S3cr3t_K#Key" --remote $remote;
  heroku config:set SECURITY_PASSWORD_SALT="S3cr3t_K#SaltPass" --remote $remote;
  heroku config:set TEMPLATES_AUTO_RELOAD=True --remote $remote
  heroku config:set MAIL_DEFAULT_SENDER=flowdash.bio@gmail.com --remote $remote;
done
