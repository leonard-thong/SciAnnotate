FROM python:3.7.9
WORKDIR /
RUN git clone https://github.com/leonard-thong/brat.git /brat && cd brat && git checkout lmy-dev && bash ./docker_install.sh
WORKDIR /brat
CMD ["python3", "standalone.py"]