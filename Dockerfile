# This Dockerfile is used to build a Docker image for a simple Flask application.
# It starts with a base image of Python 3.9 slim, sets the working directory
# to /app, copies the current directory's contents into the container, installs
# the required Python packages from requirements.txt, exposes port 8080, and

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py .

# CMD ensures that Flask runs on port 8080

CMD ["python","app.py"]
