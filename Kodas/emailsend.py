import smtplib
from email.mime.text import MIMEText

"""Formats email message from readings"""
def formatString(readings):
    fullstring = ""
    for key,value in readings.items():
        fullstring = fullstring + "GPIO {}\nTime: {}\nTemperature: {}\nHumidity: {}\n\n".format(key, value['timestamp'].strftime("%Y-%m-%d %H:%M:%S"), value['temp'], value['humid'])
    return fullstring

"""Send email"""
def sendEmail(readings):
    msg = MIMEText("Hello\n\nthis is automatically sent message about temperature and humidity from VU MIF supercomputer room.\n\n" + formatString(readings))
    emailTo = ["temisoklis@gmail.com"]    

    msg["Subject"] = "VU MIF Supercomputer"
    msg["From"] = "martynastest1@gmail.com"
    msg["To"] = ",".join(emailTo)

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('martynastest1@gmail.com', 'martynas')
    s.sendmail(msg["From"], emailTo, msg.as_string())
    s.close()
    print ("done")
