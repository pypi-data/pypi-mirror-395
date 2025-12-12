#!/bin/bash
set -e

# Redirect stderr to stdout for better logging
exec 2>&1

if [ "${PYTEST}" = 'TRUE' ]; then
    # run unit tests
    python -m pytest -v tests/
else
    if [ "${LOCALRUN}" = 'TRUE' ]; then
        # run with reload on file change for local dev
        python -m streamlit run 'src/app/App.py' \
            --server.port=$PORT \
            --server.address=0.0.0.0 \
            --server.maxUploadSize=32 \
            --server.maxMessageSize=256 \
            --server.runOnSave=true \
            --server.fileWatcherType=poll \
            --server.enableWebsocketCompression=true \
            --browser.gatherUsageStats=false

    else
        python -m streamlit run 'src/app/App.py' \
            --server.port=$PORT \
            --server.address=0.0.0.0 \
            --server.maxUploadSize=32 \
            --server.maxMessageSize=256 \
            --server.runOnSave=false \
            --server.enableWebsocketCompression=true \
            --browser.gatherUsageStats=false
    fi
fi
