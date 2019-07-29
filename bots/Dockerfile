FROM python:3.7-slim

WORKDIR /bots

COPY requirements.txt /bots
RUN pip3 install -r requirements.txt
COPY app_bots.py /bots

ENTRYPOINT ["python"]
CMD ["app_bots.py"]
