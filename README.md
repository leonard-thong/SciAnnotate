# Brat Rapid Annotation Tool (brat) #

## Quick start installation: standalone server ##

First, please note the following:

- The brat standalone server only is available in brat v1.3 and above.
- The standalone server is experimental and should not be used for sensitive data or systems accessible from the internet.


Run the installation script in “unprivileged” mode

    ./install.sh -u

Start the standalone server

    python standalone.py


You should then be able to access the brat server from the address printed out by standalone.py.
