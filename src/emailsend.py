import smtplib
from email.mime.text import MIMEText

"""Formats email message from readings"""
def formatString(readings):
    fullstring = ""
    for key,value in readings.items():
        fullstring = fullstring + "GPIO {}\nTemperature: {}\nHumidity: {}\nTime: {}\n\n".format(key, value['temp'], value['humid'], value['timestamp'].strftime("%Y-%m-%d %H:%M:%S"))
    return fullstring

"""Send email"""
def sendEmail(readings, emails):
    msg = MIMEText("Hello\n\nthis is automatically sent message about temperature and humidity from VU MIF supercomputer room.\n\n" + formatString(readings))
    emailTo = emails    

    msg["Subject"] = "VU MIF Supercomputer"
    msg["From"] = "termometrassuperkomp@gmail.com"
    msg["To"] = ",".join(emailTo)

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('termometrassuperkomp@gmail.com', 'kursinis')
    s.sendmail(msg["From"], emailTo, msg.as_string())
    s.close()
