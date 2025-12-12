import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional

from agentgear.server.app.models import SMTPSettings

def send_email(smtp_config: SMTPSettings, recipients: List[str], subject: str, html_content: str):
    if not smtp_config or not smtp_config.enabled:
        raise ValueError("SMTP is not configured or enabled")

    msg = MIMEMultipart()
    msg["From"] = smtp_config.sender_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))

    try:
        server = smtplib.SMTP(smtp_config.host, smtp_config.port)
        if smtp_config.encryption == "starttls":
            server.starttls()
        elif smtp_config.encryption == "ssl":
            server = smtplib.SMTP_SSL(smtp_config.host, smtp_config.port)
        
        if smtp_config.username and smtp_config.password:
            server.login(smtp_config.username, smtp_config.password)
        
        server.sendmail(smtp_config.sender_email, recipients, msg.as_string())
        server.quit()
    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")
