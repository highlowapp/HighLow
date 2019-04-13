FROM python:rc-stretch
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["python"]
CMD gunicorn -w 4 -b 0.0.0.0:80 wsgi
