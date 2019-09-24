FROM python:3.7

COPY bibcheck.py /
CMD ["python", "bibcheck.py"]
