from flask_mail import Message

def send_reset_email(mail, to_email, reset_link, sender):
    msg = Message('Password Reset', sender=sender, recipients=[to_email])
    msg.body = f"Use this link to reset your password (valid for a short time): {reset_link}"
    mail.send(msg)