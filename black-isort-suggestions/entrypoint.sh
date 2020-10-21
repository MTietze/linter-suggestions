#!/bin/sh
set -e

if [[ -z "$GITHUB_TOKEN" ]]; then
	echo "The GITHUB_TOKEN is required."
	exit 1
fi

cd $GITHUB_WORKSPACE

black .
isort ./*.py


COMMIT_SHA=$(cat $GITHUB_EVENT_PATH | jq -r .pull_request.head.sha)
COMMENTS_URL=$(cat /github/workflow/event.json | jq -r .pull_request.review_comments_url)

python ./black-isort-suggestions/gitdiff.py $COMMIT_SHA $COMMENTS_URL $GITHUB_TOKEN

exit 0

