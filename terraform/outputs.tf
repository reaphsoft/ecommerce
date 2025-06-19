# outputs.tf
output "instance_public_ip" {
  description = "Public IP of the deployed EC2 instance"
  value       = aws_instance.flask.public_ip
}
