# Not an ant file for producing a dlmat servlet WAR.
# 
# Author:	Pontus Stenetorp	<pontus stenetorp se>
# Version:	2012-07-29

dlmat_WAR=dlmat.war
SERVLET_DIR=dlmat
META_DIR=${SERVLET_DIR}/META-INF
WEB_DIR=${SERVLET_DIR}/WEB-INF

${dlmat_WAR}: ${META_DIR}/context.xml ${WEB_DIR}/web.xml ${shell find ${SERVLET_DIR}}
	jar -cf ${dlmat_WAR} -C ${SERVLET_DIR} .

.PHONY: clean
clean:
	rm -f ${dlmat_WAR}
