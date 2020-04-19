# data "aws_iam_role" "DynamoDBAutoscaleRole" {
#   name = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/aws-service-role/dynamodb.application-autoscaling.amazonaws.com/AWSServiceRoleForApplicationAutoScaling_DynamoDBTable"
# }

resource "aws_dynamodb_table" "community_response_hubs" {
  name           = "community_response_hubs"
  billing_mode   = "PROVISIONED"
  read_capacity  = 10
  write_capacity = 10
  hash_key       = "gss"

  attribute {
    name = "gss"
    type = "S"
  }

  lifecycle {
    ignore_changes = [read_capacity, write_capacity]
  }
}

resource "aws_appautoscaling_target" "community_response_hubs_read_target" {
  max_capacity       = 25
  min_capacity       = 10
  resource_id        = "table/${aws_dynamodb_table.community_response_hubs.name}"
  scalable_dimension = "dynamodb:table:ReadCapacityUnits"
  service_namespace  = "dynamodb"
}

resource "aws_appautoscaling_policy" "community_response_hubs_read_policy" {
  name               = "DynamoDBReadCapacityUtilization:${aws_appautoscaling_target.community_response_hubs_read_target.resource_id}"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.community_response_hubs_read_target.resource_id
  scalable_dimension = aws_appautoscaling_target.community_response_hubs_read_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.community_response_hubs_read_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "DynamoDBReadCapacityUtilization"
    }

    target_value = 70
  }
}

resource "aws_appautoscaling_target" "community_response_hubs_write_target" {
  max_capacity       = 25
  min_capacity       = 10
  resource_id        = "table/${aws_dynamodb_table.community_response_hubs.name}"
  scalable_dimension = "dynamodb:table:WriteCapacityUnits"
  service_namespace  = "dynamodb"
}

resource "aws_appautoscaling_policy" "community_response_hubs_write_policy" {
  name               = "DynamoDBReadCapacityUtilization:${aws_appautoscaling_target.community_response_hubs_write_target.resource_id}"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.community_response_hubs_write_target.resource_id
  scalable_dimension = aws_appautoscaling_target.community_response_hubs_write_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.community_response_hubs_write_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "DynamoDBWriteCapacityUtilization"
    }

    target_value = 70
  }
}

resource "aws_dynamodb_table" "postcode_to_gss" {
  name           = "postcode_to_gss"
  billing_mode   = "PROVISIONED"
  read_capacity  = 10
  write_capacity = 10
  hash_key       = "pcd"

  attribute {
    name = "pcd"
    type = "S"
  }
}

resource "aws_appautoscaling_target" "postcode_to_gss_read_target" {
  max_capacity       = 25
  min_capacity       = 10
  resource_id        = "table/${aws_dynamodb_table.postcode_to_gss.name}"
  scalable_dimension = "dynamodb:table:ReadCapacityUnits"
  service_namespace  = "dynamodb"
}

resource "aws_appautoscaling_policy" "postcode_to_gss_read_policy" {
  name               = "DynamoDBReadCapacityUtilization:${aws_appautoscaling_target.postcode_to_gss_read_target.resource_id}"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.postcode_to_gss_read_target.resource_id
  scalable_dimension = aws_appautoscaling_target.postcode_to_gss_read_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.postcode_to_gss_read_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "DynamoDBReadCapacityUtilization"
    }

    target_value = 70
  }
}

resource "aws_appautoscaling_target" "postcode_to_gss_write_target" {
  max_capacity       = 25
  min_capacity       = 10
  resource_id        = "table/${aws_dynamodb_table.postcode_to_gss.name}"
  scalable_dimension = "dynamodb:table:WriteCapacityUnits"
  service_namespace  = "dynamodb"
}

resource "aws_appautoscaling_policy" "postcode_to_gss_write_policy" {
  name               = "DynamoDBReadCapacityUtilization:${aws_appautoscaling_target.postcode_to_gss_write_target.resource_id}"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.postcode_to_gss_write_target.resource_id
  scalable_dimension = aws_appautoscaling_target.postcode_to_gss_write_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.postcode_to_gss_write_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "DynamoDBWriteCapacityUtilization"
    }

    target_value = 70
  }
}
