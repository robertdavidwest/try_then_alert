import smtplib
import functools
from alert import get_gmail_credentials, send_gmail


def try_then_alert(function=None, subject='An Error Occured'):
    if function is None:
        return functools.partial(try_then_alert, subject=subject)
    @functools.wraps(function)
    def wrap(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            html = e.message
            credentials = get_gmail_credentials()
            try:
                send_gmail(me=credentials['email'],
                           you=credentials['email'],
                           password=credentials['password'],
                           html=html,
                           subject=subject)

            except Exception as email_e:
                print '--------------------'
                print 'Error Alert not sent'
                print '--------------------'
                print 'Email send error msg:'
                print email_e.message
                print email_e.strerror
                print '--------------------'
                print '--------------------'
            raise e
    return wrap
