import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def send_reset_password_email(email, reset_token):
    sender_email = "hola@jonatanjimeneza.com"
    receiver_email = email
    password = "Jaredh2o,13"

    reset_link = f"http://localhost:3000/reset-password/{reset_token}"  # Enlace con el token como parámetro

    message = MIMEMultipart("alternative")
    message["Subject"] = "Reset your password"
    message["From"] = sender_email
    message["To"] = receiver_email

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Password Reset</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background-color: #f9f9f9;
                border-radius: 5px;
                padding: 30px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .logo {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .logo img {{
                max-width: 200px;
                height: auto;
            }}
            h1 {{
                color: #4a4a4a;
                margin-bottom: 20px;
                text-align: center;
            }}
            .button {{
                display: inline-block;
                padding: 12px 24px;
                background-color: #AF4CAB;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                font-weight: bold;
                margin-top: 20px;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 0.9em;
                color: #777;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">
                <img src="http:/localhost:3000/logo.png" alt="CargoBrain">
            </div>
            <h1>Password Reset Request</h1>
            <p>Hello,</p>
            <p>We received a request to reset your password. If you didn't make this request, you can ignore this email.</p>
            <p>To reset your password, click on the button below:</p>
            <p style="text-align: center;">
                <a href="{reset_link}" class="button">Reset Password</a>
            </p>
            <p>This link will expire in 1 hour for security reasons.</p>
            
            <div class="footer">
                <p>This is an automated message, please do not reply to this email.</p>
                <p>&copy; 2024 CargoBrain. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    text = f"""
    Hello,

    We received a request to reset your password. If you didn't make this request, you can ignore this email.

    To reset your password, please visit the following link:
    {reset_link}

    This link will expire in 1 hour for security reasons.

    If you're having trouble with the link, copy and paste the URL into your web browser.

    This is an automated message, please do not reply to this email.

    © 2023 YourCompany. All rights reserved.
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    try:
        with smtplib.SMTP_SSL("smtp.hostinger.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

