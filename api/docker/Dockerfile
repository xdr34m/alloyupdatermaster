FROM docker.mirror.markant.com/python:3.13

WORKDIR /code/app

COPY ../config/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#COPY ../src /code/client 
#is binded into
COPY ../src/main.py /code/app/main.py
COPY ../src/utils.py /code/app/utils.py

COPY ../config/gunicorn.config.py /code/app/gunicorn.config.py

#config is determined in gunicorn.config.py 
CMD ["gunicorn", "-c", "gunicorn.config.py", "main:app"]