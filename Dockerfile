FROM python:3.13.5-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install --upgrade pip wheel "poetry==2.1.4"

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY my_project .

COPY my_project/prestart.sh .
COPY my_project/main.py .

RUN chmod +x prestart.sh
RUN chmod +x main.py

ENTRYPOINT ["./prestart.sh"]

CMD ["python", "main.py"]