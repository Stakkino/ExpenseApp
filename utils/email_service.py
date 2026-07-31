import random
import smtplib
from email.message import EmailMessage


GMAIL_SENDER = "expenseapp@gmail.com"
APP_PASSWORD = "XXXX XXXX XXXX XXXX"

def envoyer_otp(email_destinataire):
    try:
        otp = str(random.randint(100000, 999999))
        msg = EmailMessage()
        msg["Subject"] = "Verification Expense Application"
        msg["From"] = GMAIL_SENDER
        msg["To"] = email_destinataire
        msg.set_content(f"""
                Bonjour,

                Votre code de verification est :
                {otp}
                Ce code expire dans 5 minutes.

                Expense Application
                """)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_SENDER, APP_PASSWORD)
            smtp.send_message(msg)

        return otp

    except Exception as e:
        print("Erreur Email :", e)
        return None