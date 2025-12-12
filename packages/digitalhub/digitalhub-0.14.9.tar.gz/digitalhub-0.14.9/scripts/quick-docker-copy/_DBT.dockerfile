ARG VERSION=latest
FROM ghcr.io/scc-digitalhub/digitalhub-sdk/wrapper-dbt:${VERSION}

ARG ROOT=/usr/local/lib/python3.9/site-packages
ARG pth=./digitalhub-sdk
ARG pthr=${pth}-runtime-

ARG sdk=digitalhub
ARG rtm=${sdk}_runtime_
ARG dbt=dbt

ARG wpth=./digitalhub-sdk-wrapper-

COPY ${pth}/${sdk} ${ROOT}/${sdk}
COPY ${pthr}${dbt}/${rtm}${dbt} ${ROOT}/${rtm}${dbt}
COPY ${wpth}${dbt}/wrapper.py /app


USER root
RUN chown -R nonroot ${ROOT}/digitalhub*

USER 8877
