FROM python:3.8

ARG file="server.py"
ADD $file /
ENV fileName=$file

# RUN apt-get update && apt-get install -y python3 && apt install -y python3-pip

COPY requirements.txt .
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]
CMD [ "server.py" ]