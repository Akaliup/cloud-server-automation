#!/bin/bash
# 云服务器自动化备份脚本

# 配置信息
BACKUP_DIR="/data/backups"
SOURCE_DIRS="/etc /var/www /home"
DB_USER="root"
DB_PASSWORD="your_password"
DB_NAMES="mydb1 mydb2"
RETENTION_DAYS=7

# 创建备份目录
mkdir -p $BACKUP_DIR/$(date +%Y%m%d)

# 备份文件系统
for dir in $SOURCE_DIRS; do
    tar -czf $BACKUP_DIR/$(date +%Y%m%d)/$(basename $dir)_$(date +%Y%m%d).tar.gz $dir
done

# 备份MySQL数据库
for db in $DB_NAMES; do
    mysqldump -u $DB_USER -p$DB_PASSWORD $db > $BACKUP_DIR/$(date +%Y%m%d)/${db}_$(date +%Y%m%d).sql
done

# 清理旧备份
find $BACKUP_DIR -type d -mtime +$RETENTION_DAYS -exec rm -rf {} \;

# 上传到OSS(可选)
# ossutil64 cp -r $BACKUP_DIR/$(date +%Y%m%d) oss://your-bucket/backups/    