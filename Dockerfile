FROM python:3.9

RUN sed -i "s@http://deb.debian.org@http://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list
RUN rm -Rf /var/lib/apt/lists/*
RUN apt-get update

ENV APP_ROOT /code
WORKDIR ${APP_ROOT}/
COPY requirements.txt ${APP_ROOT}/
RUN pip install -r requirements.txt

ENV TIME_ZONE=Asia/Shanghai
RUN echo "${TIME_ZONE}" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime
COPY . ${APP_ROOT}
RUN find . -name "*.pyc" -delete
CMD ["python","live_main.py"]