# dlmat servlet #

This is a full-fledged dlmat CGI servlet to deploy dlmat on Tomcat. While this
is a bit of an exotic usecase, it is an existing one and this README along
with the XML provided should keep you from crying your eyes out while solving
this exercise.

# Building #

First, some words on how this works. You will attempt to create a WAR (Web
application ARchive) containing a working dlmat installation. This means you
will first have to install dlmat as usual and deploy your data. Create the dlmat
folder structure as shown (`dlmat/WEB-INF`, `dlmat/META-INF`) with the given
`web.xml` and `context.xml`. Copy your previously installed dlmat installation
to `dlmat/`, then, proving that you don't need ant to build something Java-ish,
simply go to the parent folder of `dlmat`, where the `GNUmakefile` is, and run:

    make

This will produce an archive `dlmat.war` that you can deploy on Tomcat.

# Installation #

Drop the `dlmat.war` into the Tomcat `webapps` directory and you should be able
to access your installation using:

    http://${HOSTNAME}:${PORT}/dlmat/

From now on, dlmat should work as usual with the exception that it is Tomcat
serving your requests.
