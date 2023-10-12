FROM python:latest
EXPOSE 5969
WORKDIR /flaskapp
RUN pip install -r requirements.txt
COPY . .
CMD python ./app.py
