import aiosmtplib
from email.message import EmailMessage
from email.utils import formatdate


async def send_email_async(subject, message, from_addr, to_addr, csv_file):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Date"] = formatdate(localtime=True)
    msg.set_content(message)

    with open(csv_file, "rb") as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=csv_file)

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'vikas@innovquant.com'
    smtp_password = 'rmpmakmpgekzjmse'
    
    try:
        client = aiosmtplib.SMTP(hostname=smtp_server, port=smtp_port)
        await client.connect()
        #print('ok')
        #await client.starttls()
        #print('ok1')
        await client.login(smtp_user, smtp_password)
        #print('ok2')
        await client.send_message(msg)
        await client.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")