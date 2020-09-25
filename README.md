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

## Add New Labeling Functions

- Access the file labelFunctionExecutor.py
- Implement / Import your labeling function
- Add your function and corresponding alias to LABELING_FUNCTION_SET

```
LABELING_FUNCTION_SET = {"alias": your_new_function}
```

## Release Note Sept.4 2020
### Feature:
* Labeling Function Real Time Debug
* Labeling Function Hot Append
* MD5 Color Generation, Stable color for each added labeing function
