locals {
  s3_origin_id     = "S3"
  lambda_origin_id = "Lambda"
}


resource "aws_cloudfront_distribution" "theyhelpyou" {
  enabled             = true
  aliases             = ["www.theyhelpyou.co.uk"]
  default_root_object = "index.html"

  is_ipv6_enabled = true
  price_class     = "PriceClass_100"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = local.s3_origin_id

    forwarded_values {
      query_string = true

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
  }

  ordered_cache_behavior {
    allowed_methods = [
      "DELETE",
      "GET",
      "HEAD",
      "OPTIONS",
      "PATCH",
      "POST",
      "PUT",
    ]
    cached_methods = [
      "GET",
      "HEAD",
    ]

    path_pattern           = "/api/*"
    target_origin_id       = local.lambda_origin_id
    viewer_protocol_policy = "redirect-to-https"

    forwarded_values {
      query_string = true

      cookies {
        forward = "none"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  logging_config {
    bucket          = aws_s3_bucket.theyhelpyou-logs.bucket_domain_name
    include_cookies = false
  }

  origin {
    domain_name = aws_s3_bucket.theyhelpyou.bucket_regional_domain_name
    origin_id   = local.s3_origin_id
  }

  origin {
    domain_name = "0jknti8qal.execute-api.eu-west-2.amazonaws.com"
    origin_id   = local.lambda_origin_id

    custom_origin_config {
      http_port                = 80
      https_port               = 443
      origin_keepalive_timeout = 5
      origin_protocol_policy   = "https-only"
      origin_read_timeout      = 30
      origin_ssl_protocols = [
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
