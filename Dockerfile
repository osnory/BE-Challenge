FROM python:3.9-buster

# set work directory
WORKDIR /opt

# install dependencies
RUN pip install --upgrade pip
ADD requirements /tmp/requirements
RUN pip install -r /tmp/requirements/prod.txt && rm -rf /tmp/requirements


# copy project
# ADD revenue /opt/revenue
ADD revenue/ /opt/revenue
ADD app.py /opt/
ADD manage.py /opt/

ENV PYTHONPATH=/opt
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "manage:app"]

