# dlwlrat servlet #

This is a full-fledged dlwlrat CGI servlet to deploy dlwlrat on Tomcat. While this
is a bit of an exotic usecase, it is an existing one and this README along
with the XML provided should keep you from crying your eyes out while solving
this exercise.

# Building #

First, some words on how this works. You will attempt to create a WAR (Web
application ARchive) containing a working dlwlrat installation. This means you
will first have to install dlwlrat as usual and deploy your data. Create the dlwlrat
folder structure as shown (`dlwlrat/WEB-INF`, `dlwlrat/META-INF`) with the given
`web.xml` and `context.xml`. Copy your previously installed dlwlrat installation
to `dlwlrat/`, then, proving that you don't need ant to build something Java-ish,
simply go to the parent folder of `dlwlrat`, where the `GNUmakefile` is, and run:

    make

This will produce an archive `dlwlrat.war` that you can deploy on Tomcat.

# Installation #

Drop the `dlwlrat.war` into the Tomcat `webapps` directory and you should be able
to access your installation using:

    http://${HOSTNAME}:${PORT}/dlwlrat/

From now on, dlwlrat should work as usual with the exception that it is Tomcat
serving your requests.
