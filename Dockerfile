FROM python:3.7.9
WORKDIR /
RUN git clone https://github.com/leonard-thong/dlwlrat.git /dlwlrat && cd dlwlrat && git checkout lmy-dev && bash ./docker_install.sh
WORKDIR /dlwlrat
CMD ["python3", "standalone.py"]