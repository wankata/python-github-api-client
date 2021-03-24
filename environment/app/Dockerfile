FROM python:3
 ENV PYTHONUNBUFFERED=1
 RUN python -m pip install --upgrade pip
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 ADD dev_requirements.txt /code/
 RUN pip install -r dev_requirements.txt
