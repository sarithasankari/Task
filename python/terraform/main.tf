resource "aws_iam_role" "lambda_role" {
  name = "lambda_search_products_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Action = "sts:AssumeRole",
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}


resource "aws_lambda_function" "search_products" {
  function_name = "search_products"
  filename      = "lambda_function.zip"
  handler       = "lambda_handler.lambda_handler"
  runtime       = "python3.10"
  role          = aws_iam_role.lambda_role.arn
  timeout       = 30
  memory_size   = 1024

  depends_on = [
    aws_iam_role_policy_attachment.lambda_basic
  ]
}


resource "aws_s3_bucket" "products_csv" {
  bucket = var.s3_bucket_name
}


resource "aws_db_instance" "product_db" {
  identifier          = "product-db-instance"
  allocated_storage   = 20
  engine              = "mysql"
  engine_version      = "8.0"
  instance_class      = "db.t3.micro"
  db_name             = "product_db"
  username            = var.db_username
  password            = var.db_password
  publicly_accessible = true
  skip_final_snapshot = true
}
