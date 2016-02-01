import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getuser
import keyring

def get_gmail_credentials():
    """Stores gmail email address and password in the keyring
    Returns
    -------
    credentials : dict
        contains 'email' and 'password'
    """

    # get system username 
    system_username = getuser()
    gmail = keyring.get_password(service_name='gmail_address', 
                                 username=system_username)
    
    # store gmail address in keyring using system username as key
    if not gmail:
        confirm = None
        gmail = raw_input("Please enter your gmail address: ")            
        while confirm != '':
            confirm = raw_input('You entered: {}. If this is correct, hit enter.'
                               ' Or you can re-enter: '.format(gmail))            
            if confirm != '':
                gmail = confirm

        keyring.set_password(service_name='gmail_address',
                                     username=system_username,
                                     password=gmail)
        
    # search for gmail password - create password if not yet stored
    password = keyring.get_password(service_name='gmail_password', username=gmail)
    if not password:
        confirm = None
        password = raw_input("Please enter your gmail password: ")            
        while confirm != '':
            confirm = raw_input('You entered: {}. If this is correct, hit enter.'
                               'or you can re-enter: '.format(password))            
            if confirm != '':
                password = confirm

        keyring.set_password(service_name='gmail_password',
                                     username=gmail,
                                     password=password)
        print 'credentials were successfully stored in keyring'

    credentials = {'email': gmail,
                   'password': password}

    return credentials


def send_gmail(me, you, password, html, text, subject):
    """send_email will send an email from the e-mail address 'me', to 'you'. 
    The email message sent is stored in 'html'.
     
    Parameters
    ----------
    me : str 
        the gmail address that mail will be sent from
    you : str
        the recipients email address
    password : str
        the gmail user's password
    html : str
        the html e-mail message to be sent
    text : str
        the text alternative if recipient cannot receive html
    subject : str
        subject line of email
    """
    # me == my email address
    # you == recipient's email address
    
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you
    
    # Create the body of the message (a plain-text and an HTML version).

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(me, password)
    
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    server.sendmail(me, you, msg.as_string())
    server.quit()


def send_alert(html, text, subject, alert_recipients):
    """Send alert meesage. If there is an error in sending the message it is
    printed to the screen but it will not hault the original function call
    """
    try:
        credentials = get_gmail_credentials()
        if not alert_recipients:
            alert_recipients = [credentials['email']]

        if isinstance(alert_recipients, str):
            alert_recipients = [alert_recipients]

        for you in alert_recipients:
            send_gmail(me=credentials['email'],
                       you=you,
                       password=credentials['password'],
                       html=html,
                       text=text,
                       subject=subject)

    except Exception as email_e:
        # If the alert message fails, throw the original error and
        # just print the send error to the user
        print '--------------------'
        print '   Alert not sent   '
        print '--------------------'
        print 'Email send error:'
        print email_e.message
        print '--------------------'
        print '--------------------'

