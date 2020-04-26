resource "aws_cloudwatch_event_rule" "theyhelpyou-import_sheet-900" {
    name = "theyhelpyou-import_sheet-900"
    schedule_expression = "rate(15 minutes)"
}

resource "aws_cloudwatch_event_target" "theyhelpyou-import_sheet-900" {
    rule = aws_cloudwatch_event_rule.theyhelpyou-import_sheet-900.name
    arn = aws_lambda_function.import_sheet.arn
}

resource "aws_cloudwatch_event_rule" "theyhelpyou-import_from_llm-5am" {
    name = "theyhelpyou-import_from_llm-5am"
    schedule_expression = "cron(0 5 * * ? *)"
}

resource "aws_cloudwatch_event_target" "theyhelpyou-import_from_llm-5am" {
    rule = aws_cloudwatch_event_rule.theyhelpyou-import_from_llm-5am.name
    arn = aws_lambda_function.import_from_llm.arn
}
