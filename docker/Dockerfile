FROM python:3.9.9
ENV RETRY=3
ENV BACKOFF_FACTOR=1
ENV PYTHONPATH=/data
RUN apt update -y
RUN pip install --upgrade pip
RUN pip install python-dotenv fastapi uvicorn typer requests
COPY start.py /usr/local/bin
RUN chmod u+x /usr/local/bin/start.py
EXPOSE 8000
ENTRYPOINT ["/usr/local/bin/start.py" ] 