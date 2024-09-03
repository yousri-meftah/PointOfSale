FROM python:3.11-alpine

WORKDIR /backend

RUN apk add --no-cache gcc musl-dev postgresql-dev

RUN pip install --upgrade pip

COPY backend/requirements.txt /backend/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend folder
COPY backend /backend


EXPOSE 8000
