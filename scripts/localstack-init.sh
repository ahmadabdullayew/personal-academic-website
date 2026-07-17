#!/bin/sh
set -eu

: "${S3_BUCKET_QUARANTINE:?S3_BUCKET_QUARANTINE is required}"
: "${S3_BUCKET_PRIVATE:?S3_BUCKET_PRIVATE is required}"
: "${S3_BUCKET_PUBLIC:?S3_BUCKET_PUBLIC is required}"
: "${SQS_QUEUE_URL:?SQS_QUEUE_URL is required}"

for bucket in "${S3_BUCKET_QUARANTINE}" "${S3_BUCKET_PRIVATE}" "${S3_BUCKET_PUBLIC}"; do
  if ! awslocal s3api head-bucket --bucket "${bucket}" >/dev/null 2>&1; then
    awslocal s3api create-bucket --bucket "${bucket}" >/dev/null
  fi
done

queue_name=${SQS_QUEUE_URL##*/}
if [ -z "${queue_name}" ]; then
  echo "SQS_QUEUE_URL must end with a queue name" >&2
  exit 1
fi

dead_letter_queue_name="${queue_name}-dlq"
if ! awslocal sqs get-queue-url --queue-name "${dead_letter_queue_name}" >/dev/null 2>&1; then
  awslocal sqs create-queue --queue-name "${dead_letter_queue_name}" >/dev/null
fi

dead_letter_queue_arn=$(awslocal sqs get-queue-attributes \
  --queue-url "$(awslocal sqs get-queue-url --queue-name "${dead_letter_queue_name}" --query QueueUrl --output text)" \
  --attribute-names QueueArn \
  --query Attributes.QueueArn \
  --output text)
redrive_attributes=$(printf \
  '{"RedrivePolicy":"{\\"deadLetterTargetArn\\":\\"%s\\",\\"maxReceiveCount\\":\\"5\\"}"}' \
  "${dead_letter_queue_arn}")

if ! awslocal sqs get-queue-url --queue-name "${queue_name}" >/dev/null 2>&1; then
  awslocal sqs create-queue \
    --queue-name "${queue_name}" \
    --attributes "${redrive_attributes}" >/dev/null
else
  queue_url=$(awslocal sqs get-queue-url --queue-name "${queue_name}" --query QueueUrl --output text)
  awslocal sqs set-queue-attributes \
    --queue-url "${queue_url}" \
    --attributes "${redrive_attributes}" >/dev/null
fi
