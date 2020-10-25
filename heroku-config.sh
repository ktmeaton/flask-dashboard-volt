#!/bin/bash

for heroku_env in Staging Production;
do
  remote=`echo "${heroku_env}" | awk '{print tolower($0)}'`;
  heroku config:set FLASK_ENV="$remote" --remote $remote;
  heroku config:set APP_MAIL_USERNAME="myEmailUsername" --remote $remote;
  heroku config:set APP_MAIL_PASSWORD="myEmailPassword" --remote $remote;
  heroku config:set SECRET_KEY="S3cr3t_K#Key" --remote $remote;
done
