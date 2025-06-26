"""
Script de sauvegarde automatique à planifier via cron.
"""
import subprocess
import sys
import os
import glob
import smtplib
from email.mime.text import MIMEText

backup_script = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backup.py'))

def cleanup_old_backups(backup_dir, keep=7):
    """Supprime les backups les plus anciens, ne garde que les N plus récents."""
    files = sorted(glob.glob(os.path.join(backup_dir, 'sync_local_*.db')), reverse=True)
    for old_file in files[keep:]:
        os.remove(old_file)
    log_dirs = sorted(glob.glob(os.path.join(backup_dir, 'logs_*')), reverse=True)
    for old_dir in log_dirs[keep:]:
        if os.path.isdir(old_dir):
            import shutil
            shutil.rmtree(old_dir)

def send_notification(subject, body, to_email):
    from_email = os.getenv('BACKUP_MAIL_FROM', 'backup@localhost')
    smtp_server = os.getenv('BACKUP_SMTP_SERVER', 'localhost')
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    try:
        with smtplib.SMTP(smtp_server) as server:
            server.sendmail(from_email, [to_email], msg.as_string())
    except Exception as e:
        print(f"Erreur envoi mail backup : {e}")

def send_slack_notification(message):
    webhook_url = os.getenv('BACKUP_SLACK_WEBHOOK')
    if not webhook_url:
        return
    import requests
    try:
        requests.post(webhook_url, json={"text": message})
    except Exception as e:
        print(f"Erreur envoi Slack : {e}")

if __name__ == '__main__':
    subprocess.run([sys.executable, backup_script])
    # Nettoyage des anciens backups (garde les 7 plus récents)
    backup_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../backups'))
    cleanup_old_backups(backup_dir, keep=7)
    # Notification email
    to_email = os.getenv('BACKUP_MAIL_TO')
    notif_msg = f'Backup effectué avec succès dans {backup_dir} le {__import__("datetime").datetime.now()}'
    if to_email:
        send_notification(
            subject='Backup WooCommerce-Odoo OK',
            body=notif_msg,
            to_email=to_email
        )
    # Notification Slack
    send_slack_notification(notif_msg)
