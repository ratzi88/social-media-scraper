# AWS VPC with Terraform

This Terraform configuration creates an AWS Virtual Private Cloud (VPC) with public and private subnets, an internet gateway, and a single NAT gateway. It sets up routing for both public and private subnets to enable internet access for resources as required.

## Resources Created

### VPC
- **CIDR block**: `10.0.0.0/16`
- DNS support and DNS hostnames enabled.

### Subnets
- **Public Subnets**:
  - `10.0.1.0/24` in `eu-central-1a`
  - `10.0.2.0/24` in `eu-central-1b`
- **Private Subnets**:
  - `10.0.3.0/24` in `eu-central-1a`
  - `10.0.4.0/24` in `eu-central-1b`

### Internet Gateway
- Attached to the VPC for public internet access.

### NAT Gateway
- A single NAT Gateway in the first public subnet (`eu-central-1a`).
- Used by private subnets for outbound internet access.

### Route Tables
- A shared **public route table** for public subnets.
- A shared **private route table** for private subnets, routing through the NAT Gateway.
