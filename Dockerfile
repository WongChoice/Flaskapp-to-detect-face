FROM python:latest
EXPOSE 0
WORKDIR /flaskapp
RUN pip install flaskapp
COPY . .
CMD [ "flask","RUN","--host","0.0.0.0" ]
