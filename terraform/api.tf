resource "aws_apigatewayv2_api" "theyhelpyou" {
  name          = "theyhelpyou"
  protocol_type = "HTTP"

  cors_configuration {
    allow_credentials = false
    allow_headers     = []
    allow_methods     = ["GET"]
    allow_origins     = ["*"]
    expose_headers    = []
    max_age           = 3600
  }
}

resource "aws_apigatewayv2_route" "export_for_llm" {
  api_id    = aws_apigatewayv2_api.theyhelpyou.id
  route_key = "GET /api/export-local-links-manager"
  target    = "integrations/${aws_apigatewayv2_integration.export_for_llm.id}"
}

resource "aws_apigatewayv2_integration" "export_for_llm" {
  api_id                 = aws_apigatewayv2_api.theyhelpyou.id
  integration_type       = "AWS_PROXY"
  payload_format_version = "2.0"
  timeout_milliseconds   = 29000
  integration_method     = "POST"
  integration_uri        = aws_lambda_function.export_for_llm.invoke_arn

  lifecycle {
    ignore_changes = [passthrough_behavior] # Buggy - can only be set on WebSocket APIs
  }
}

resource "aws_apigatewayv2_route" "fetch_by_postcode" {
  api_id    = aws_apigatewayv2_api.theyhelpyou.id
  route_key = "GET /api/postcode"
  target    = "integrations/${aws_apigatewayv2_integration.fetch_by_postcode.id}"
}

resource "aws_apigatewayv2_integration" "fetch_by_postcode" {
  api_id                 = aws_apigatewayv2_api.theyhelpyou.id
  integration_type       = "AWS_PROXY"
  payload_format_version = "2.0"
  timeout_milliseconds   = 29000
  integration_method     = "POST"
  integration_uri        = aws_lambda_function.fetch_by_postcode.invoke_arn

  lifecycle {
    ignore_changes = [passthrough_behavior]
  }
}

resource "aws_apigatewayv2_route" "import_sheet" {
  api_id    = aws_apigatewayv2_api.theyhelpyou.id
  route_key = "POST /api/import"
  target    = "integrations/${aws_apigatewayv2_integration.import_sheet.id}"
}

resource "aws_apigatewayv2_integration" "import_sheet" {
  api_id                 = aws_apigatewayv2_api.theyhelpyou.id
  integration_type       = "AWS_PROXY"
  payload_format_version = "2.0"
  timeout_milliseconds   = 29000
  integration_method     = "POST"
  integration_uri        = aws_lambda_function.import_sheet.invoke_arn

  lifecycle {
    ignore_changes = [passthrough_behavior]
  }
}

resource "aws_apigatewayv2_route" "report_a_problem" {
  api_id    = aws_apigatewayv2_api.theyhelpyou.id
  route_key = "POST /api/report-a-problem"
  target    = "integrations/${aws_apigatewayv2_integration.report_a_problem.id}"
}

resource "aws_apigatewayv2_integration" "report_a_problem" {
  api_id                 = aws_apigatewayv2_api.theyhelpyou.id
  integration_type       = "AWS_PROXY"
  payload_format_version = "2.0"
  timeout_milliseconds   = 29000
  integration_method     = "POST"
  integration_uri        = aws_lambda_function.report_a_problem.invoke_arn

  lifecycle {
    ignore_changes = [passthrough_behavior]
  }
}

resource "aws_apigatewayv2_route" "update_attr" {
  api_id    = aws_apigatewayv2_api.theyhelpyou.id
  route_key = "POST /api/update"
  target    = "integrations/${aws_apigatewayv2_integration.update_attr.id}"
}

resource "aws_apigatewayv2_integration" "update_attr" {
  api_id                 = aws_apigatewayv2_api.theyhelpyou.id
  integration_type       = "AWS_PROXY"
  payload_format_version = "2.0"
  timeout_milliseconds   = 29000
  integration_method     = "POST"
  integration_uri        = aws_lambda_function.update_attr.invoke_arn

  lifecycle {
    ignore_changes = [passthrough_behavior]
  }
}
