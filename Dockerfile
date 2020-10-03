FROM python:3.8-alpine as base

FROM base as builder
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt

FROM base
COPY --from=builder /install /usr/local
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /home/appuser
USER appuser

COPY bibcheck.py ./
CMD ["python", "./bibcheck.py"]
