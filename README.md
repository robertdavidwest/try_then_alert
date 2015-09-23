## Try then alert

* Send your self an alert if your function call or crashes or finishes successfully 
* Currently setup for gmail accounts only

## Dependencies 

* Install packages `email`, `smtblib`, `keyring`, `getpass using:

		$ pip install <package_name>
				
## Installation

* Clone the repository

		$ git clone https://github.com/robertdavidwest/try_then_alert.git
* `cd` into `try_then_alert`
* Install the package
  
        $ python setup.py install
* Now you can `import try_then_alert` from anywhere on your machine
* You may also have to do this: Log into your gmail account in your browser and navigate to [https://www.google.com/settings/security/lesssecureapps](https://www.google.com/settings/security/lesssecureapps) and select **'Turn on'**


## First time use

`try_then_alert` will store your gmail credentials in the keyring so you can easily use in your code without having to hard code your gmail address and password. When used for the first time your we be prompted for these credentials. Afterwhich they will be stored in the keyring.

## Usage
This is designed to be used when you're running something that takes forever. You want to walk away from your computer and not think about it until it has finished running or if there has been an error. 

It's really to use. Just apply the wrapper to any function. Then when the function is called you will be alerted by email if there is an error in the execution, or, if the function call is successful depending on your preferences

		from try_then_alert import try_then_alert
	
		@try_then_alert
		def some_func():
			# do some important and time consuming stuff 
			
		if __name__ == '__main__':
			some_func()
			
## Features to be added

* Right now the default setting is that you will be emailed if the program has an error OR if it finishes succesfully. I want to add optional parameters, so this can be for only one or the other. 
* Also want to add optional parameters to add the email subject and message 
* Possibly add other alert methods - instant messenger for example