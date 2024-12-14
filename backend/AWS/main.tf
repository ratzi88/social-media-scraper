# Provider configuration
provider "aws" {
  region = "eu-central-1"
}

# Variable for tags
variable "tags" {
  default = {
    Name = "testing"
  }
}

# VPC
resource "aws_vpc" "my_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags                 = var.tags
}

# Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.my_vpc.id
  tags   = var.tags
}

# Public Subnets
resource "aws_subnet" "public_1a" {
  vpc_id                  = aws_vpc.my_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "eu-central-1a"
  map_public_ip_on_launch = true
  tags                    = var.tags
}

resource "aws_subnet" "public_1b" {
  vpc_id                  = aws_vpc.my_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "eu-central-1b"
  map_public_ip_on_launch = true
  tags                    = var.tags
}

# Route Table
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.my_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = var.tags
}

# Route Table Associations
resource "aws_route_table_association" "public_1a" {
  subnet_id      = aws_subnet.public_1a.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "public_1b" {
  subnet_id      = aws_subnet.public_1b.id
  route_table_id = aws_route_table.public_rt.id
}

# Security Group
resource "aws_security_group" "allow_ssh" {
  name   = "allow-ssh"
  vpc_id = aws_vpc.my_vpc.id  # Ensure it matches the VPC where your EC2 instances are being created

  # Inbound rule for SSH
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = var.tags
}



# EC2 Instances

resource "aws_instance" "vm_1a" {
  ami                    = "ami-0a628e1e89aaedf80"
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.public_1a.id
  associate_public_ip_address = true
  # key_name = "enter key pair name if already exists one"
  user_data = <<-EOF
              #!/bin/bash
              sudo apt update -y
              sudo apt install -y
              EOF

  tags = var.tags
}


resource "aws_instance" "vm_1b" {
  ami                    = "ami-0a628e1e89aaedf80"
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.public_1b.id
  associate_public_ip_address = true
  # key_name = "enter key pair name if already exists one" 
  user_data = <<-EOF
              #!/bin/bash
              sudo apt update -y
              sudo apt install -y
              EOF

  tags = var.tags
}