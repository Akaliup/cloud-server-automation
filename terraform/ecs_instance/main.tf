provider "alicloud" {
  region = "cn-hangzhou"
}

# 创建VPC
resource "alicloud_vpc" "main" {
  name       = "my-vpc"
  cidr_block = "172.16.0.0/12"
}

# 创建交换机
resource "alicloud_vswitch" "main" {
  vpc_id            = alicloud_vpc.main.id
  cidr_block        = "172.16.0.0/16"
  availability_zone = "cn-hangzhou-i"
  name              = "my-vswitch"
}

# 创建安全组
resource "alicloud_security_group" "main" {
  name        = "my-security-group"
  description = "Security group for web server"
  vpc_id      = alicloud_vpc.main.id
}

# 安全组规则
resource "alicloud_security_group_rule" "allow_http" {
  type              = "ingress"
  ip_protocol       = "tcp"
  nic_type          = "intranet"
  policy            = "accept"
  port_range        = "80/80"
  priority          = 1
  security_group_id = alicloud_security_group.main.id
  cidr_ip           = "0.0.0.0/0"
}

# 创建ECS实例
resource "alicloud_instance" "main" {
  image_id              = "ubuntu_20_04_x64_20G_alibase_20240109.vhd"
  instance_type         = "ecs.t6-c1m2.large"
  instance_name         = "web-server"
  security_groups       = [alicloud_security_group.main.id]
  vswitch_id            = alicloud_vswitch.main.id
  internet_charge_type  = "PayByTraffic"
  internet_max_bandwidth_out = 10
  system_disk_category  = "cloud_efficiency"
  password              = "YourPassword123"
  host_name             = "web-server"
  zone_id               = "cn-hangzhou-i"
}

# 输出公网IP
output "public_ip" {
  value = alicloud_instance.main.public_ip
}    