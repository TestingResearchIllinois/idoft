# Assume this script is run from the folder of .pom.xml files

mvn edu.illinois:nondex-maven-plugin:2.1.1:nondex -Dlicense.skip -Drat.skip --fail-at-end | tee ./nondex.log

awk '/\[INFO\] Across all seeds:/{flag=1; next} /\[INFO\] Test results can be found at:/{flag=0} flag' "./nondex.log" > "./result"