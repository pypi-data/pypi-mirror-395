ARG VERSION=latest
FROM ghcr.io/scc-digitalhub/digitalhub-serverless/python-runtime:3.11-${VERSION}

ARG ROOT=/usr/local/lib/python3.11/site-packages
ARG pth=./digitalhub-sdk
ARG pthr=${pth}-runtime-
ARG sdk=digitalhub
ARG rtm=${sdk}_runtime_

ARG py=python
ARG cont=container
ARG kfp=kfp
ARG dbt=dbt
ARG mdl=modelserve
ARG hera=hera
ARG flw=flower


COPY ${pth}/${sdk} ${ROOT}/${sdk}
COPY ${pthr}${py}/${rtm}${py} ${ROOT}/${rtm}${py}
COPY ${pthr}${cont}/${rtm}${cont} ${ROOT}/${rtm}${cont}
COPY ${pthr}${kfp}/${rtm}${kfp} ${ROOT}/${rtm}${kfp}
COPY ${pthr}${dbt}/${rtm}${dbt} ${ROOT}/${rtm}${dbt}
COPY ${pthr}${mdl}/${rtm}${mdl} ${ROOT}/${rtm}${mdl}
COPY ${pthr}${hera}/${rtm}${hera} ${ROOT}/${rtm}${hera}
COPY ${pthr}${flw}/${rtm}${flw} ${ROOT}/${rtm}${flw}

COPY ./run_handler.py /opt/nuclio
