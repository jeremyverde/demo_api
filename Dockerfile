FROM library/python:3.11-slim-bookworm
RUN adduser nonroot
WORKDIR /code

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./src src

USER nonroot
CMD ["uvicorn", "src.main:app","--host", "0.0.0.0", "--port", "8000"]
