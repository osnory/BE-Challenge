FROM python:3.9-buster

# set work directory
WORKDIR /opt

# install dependencies
RUN pip install --upgrade pip
ADD requirements /tmp/requirements
RUN pip install -r /tmp/requirements/prod.txt && rm -rf /tmp/requirements


# copy project and run files
ADD revenue/ /opt/revenue
ADD app.py /opt/
ADD manage.py /opt/

# copy the data files
ADD data/ /opt/data

ENV PYTHONPATH=/opt
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "manage:app"]
