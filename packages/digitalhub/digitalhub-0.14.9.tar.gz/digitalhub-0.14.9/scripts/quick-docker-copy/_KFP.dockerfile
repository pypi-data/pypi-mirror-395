ARG VERSION=latest
FROM ghcr.io/scc-digitalhub/digitalhub-sdk/wrapper-kfp:${VERSION}

ARG ROOT=/usr/local/lib/python3.9/site-packages
ARG pth=./digitalhub-sdk
ARG pthr=${pth}-runtime-
ARG sdk=digitalhub
ARG rtm=${sdk}_runtime_
ARG py=python
ARG cont=container
ARG kfp=kfp
ARG dbt=dbt
ARG mdl=modelserve
ARG wpth=./digitalhub-sdk-wrapper-

COPY ${pth}/${sdk} ${ROOT}/${sdk}
COPY ${pthr}${py}/${rtm}${py} ${ROOT}/${rtm}${py}
COPY ${pthr}${cont}/${rtm}${cont} ${ROOT}/${rtm}${cont}
COPY ${pthr}${kfp}/${rtm}${kfp} ${ROOT}/${rtm}${kfp}
COPY ${pthr}${dbt}/${rtm}${dbt} ${ROOT}/${rtm}${dbt}
COPY ${pthr}${mdl}/${rtm}${mdl} ${ROOT}/${rtm}${mdl}
COPY ${wpth}${kfp}/wrapper.py /app
COPY ${wpth}${kfp}/step.py /app

USER root
RUN chown -R nonroot ${ROOT}/digitalhub*
RUN chown -R nonroot /app/*


USER 8877
