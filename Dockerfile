FROM python:3.6

#RUN mkdir -p /usr/src/app
RUN python -m pip install -U --force-reinstall pip

#RUN git clone --recursive "https://github.com/0-ng/end_web.git" /usr/src/app
WORKDIR /usr/src/app
COPY ./ ./
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD ["gunicorn", "manage:app", "-c", "./gunicorn.conf.py", "--log-level", "debug"]
#CMD ["/usr/local/bi/gunicorn", "-w", "5", "-b", ":8000", "-k", "gevent", "manage:app"]