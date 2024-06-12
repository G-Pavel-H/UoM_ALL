set STENDHAL_VERSION=1.41
set LOCALCLASSPATH=.;data\script;data\conf;build\lib\stendhal-server-%STENDHAL_VERSION%.jar;libs\*
java -Xmx400m -cp "%LOCALCLASSPATH%" games.stendhal.server.StendhalServer -c server.ini -l
@pause