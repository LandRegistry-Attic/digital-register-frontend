# digital-register-frontend

This is the repo for the frontend of the digital register service. It is written in Python, with the Flask framework.

### Digital Register Frontend build status

[![Build Status](http://52.16.47.1/job/digital-register-frontend-unit-tests%20(Master)/badge/icon)](http://52.16.47.1/job/digital-register-frontend-unit-tests%20(Master)/)

### Digital Register Frontend Acceptance tests status
[![Build Status](http://52.16.47.1/job/digital-register-frontend-acceptance-tests/badge/icon)](http://52.16.47.1/job/digital-register-frontend-acceptance-tests/)

## Setup

To create a virtual env, run the following from a shell:

```
    mkvirtualenv -p /usr/bin/python3 digital-register-frontend
    source environment.sh
    pip install -r requirements.txt
```

## Run the tests

To run the tests for the Digital Register, go to its folder and run `lr-run-tests`.

## Run the acceptance tests

To run the acceptance tests for the Digital Register, go to the `acceptance-tests` folder and run:
```
   ./run-tests.sh
```

You will need to have a Postgres database running (see `db/lr-start-db` and `db/insert-fake-data` scripts in the [centos-dev-env](https://github.com/LandRegistry/centos-dev-env) project), as well as the digital-register-frontend and digital-register-api applications running on your development VM.

## Run the server

### Run in dev mode

To run the server in dev mode, execute the following command:

    ./run_flask_dev.sh

### Run using gunicorn

To run the server using gunicorn, activate your virtual environment, add the application directory to python path
(e.g. `export PYTHONPATH=/vagrant/apps/digital-register-frontend/:$PYTHONPATH`) and execute the following commands:

    pip install gunicorn
    gunicorn -p /tmp/gunicorn-digital-register-frontend.pid service.server:app -c gunicorn_settings.py


## Jenkins builds

We use three separate builds:
- [branch](http://52.16.47.1/job/digital-register-frontend-unit-tests%20(Branch)/)
- [master](http://52.16.47.1/job/digital-register-frontend-unit-tests%20(Master)/)
- [acceptance](http://52.16.47.1/job/digital-register-frontend-acceptance-tests/)


## Third Party Tools

<a href="http://www.browserstack.com"><img src="https://www.browserstack.com/images/layout/browserstack-logo-600x315.png" alt="browserstack logo" width=300/></a>

<p>This repo is being tested using browserstack</p>
<p><i>Rapid Selenium webdriver testing with 100% reliability</i></p>



