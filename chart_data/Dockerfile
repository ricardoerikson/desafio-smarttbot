FROM python:3.7-slim

WORKDIR /chart_data

COPY requirements.txt /chart_data
RUN pip3 install -r requirements.txt

COPY app_chart_data.py /chart_data
COPY poloniex.py /chart_data
COPY candlesticks.py /chart_data
COPY utils.py /chart_data

ENTRYPOINT ["python"]
CMD ["app_chart_data.py"]
