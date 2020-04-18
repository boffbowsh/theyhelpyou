resource "aws_s3_bucket" "theyhelpyou" {
  acl           = "private"
  force_destroy = false
}

resource "aws_s3_bucket_policy" "theyhelpyou" {
  bucket = aws_s3_bucket.theyhelpyou.bucket
  policy = <<POLICY
{
    "Id": "PolicyForCloudFrontPrivateContent",
    "Statement":[
        {
            "Action": "s3:GetObject",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity E33JNERF5G3PG3"
            },
            "Resource": "${aws_s3_bucket.theyhelpyou.arn}/*"
        }
    ],
    "Version": "2008-10-17"
}
POLICY
}
