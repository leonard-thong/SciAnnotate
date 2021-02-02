# SciAnnotate servlet #

This is a full-fledged SciAnnotate CGI servlet to deploy SciAnnotate on Tomcat. While this
is a bit of an exotic usecase, it is an existing one and this README along
with the XML provided should keep you from crying your eyes out while solving
this exercise.

# Building #

First, some words on how this works. You will attempt to create a WAR (Web
application ARchive) containing a working SciAnnotate installation. This means you
will first have to install SciAnnotate as usual and deploy your data. Create the SciAnnotate
folder structure as shown (`SciAnnotate/WEB-INF`, `SciAnnotate/META-INF`) with the given
`web.xml` and `context.xml`. Copy your previously installed SciAnnotate installation
to `SciAnnotate/`, then, proving that you don't need ant to build something Java-ish,
simply go to the parent folder of `SciAnnotate`, where the `GNUmakefile` is, and run:

    make

This will produce an archive `SciAnnotate.war` that you can deploy on Tomcat.

# Installation #

Drop the `SciAnnotate.war` into the Tomcat `webapps` directory and you should be able
to access your installation using:

    http://${HOSTNAME}:${PORT}/SciAnnotate/

From now on, SciAnnotate should work as usual with the exception that it is Tomcat
serving your requests.
