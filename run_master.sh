#!/usr/bin/env bash
gunicorn --bind 0.0.0.0:80 --workers=1 --access-logfile access.log --error-logfile error.log master_app:master --reload
