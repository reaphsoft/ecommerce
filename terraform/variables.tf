# variables.tf
variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"
}
variable "ami_id" {
  description = "AMI ID for Ubuntu 22.04 in us-east-1"
  default     = "ami-053b0d53c279acc90"
}
variable "instance_type" {
  description = "EC2 instance type"
  default     = "t2.micro"
}
variable "key_name" {
  description = "SSH key name"
  default     = "deployer-key"
}
variable "public_key_path" {
  description = "Path to your SSH public key"
  default     = "~/.ssh/id_ed25519.pub"
}
variable "your_ip_cidr" {
  description = "Your IP address in CIDR notation, for SSH security"
  default     = "78.146.243.31/32"
}
