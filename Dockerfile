FROM python:3.9-bullseye

WORKDIR /server

COPY start_server.sh start_server.sh

COPY requirments.txt requirments.txt
RUN python3 -m pip install -r requirments.txt

COPY . .

CMD ["./start_server.sh"]
