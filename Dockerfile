FROM public.ecr.aws/lambda/python:3.12

COPY pipeline_alerts_email ${LAMBDA_TASK_ROOT}/pipeline_alerts_email

COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --no-cache-dir -r requirements.txt

RUN dnf install shadow-utils -y
RUN /sbin/groupadd -r app
RUN /sbin/useradd -r -g app app
RUN chown -R app:app ${LAMBDA_TASK_ROOT}
USER app

CMD ["set-me-in-serverless.yaml"]
