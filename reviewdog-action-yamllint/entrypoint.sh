#!/bin/sh

cd "$GITHUB_WORKSPACE" || exit

git config --global --add safe.directory $GITHUB_WORKSPACE

export REVIEWDOG_GITHUB_API_TOKEN="${INPUT_GITHUB_TOKEN}"

echo '::group:: Running yamllint with reviewdog 🐶 ...'
yamllint --version
yamllint --format "parsable" ${INPUT_YAMLLINT_FLAGS:-'.'} |
    reviewdog \
        -efm="%f:%l:%c: %m" \
        -name "yamllint" \
        -reporter="${INPUT_REPORTER:-github-pr-check}" \
        -level="${INPUT_LEVEL}" \
        -filter-mode="${INPUT_FILTER_MODE}" \
        -fail-level="${INPUT_FAIL_LEVEL}" \
        -fail-on-error="${INPUT_FAIL_ON_ERROR}" \
        ${INPUT_REVIEWDOG_FLAGS}
EXIT_CODE=$?
echo '::endgroup::'

exit $EXIT_CODE
