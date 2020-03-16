FROM python:3
COPY main.py /app/
COPY requirements.txt /app/requirements.txt
ADD pip.conf /root/.pip/
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

COPY download-to-oss.tar.gz /app/
RUN pip install /app/download-to-oss.tar.gz
CMD ["gunicorn", "-w", "2", "-b","0.0.0.0:5000","--access-logfile","-","--error-logfile","-","--log-file","-","download_to_oss:app"]
