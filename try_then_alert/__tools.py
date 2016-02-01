import cgitb
import sys
import functools
from __alert import send_alert

def try_then_alert(function=None, 
                   alert_on_error=True, 
                   alert_on_completion=False,
                   error_subject='An Error Occurred',
                   completion_subject='Run Successful',
                   alert_recipients=None):
    """try_then_alert is a decorator:

    @try_then_alert
    def some_func():
        # do stuff

    some_func()

    If the subject function throws an error then an email 
    is sent to the email addresses in alert_recipients from your gmail account.

    On first use you will be prompted for your gmail credentials and they are 
    stored in the keyring.

    function : function
        subject function for decorator
    alert_on_error : booleon (default True)
        If true an email is sent if an error occurrs in function
    alert_on_completion : booleon (default False) 
        If true an email is sent if function runs with no errors
    error_subject : str (default 'An Error Occurred')
        error message email subject
    completion_subject : str (default 'Run Successful')
        completion message email subject
    alert_recipients : list or str (default to your gmail address)
        a single e-mail address or a list of e-mail addresses. If not specified
        emails will be sent from and to the same gmail account

    """
    if function is None:
        return functools.partial(try_then_alert,
                                 alert_on_error=alert_on_error,
                                 alert_on_completion=alert_on_completion,
                                 error_subject=error_subject,
                                 completion_subject=completion_subject,
                                 alert_recipients=alert_recipients)

    @functools.wraps(function)
    def wrap(*args, **kwargs):
        try:
            f = function(*args, **kwargs)
        except Exception as e:

            if alert_on_error:
                # if an error occurred send an error message
                send_alert(html=cgitb.html(sys.exc_info()),
                           text=cgitb.text(sys.exc_info()),
                           subject=error_subject,
                           alert_recipients=alert_recipients)

            # using exc_info captures traceback as well as error message
            exc_info = sys.exc_info()
            raise exc_info[1], None, exc_info[2]
        else:
            if alert_on_completion:                
                # if there are no errors send a run successful message
                send_alert(html='',
                           text='',
                           subject=completion_subject,
                           alert_recipients=alert_recipients)

        return f

    return wrap