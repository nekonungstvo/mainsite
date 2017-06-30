FROM debian
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip
EXPOSE 8000
ADD . /mainsite
WORKDIR mainsite
RUN pip3 install -r requirements.txt
CMD ["gunicorn", "-w", "4", "app:app"]