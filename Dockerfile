FROM python:3-onbuild
LABEL maintainer "cclauss@bluewin.ch"
# ENV port=8080
CMD [ "python", "./server.py", "90000"]
