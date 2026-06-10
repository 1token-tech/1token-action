FROM python:alpine

ENV REVIEWDOG_VERSION=v0.20.3

RUN wget -O - -q https://raw.githubusercontent.com/reviewdog/reviewdog/fd59714416d6d9a1c0692d872e38e7f8448df4fc/install.sh| sh -s -- -b /usr/local/bin/ ${REVIEWDOG_VERSION}
RUN apk --no-cache add git

RUN pip install "pyyaml<=5.3.1" "yamllint"

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
