# ======================================================================================================================

# Authors: BERKYT

# ======================================================================================================================


FROM python:3.9-slim as builder

# Директория скрипта
WORKDIR /q_1

# Переменные окружения python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

FROM python:3.9-slim

# Директория скрипта
WORKDIR /q_1

COPY --from=builder /q_1 .

ADD q_1.py /q_1

EXPOSE 1234
