#!/usr/bin/env bash

set -euxo pipefail
UPSTREAM_REPO="${UPSTREAM_REPO:-$1}"
UPSTREAM_BRANCH="${UPSTREAM_BRANCH:-$2}"
DOWNSTREAM_REPO="${DOWNSTREAM_REPO:-$3}"
DOWNSTREAM_BRANCH="${DOWNSTREAM_BRANCH:-$4}"
IGNORE_FILES="${IGNORE_FILES:-$5}"
FETCH_ARGS="${FETCH_ARGS:-$6}"
MERGE_ARGS="${MERGE_ARGS:-$7}"
PUSH_ARGS="${PUSH_ARGS:-$8}"
GITHUB_TOKEN="${GITHUB_TOKEN:-$9}"



git clone $DOWNSTREAM_REPO --branch ${DOWNSTREAM_BRANCH} work


cd work || { echo "Missing work dir" && exit 2 ; }
git remote set-url origin "https://x-access-token:${GITHUB_TOKEN}@github.com/${DOWNSTREAM_REPO/https:\/\/github.com\//}"


git config --local user.password ${GITHUB_TOKEN}
git config --global merge.ours.driver true

git remote add upstream "$UPSTREAM_REPO"

git remote -v

git fetch ${FETCH_ARGS} upstream

git checkout ${DOWNSTREAM_BRANCH}


if [ -n "$IGNORE_FILES" ]; then
    IFS=', ' read -r -a exclusions <<< "$IGNORE_FILES"
    for exclusion in "${exclusions[@]}"
    do
        echo "$exclusion merge=ours" >> .gitattributes
    done
fi

cat .gitattributes

MERGE_RESULT=$(git merge ${MERGE_ARGS} ${UPSTREAM_BRANCH})
git status


if [[ $MERGE_RESULT == "" ]] || [[ $MERGE_RESULT == *"merge failed"* ]] || [[ $MERGE_RESULT == *"CONFLICT ("* ]]
then
  echo "Merge Failed! Exiting..."
  exit 1
elif [[ $MERGE_RESULT != *"Already up to date."* ]]
then
  git push ${PUSH_ARGS} origin ${DOWNSTREAM_BRANCH} || exit $?
fi

cd ..
rm -rf work