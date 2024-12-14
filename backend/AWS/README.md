# AWS VPC with Terraform

This Terraform configuration creates an AWS Virtual Private Cloud (VPC) with public subnets, an internet gateway, and two EC2 instances. It sets up routing for the public subnets to enable internet access for resources as required.

---

## **Changes Made**
- Updated to include EC2 instances (`vm_1a` and `vm_1b`) in public subnets.
- Security group (`allow_ssh`) added to allow SSH access (port 22) from all IPs.
- Added `tags` variable to ensure consistent tagging for resources.
- Adjusted the configuration to match the newly added components, including the user data for instance initialization.

**Date of Update**: December 14, 2024

---

## **Resources Created**

### **VPC**
- **CIDR block**: `10.0.0.0/16`
- DNS support and DNS hostnames enabled.

### **Subnets**
- **Public Subnets**:
  - `10.0.1.0/24` in `eu-central-1a`
  - `10.0.2.0/24` in `eu-central-1b`

### **Internet Gateway**
- Attached to the VPC for public internet access.

### **Route Table**
- A shared **public route table** for public subnets, routing through the internet gateway.

### **Security Group**
- **Name**: `allow-ssh`
- Allows inbound SSH (port 22) from all IPs.
- Allows all outbound traffic.

### **EC2 Instances**
- **AMI**: `ami-0a628e1e89aaedf80` (Ubuntu-based image, replace with the desired AMI ID as needed).
- **Instances**:
  - `vm_1a`: Deployed in `public_1a` subnet (AZ: `eu-central-1a`).
  - `vm_1b`: Deployed in `public_1b` subnet (AZ: `eu-central-1b`).
- **User Data**:
  - Updates and installs basic packages on instance startup.

---

## **Usage**

1. **Prepare the Environment**:
   - Ensure Terraform is installed.
   - Set up your AWS CLI with appropriate credentials.

2. **Apply Configuration**:
   - terraform init
   - terraform plan
   - terraform apply

3. **Access EC2 Instances**;
   - Use the assigned public IPs of the EC2 instances.
   - SSH into the instances:
   - ssh -i /path/to/your-key.pem ubuntu@<public-ip>