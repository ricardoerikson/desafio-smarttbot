FROM python:3.7-slim

WORKDIR /chart_data

COPY requirements.txt /chart_data
RUN pip3 install -r requirements.txt
COPY app.py /chart_data
COPY poloniex.py /chart_data
COPY candlesticks.py /chart_data

ENTRYPOINT ["python"]
CMD ["app.py"]
