FROM python:3.9
RUN apt -y update && apt -y install python3 python3-pip git python3-all-dev vim python3-lldb strace
RUN python3 -m pip install django gpustat pudb flask

ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

WORKDIR /workdir
COPY lib lib

#ENTRYPOINT ["python3", "-m", "pudb", "/workdir/lib/server.py"]
ENTRYPOINT ["python3", "/workdir/lib/server.py"]
