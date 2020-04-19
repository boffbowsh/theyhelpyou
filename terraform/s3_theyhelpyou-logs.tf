resource "aws_s3_bucket" "theyhelpyou-logs" {
  grant {
    id          = "b652a45401fab37d176a73e73abff8ec79063a29626c6374be4a2916dd71a166"
    permissions = ["FULL_CONTROL"]
    type        = "CanonicalUser"
  }
  grant {
    id          = "c4c1ede66af53448b93c283ce9448c4ba468c9432aa01d700d3878632f77d2d0"
    permissions = ["FULL_CONTROL"]
    type        = "CanonicalUser"
  }
}