FROM python:3.10.4
ENV PYTHONNUNBUFFERED = 1
WORKDIR /app
COPY ./backend/reuirements reuirements
RUN pip3 install --upgrade pip
RUN pip3 install -r reuirements.txt
COPY . /app
EXPOSE 8000
