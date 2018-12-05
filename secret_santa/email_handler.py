import smtplib

class EmailHandler:
    def __init__(self, email, password, server='smtp.gmail.com', port=587):
        self.server = smtplib.SMTP(server, port)
        self.server.starttls()
        self.server.login(email, password)
        self.email = email

    def sendmail(self, to, message):
        self.server.sendmail(self.email, to, message)

    def cleanup(self):
        self.server.quit()

def get_template(toName, toEmail, fromName, fromEmail):
    with open('template.html', 'r') as template:
        template_content = template.read().format(fromName, fromEmail, toName, toEmail, toName)
        return template_content
