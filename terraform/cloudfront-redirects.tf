locals {
  redirects_origin_id = "S3"
}

resource "aws_cloudfront_distribution" "theyhelpyou-redirects" {
  enabled = true
  aliases = [
    "theyhelpyou.co.uk",
    "theyhelpyou.com",
    "www.theyhelpyou.com"
  ]

  is_ipv6_enabled = true
  price_class     = "PriceClass_100"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = local.redirects_origin_id

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  logging_config {
    bucket          = aws_s3_bucket.theyhelpyou-logs.bucket_domain_name
    include_cookies = false
    prefix          = "redirects"
  }

  origin {
    domain_name = aws_s3_bucket.theyhelpyou-redirects.website_endpoint
    origin_id   = local.s3_origin_id

    custom_origin_config {
      http_port                = 80
      https_port               = 443
      origin_keepalive_timeout = 5
      origin_protocol_policy   = "http-only"
      origin_read_timeout      = 30
      origin_ssl_protocols = [
        "TLSv1",
        "TLSv1.1",
        "TLSv1.2",
      ]
    }
  }

  viewer_certificate {
    acm_certificate_arn      = "arn:aws:acm:us-east-1:${data.aws_caller_identity.current.account_id}:certificate/30816dbe-4609-4623-8853-d6ec6ec90bd3"
    minimum_protocol_version = "TLSv1.1_2016"
    ssl_support_method       = "sni-only"
  }
}
