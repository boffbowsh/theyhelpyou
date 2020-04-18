resource aws_iam_group "theyhelpyou-admins" {
  name = "theyhelpyou-admins"
  path = "/users/"
}

data "aws_iam_policy_document" "terraform_state" {
  statement {
    actions   = ["s3:ListBucket"]
    resources = ["arn:aws:s3:::theyhelpyou-terraform"]
  }
  statement {
    actions   = ["s3:GetObject", "s3:PutObject"]
    resources = ["arn:aws:s3:::theyhelpyou-terraform/theyhelpyou.tfstate"]
  }
  statement {
    actions   = ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:DeleteItem"]
    resources = ["arn:aws:dynamodb:*:*:table/theyhelpyou-terraform"]
  }
}

resource "aws_iam_policy" "terraform_state" {
  policy = data.aws_iam_policy_document.terraform_state.json
}

resource "aws_iam_group_policy_attachment" "theyhelpyou-admins_terraform_state" {
  group      = aws_iam_group.theyhelpyou-admins.name
  policy_arn = aws_iam_policy.terraform_state.arn
}
