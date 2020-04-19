resource "aws_iam_role" "theyhelpyou-lambdas" {
  name               = "theyhelpyou-lambda"
  path               = "/service-role/"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_policy" "theyhelpyou-lambda_logging" {
  name        = "theyhelpyou-lambda_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/theyhelpyou_*"
            ]
        }
    ]
}
EOF
}

resource "aws_iam_policy" "theyhelpyou-lambda_xray" {
  name        = "theyhelpyou-lambda_xray"
  path        = "/"
  description = "IAM policy for tracing from a lambda"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": {
        "Effect": "Allow",
        "Action": [
            "xray:PutTraceSegments",
            "xray:PutTelemetryRecords"
        ],
        "Resource": [
            "*"
        ]
    }
}
EOF
}

resource "aws_iam_policy" "theyhelpyou-lambda_dynamodb" {
  name        = "theyhelpyou-lambda_dynamodb"
  path        = "/"
  description = "IAM policy for tracing from a lambda"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:BatchWriteItem",
                "dynamodb:PutItem",
                "dynamodb:DescribeTable",
                "dynamodb:DeleteItem",
                "dynamodb:GetItem",
                "dynamodb:Scan",
                "dynamodb:UpdateItem"
            ],
            "Resource": [
                "arn:aws:dynamodb:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:table/community_response_hubs",
                "arn:aws:dynamodb:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:table/postcode_to_gss"
            ]
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.theyhelpyou-lambdas.name
  policy_arn = aws_iam_policy.theyhelpyou-lambda_logging.arn
}

resource "aws_iam_role_policy_attachment" "lambda_xray" {
  role       = aws_iam_role.theyhelpyou-lambdas.name
  policy_arn = aws_iam_policy.theyhelpyou-lambda_xray.arn
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb" {
  role       = aws_iam_role.theyhelpyou-lambdas.name
  policy_arn = aws_iam_policy.theyhelpyou-lambda_dynamodb.arn
}
