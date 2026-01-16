output "s3_bucket_name" {
  value = aws_s3_bucket.products_csv.bucket
}

output "rds_endpoint" {
  value = aws_db_instance.product_db.endpoint
}
