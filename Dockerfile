FROM python:3.7

RUN useradd --create-home appuser

COPY requirements.txt /home/appuser
RUN pip install -r /home/appuser/requirements.txt


WORKDIR /home/appuser
USER appuser

COPY bibcheck.py ./
CMD ["python", "./bibcheck.py"]
