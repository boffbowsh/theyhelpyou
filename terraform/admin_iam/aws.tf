provider "aws" {
  version = "~> 2.0"
  region  = "eu-west-2"
}

terraform {
  backend "s3" {
    bucket         = "theyhelpyou-terraform"
    key            = "theyhelpyou_admin.tfstate"
    region         = "eu-west-2"
    dynamodb_table = "theyhelpyou-terraform"
  }
}