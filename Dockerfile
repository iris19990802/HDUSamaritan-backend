FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak && \
    echo "deb https://mirrors.ustc.edu.cn/debian/ buster main contrib non-free" >/etc/apt/sources.list && \
    echo "deb https://mirrors.ustc.edu.cn/debian/ buster-updates main contrib non-free" >>/etc/apt/sources.list && \
    echo "deb https://mirrors.ustc.edu.cn/debian/ buster-proposed-updates main contrib non-free" >>/etc/apt/sources.list && \
    echo "deb https://mirrors.ustc.edu.cn/debian-security/ buster/updates main contrib non-free" >>/etc/apt/sources.list

RUN apt-get update

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

COPY . /code/