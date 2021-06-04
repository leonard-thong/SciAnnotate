FROM python:3.7.9
WORKDIR /
RUN git clone https://github.com/leonard-thong/SciAnnotate.git /SciAnnotate && cd SciAnnotate && git checkout label_function_dev && bash ./docker_install.sh
WORKDIR /SciAnnotate
ENTRYPOINT ["python3", "standalone.py"]