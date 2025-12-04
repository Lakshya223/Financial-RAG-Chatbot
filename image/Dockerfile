FROM public.ecr.aws/lambda/python:3.11

# Install system dependencies

RUN yum install -y gcc gcc-c++ make curl && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    source $HOME/.cargo/env && \
    yum clean all

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install --upgrade pip \
    && pip install pysqlite3-binary \
    && pip install -r requirements.txt

EXPOSE 8000
ENV IS_USING_IMAGE_RUNTIME=True

COPY backend/ ${LAMBDA_TASK_ROOT}/
COPY scripts/ ${LAMBDA_TASK_ROOT}/scripts/
