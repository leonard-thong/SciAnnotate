FROM python:3.7
WORKDIR /
RUN git clone https://github.com/dreamyang-liu/SciAnnotate.git /SciAnnotate && cd SciAnnotate && git checkout label_function_dev && bash ./docker_install.sh
WORKDIR /SciAnnotate
ENTRYPOINT ["python3", "standalone.py"]