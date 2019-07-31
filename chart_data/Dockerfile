FROM desafio-smarttbot:latest

WORKDIR /chart_data

COPY app_chart_data.py /chart_data
COPY poloniex.py /chart_data
COPY candlesticks.py /chart_data
COPY utils.py /chart_data

ENTRYPOINT ["python"]
CMD ["app_chart_data.py"]
