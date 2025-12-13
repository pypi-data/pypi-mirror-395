# Web Report Protection and Automation for Pristy Support

This guide explains how to password-protect Pristy Support reports published on a web server, and how to automate their generation with systemd.

## Table of Contents

- [Apache Protection](#apache-protection-ubuntudebian)
- [nginx Protection](#nginx-protection-ubuntudebiancentos)
- [Nightly Automated Audit](#nightly-automated-audit-systemd-timer)



## Apache Protection (Ubuntu/Debian)

### Prerequisites

- Apache installed (`apache2` on Ubuntu/Debian)
- `auth_basic` module enabled (enabled by default)
- Reports published to `/var/www/html/pristy-support` (configurable)

### Configuration

#### 1. Create Password File

```bash
# Create file with first user
sudo htpasswd -c /etc/apache2/.htpasswd-pristy admin
# Enter password twice when prompted
```

#### 2. Add Additional Users

```bash
# Add more users (without -c to avoid overwriting file)
sudo htpasswd /etc/apache2/.htpasswd-pristy user2
sudo htpasswd /etc/apache2/.htpasswd-pristy user3
```

#### 3. Create .htaccess File

Create `/var/www/html/pristy-support/.htaccess`:

```apache
AuthType Basic
AuthName "Pristy Support Reports - Restricted Access"
AuthUserFile /etc/apache2/.htpasswd-pristy
Require valid-user

# Optional: customize error page
ErrorDocument 401 "Unauthorized access. Please authenticate."
```

**With sudo:**

```bash
sudo tee /var/www/html/pristy-support/.htaccess > /dev/null << 'EOF'
AuthType Basic
AuthName "Pristy Support Reports - Restricted Access"
AuthUserFile /etc/apache2/.htpasswd-pristy
Require valid-user
EOF
```

#### 4. Verify Apache Configuration

Ensure Apache allows `.htaccess` files in this directory.

Edit the vhost configuration file (`/etc/apache2/sites-available/000-default.conf` or your custom vhost):

```apache
<VirtualHost *:80>
    ServerName example.com
    DocumentRoot /var/www/html

    <Directory /var/www/html/pristy-support>
        AllowOverride AuthConfig
        Require all granted
    </Directory>

    # ... rest of configuration
</VirtualHost>
```

**Note**: If `AllowOverride` is already set to `All`, no modification needed.

#### 5. Reload Apache

```bash
# Check syntax
sudo apache2ctl configtest

# If OK, reload
sudo systemctl reload apache2
```

#### 6. Test

Access `http://your-server/pristy-support/` in a browser. An authentication prompt should appear.

### User Management

```bash
# List users (indirect, via file content)
sudo cat /etc/apache2/.htpasswd-pristy

# Delete a user
sudo htpasswd -D /etc/apache2/.htpasswd-pristy user2

# Change user password
sudo htpasswd /etc/apache2/.htpasswd-pristy admin
```



## nginx Protection (Ubuntu/Debian/CentOS)

### Prerequisites

- nginx installed
- `htpasswd` utility available via:
  - `apache2-utils` (Ubuntu/Debian)
  - `httpd-tools` (CentOS/RHEL)

### Tool Installation

#### Ubuntu/Debian

```bash
sudo apt update
sudo apt install apache2-utils
```

#### CentOS/RHEL

```bash
sudo yum install httpd-tools
```

### Configuration

#### 1. Create Password File

```bash
# Create file with first user
sudo htpasswd -c /etc/nginx/.htpasswd-pristy admin
# Enter password twice
```

#### 2. Add Additional Users

```bash
# Add more users
sudo htpasswd /etc/nginx/.htpasswd-pristy user2
```

#### 3. Configure nginx

Edit the nginx configuration file:
- **Ubuntu/Debian**: `/etc/nginx/sites-available/default` or your vhost
- **CentOS**: `/etc/nginx/conf.d/default.conf` or your vhost

Add `auth_basic` configuration in the `location` block:

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html;

    location /pristy-support/ {
        auth_basic "Pristy Support Reports - Restricted Access";
        auth_basic_user_file /etc/nginx/.htpasswd-pristy;

        # Optional: enable automatic indexing if no index.html
        autoindex on;
        autoindex_exact_size off;
        autoindex_localtime on;
    }

    # ... rest of configuration
}
```

#### 4. Test and Reload nginx

```bash
# Test syntax
sudo nginx -t

# If OK, reload
sudo systemctl reload nginx
```

#### 5. Test

Access `http://your-server/pristy-support/` in a browser. An authentication prompt should appear.

### User Management

```bash
# List users
sudo cat /etc/nginx/.htpasswd-pristy

# Delete a user
sudo htpasswd -D /etc/nginx/.htpasswd-pristy user2

# Change password
sudo htpasswd /etc/nginx/.htpasswd-pristy admin
```



## Automated Audit (systemd timer)

To automate report generation, we use a **systemd timer** (recommended on modern systemd-based systems).

### Advantages of systemd Timers

- ✅ Native on modern Ubuntu/Debian/CentOS
- ✅ Centralized logs with `journalctl`
- ✅ Manages missed runs (if server was off)
- ✅ Built-in random delay to avoid simultaneous load
- ✅ No need for crond

### Configuration

#### 1. Create systemd Service

Create `/etc/systemd/system/pristy-support-audit.service`:

```ini
[Unit]
Description=Pristy Support Audit
Documentation=https://gitlab.com/pristy-oss/pristy-support
After=network.target

[Service]
Type=oneshot
User=root

# Audit command with HTML generation (automatically published if enabled in config)
ExecStart=/usr/local/bin/pristy-support audit --format html --format markdown

# Working directory (optional)
WorkingDirectory=/tmp

# Environment variables (if necessary)
# Environment="PATH=/usr/local/bin:/usr/bin:/bin"

# Timeout (30 minutes max for audit)
TimeoutStartSec=30min

# Notifications (optional)
# OnFailure=status-email@%n.service

[Install]
WantedBy=multi-user.target
```

**Using the following command:**

```bash
sudo tee /etc/systemd/system/pristy-support-audit.service > /dev/null << 'EOF'
[Unit]
Description=Pristy Support Audit
Documentation=https://gitlab.com/pristy-oss/pristy-support
After=network.target

[Service]
Type=oneshot
User=root
ExecStart=/usr/local/bin/pristy-support audit --format html --format markdown
WorkingDirectory=/tmp
TimeoutStartSec=30min

[Install]
WantedBy=multi-user.target
EOF
```

#### 2. Create systemd Timer

Create `/etc/systemd/system/pristy-support-audit.timer`:

```ini
[Unit]
Description=Pristy Support Audit Timer (nightly at 2:00 AM)
Requires=pristy-support-audit.service

[Timer]
# Run daily at 2:00 AM
OnCalendar=*-*-* 02:00:00

# Add random delay of 0-30 minutes
# Avoids simultaneous load if multiple servers
RandomizedDelaySec=30min

# Persist missed executions
# If server was off, catch up execution on startup
Persistent=true

# Timezone (optional, defaults to system)
# OnCalendar uses system timezone

[Install]
WantedBy=timers.target
```

**Using the following command:**

```bash
sudo tee /etc/systemd/system/pristy-support-audit.timer > /dev/null << 'EOF'
[Unit]
Description=Pristy Support Audit Timer (nightly at 2:00 AM)
Requires=pristy-support-audit.service

[Timer]
OnCalendar=*-*-* 02:00:00
RandomizedDelaySec=30min
Persistent=true

[Install]
WantedBy=timers.target
EOF
```

#### 3. Enable and Start Timer

```bash
# Reload systemd configuration
sudo systemctl daemon-reload

# Enable timer at boot
sudo systemctl enable pristy-support-audit.timer

# Start timer
sudo systemctl start pristy-support-audit.timer

# Check status
sudo systemctl status pristy-support-audit.timer
```

#### 4. Check Next Executions

```bash
# List all active timers
sudo systemctl list-timers

# See specifically Pristy timer
sudo systemctl list-timers --all | grep pristy
```

**Example output:**

```
NEXT                        LEFT          LAST  PASSED  UNIT                          ACTIVATES
Wed 2025-01-22 02:00:00 CET 6h 23min left -     -       pristy-support-audit.timer    pristy-support-audit.service
```

#### 5. Test Manually

```bash
# Run service once now (without waiting for timer)
sudo systemctl start pristy-support-audit.service

# View execution logs
sudo journalctl -u pristy-support-audit.service -n 100 --no-pager

# Follow logs in real-time
sudo journalctl -u pristy-support-audit.service -f
```

#### 6. View Execution History

```bash
# Last executions of service
sudo journalctl -u pristy-support-audit.service --since "7 days ago"

# Logs with readable timestamps
sudo journalctl -u pristy-support-audit.service -o short-iso
```

### Schedule Customization

The `OnCalendar` parameter accepts many formats:

#### Simple Examples

```ini
# Every day at 3:30 AM
OnCalendar=*-*-* 03:30:00

# Every Monday at 2:00 AM
OnCalendar=Mon *-*-* 02:00:00

# First day of month at 1:00 AM
OnCalendar=*-*-01 01:00:00

# Every hour
OnCalendar=hourly

# Every day at midnight
OnCalendar=daily
```

#### Advanced Examples

```ini
# Monday to Friday at 2:00 AM (weekdays)
OnCalendar=Mon-Fri *-*-* 02:00:00

# Multiple schedules (run twice daily)
OnCalendar=*-*-* 02:00:00
OnCalendar=*-*-* 14:00:00

# Sunday at 3:00 AM
OnCalendar=Sun *-*-* 03:00:00
```

### Report Rotation Management

With the `web_publish.keep_reports: 10` configuration, only the **10 most recent reports** are automatically kept.

Check published reports:

```bash
# List reports
ls -lh /var/www/html/pristy-support/

# Count reports
ls -1 /var/www/html/pristy-support/audit-*.html | wc -l
```

### Email Notification (Optional)

To receive an email on audit failure:

#### 1. Install MTA

```bash
# Ubuntu/Debian
sudo apt install postfix mailutils

# CentOS
sudo yum install postfix mailx
```

#### 2. Create Notification Service

Create `/etc/systemd/system/status-email@.service`:

```ini
[Unit]
Description=Status email for %i

[Service]
Type=oneshot
ExecStart=/bin/sh -c 'systemctl status %i | mail -s "Service %i failed" admin@example.com'
```

#### 3. Enable Notification

Modify `pristy-support-audit.service`:

```ini
[Service]
...
OnFailure=status-email@%n.service
```

### Temporary Disable

```bash
# Stop timer
sudo systemctl stop pristy-support-audit.timer

# Disable at boot
sudo systemctl disable pristy-support-audit.timer

# Check status
sudo systemctl status pristy-support-audit.timer
```

### Complete Removal

```bash
# Stop and disable
sudo systemctl stop pristy-support-audit.timer
sudo systemctl disable pristy-support-audit.timer

# Remove files
sudo rm /etc/systemd/system/pristy-support-audit.service
sudo rm /etc/systemd/system/pristy-support-audit.timer

# Reload systemd
sudo systemctl daemon-reload
```


## Complete Recommended Configuration

### 1. Enable Web Publishing

Edit `/etc/pristy-support/config.yml` (or your config file):

```yaml
web_publish:
  enabled: true
  destination_path: /var/www/html/pristy-support
  keep_reports: 10
  create_index: true
```

### 2. Configure Automated Audit

```bash
# Create systemd files (see above)
sudo systemctl daemon-reload
sudo systemctl enable --now pristy-support-audit.timer
```

### 3. Password Protect

Follow [Apache](#apache-protection-ubuntudebian) or [nginx](#nginx-protection-ubuntudebiancentos) instructions depending on your web server.

### 4. Verify

```bash
# Test audit manually
sudo pristy-support audit --format html

# Check publication
ls -lh /var/www/html/pristy-support/

# Access via browser
# http://your-server/pristy-support/
```


## Troubleshooting

### Apache: 500 Internal Server Error

**Cause**: Incorrect `.htaccess` configuration or `AllowOverride` not configured.

**Solution**:

```bash
# Check Apache logs
sudo tail -f /var/log/apache2/error.log

# Verify AllowOverride is configured
sudo grep -r "AllowOverride" /etc/apache2/
```

### nginx: 401 but no login prompt

**Cause**: Wrong path to `.htpasswd` file.

**Solution**:

```bash
# Verify file exists
ls -l /etc/nginx/.htpasswd-pristy

# Check permissions
sudo chmod 644 /etc/nginx/.htpasswd-pristy

# Check nginx logs
sudo tail -f /var/log/nginx/error.log
```

### systemd: Timer won't start

**Cause**: Syntax error in `.service` or `.timer` files.

**Solution**:

```bash
# Verify syntax
sudo systemd-analyze verify pristy-support-audit.service
sudo systemd-analyze verify pristy-support-audit.timer

# View detailed logs
sudo journalctl -xe
```

### Reports Not Published

**Cause**: `web_publish.enabled: false` or permission error.

**Solution**:

```bash
# Check config
pristy-support --config /etc/pristy-support/config.yml audit --format html

# Check directory permissions
ls -ld /var/www/html/pristy-support/

# Test manually with sudo
sudo mkdir -p /var/www/html/pristy-support
sudo touch /var/www/html/pristy-support/test.html
```


## Security

### Recommendations

- ✅ Use HTTPS (Let's Encrypt) to encrypt passwords in transit
- ✅ Use strong passwords (12+ characters)
- ✅ Limit access by IP if possible (via firewall)
- ✅ Monitor access logs to detect connection attempts
- ✅ Change passwords regularly

### IP Restriction (Optional)

#### Apache

```apache
<Directory /var/www/html/pristy-support>
    AuthType Basic
    AuthName "Pristy Support Reports"
    AuthUserFile /etc/apache2/.htpasswd-pristy
    Require valid-user

    # Restrict by IP
    Require ip 192.168.1.0/24
    Require ip 10.0.0.0/8
</Directory>
```

#### nginx

```nginx
location /pristy-support/ {
    auth_basic "Pristy Support Reports";
    auth_basic_user_file /etc/nginx/.htpasswd-pristy;

    # Restrict by IP
    allow 192.168.1.0/24;
    allow 10.0.0.0/8;
    deny all;
}
```
