FROM public.ecr.aws/lambda/python:3.11

COPY pipeline_alerts_email ${LAMBDA_TASK_ROOT}/pipeline_alerts_email

COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --no-cache-dir -r requirements.txt

CMD ["set-me-in-serverless.yaml"]
