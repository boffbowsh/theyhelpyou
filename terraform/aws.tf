provider "aws" {
  version = "~> 2.0"
  region  = "eu-west-2"
}

terraform {
  backend "s3" {
    bucket         = "theyhelpyou-terraform"
    key            = "theyhelpyou.tfstate"
    region         = "eu-west-2"
    dynamodb_table = "theyhelpyou-terraform"
  }
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
