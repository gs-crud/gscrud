FROM python:3.9
WORKDIR /
COPY ./src /src
COPY ./requirements.txt /requirements.txt
COPY ./setup.py /setup.py
RUN pip install -r /requirements.txt
RUN pip install -e .
CMD ["uvicorn", "gscrud.controllers.app:app", "--host", "0.0.0.0", "--port", "80"]