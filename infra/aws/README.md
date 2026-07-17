# AWS infrastructure boundary

This directory is reserved for the reviewed infrastructure-as-code
implementation of ADR 0001. The selected production components are Route 53,
ACM, CloudFront, WAF, ALB, ECS Fargate, RDS PostgreSQL Multi-AZ, SQS/DLQ, S3,
ECR, Secrets Manager, KMS, CloudWatch and AWS Backup.

No deployable infrastructure is asserted by the foundation milestone. The
selected region is `eu-central-1`; regional durable state and backups must not
use cross-region replication. Implementation must follow the jurisdiction and
transfer record plus the later network, backup, RPO/RTO, monitoring, cost and
security decisions, and must be tested before production use.
