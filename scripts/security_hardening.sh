#!/bin/bash
# 服务器安全加固脚本

# 1. 禁用root远程登录
sed -i 's/PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config

# 2. 限制SSH访问IP
echo "AllowUsers admin@192.168.1.0/24" >> /etc/ssh/sshd_config

# 3. 配置防火墙
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

# 4. 更新系统
apt update && apt upgrade -y

# 5. 安装Fail2Ban防止暴力破解
apt install fail2ban -y
systemctl enable fail2ban
systemctl start fail2ban

# 6. 配置日志审计
apt install auditd -y
systemctl enable auditd
systemctl start auditd

# 重启SSH服务使配置生效
systemctl restart sshd    