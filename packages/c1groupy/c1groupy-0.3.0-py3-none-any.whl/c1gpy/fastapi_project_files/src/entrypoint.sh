#!/bin/bash
## Main script for starting up FastAPI WSGI server or tests in a container

# Redirect stderr to stdout for better logging
exec 2>&1

if [ "${PYTEST}" = 'TRUE' ]
then
    python -m pytest -v tests/  # run Pytest framework
else # run FastAPI
    if [ "${LOCALRUN}" = 'TRUE' ]
    then
        python -m hypercorn api_interface:rest_api --bind :$PORT --reload --workers 4 --worker-class uvloop # run with reload for local dev
    else
          python -m hypercorn api_interface:rest_api --bind :$PORT --workers 4 --worker-class uvloop
    fi
fi
