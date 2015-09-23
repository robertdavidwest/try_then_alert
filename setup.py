
from distutils.core import setup
from try_then_alert import __version__

setup(
    name='try_then_alert',
    version=__version__,
    author='Robert West',
    author_email='robert.david.west@gmail.com',
    packages=['try_then_alert'],
    scripts=[],
    description='Wrapper function. When used, if an error is thrown, an alert'
                ' will be sent',
    long_description=open('README.md').read(),
    install_requires=[
        'smtplib',
        'email',
        'keyring',
        'getpass'
    ],
)
