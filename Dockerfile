FROM python:3.7.9
WORKDIR /
RUN git clone https://github.com/leonard-thong/SciAnnotate.git /SciAnnotate && cd SciAnnotate && git checkout lmy-dev && bash ./docker_install.sh
WORKDIR /SciAnnotate
CMD ["python3", "standalone.py"]