resource "aws_s3_bucket" "theyhelpyou-redirects" {
  website {
    redirect_all_requests_to = "https://www.theyhelpyou.co.uk"
  }
}

resource "aws_s3_bucket_policy" "theyhelpyou-redirects" {
  bucket = aws_s3_bucket.theyhelpyou-redirects.bucket
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
            "Resource": "${aws_s3_bucket.theyhelpyou-redirects.arn}/*"
        }
    ],
    "Version": "2008-10-17"
}
POLICY
}
