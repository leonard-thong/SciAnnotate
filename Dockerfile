FROM python:3.7.9
WORKDIR /
RUN git clone https://github.com/leonard-thong/brat.git /dlmat && cd dlmat && git checkout lmy-dev && bash ./docker_install.sh
WORKDIR /dlmat
CMD ["python3", "standalone.py"]