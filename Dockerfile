FROM python:3.7
MAINTAINER Jan Slod

ENV PYTHONBUFFERED 1

COPY requirements.txt /requirements.txt
RUN echo "ipv6" >> /etc/modules
RUN apt-get install default-libmysqlclient-dev
RUN pip install -r /requirements.txt

RUN mkdir /home_budget
WORKDIR /home_budget
COPY . /home_budget
EXPOSE 8000

RUN useradd -ms /bin/bash user
RUN chown -R user:user /home_budget
RUN chmod -R 755 /home_budget
USER user
