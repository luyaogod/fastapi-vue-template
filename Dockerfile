FROM python:3.10.4
ENV PYTHONNUNBUFFERED = 1
WORKDIR /app
COPY ./backend/requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip3 config set install.trusted-host mirrors.aliyun.com
RUN pip3 install -r requirements.txt
COPY . /app
EXPOSE 8000
