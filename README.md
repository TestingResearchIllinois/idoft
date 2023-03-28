# My Flaky Test data

Following challenge at https://mir.cs.illinois.edu/marinov/eval.html#Reading


- **Project** URL for repo on GitHub
- **SHA** Detected for the commit where we found the flaky test (which is most likely not the latest commit in this repo)
- **Module** Path for the so-called Maven module ("subproject") where this test is
- **Fully-Qualified Test Name** in the from packageName.ClassName.methodName
- **Category** for the kind of test (we'll focus here on "ID" tests)
- **Status** for the status: detected (found but not fixed), accepted (fixed and PR accepted), rejected (fixed but PR rejected), ...
- **PR** Link for the pull request (PR) on GitHub that proposed a fix for this test
- **Notes** for optional additional information 

```
user@bserver:~/Projects/idoft$ grep ,ID,, pr-data.csv | grep -v "\\[" | shuf --random-source=<(while :; do echo faustino.aguilar@up.ac.pa; done) | head
```

|Project|SHA|Module|Fully-Qualified Test Name|Category|Status|PR|Notes|
|---|---|---|---|---|---|---|---|
|https://github.com/apache/pinot|ecf41be2ecd007853c2db19e1c6a038cf356cb9e|pinot-core|org.apache.pinot.queries.ExplainPlanQueriesTest.testSelectAggregate|ID||||
|https://github.com/apache/pinot|ecf41be2ecd007853c2db19e1c6a038cf356cb9e|pinot-core|org.apache.pinot.queries.NullEnabledQueriesTest.testQueriesWithDictFloatColumn|ID||||
|https://github.com/apache/openwebbeans|424af4bb7285b806d3e3efe5020cd3e440e0a4ff|webbeans-tck-jakart|org.jboss.cdi.tck.tests.extensions.configurators.observerMethod.ObserverMethodConfiguratorTest.notifyAcceptingConsumerNotified|ID||||
|https://github.com/GoogleCloudPlatform/DataflowTemplates|5094c7b39de511c9ed441d9fde28553a88f68e4b|.|com.google.cloud.teleport.templates.common.DatastoreConvertersTest.testCheckNoKeyBothCorrectAndInvalid|ID||||
|https://github.com/apache/pinot|ecf41be2ecd007853c2db19e1c6a038cf356cb9e|pinot-core|org.apache.pinot.queries.ExplainPlanQueriesTest.testSelectColumnsUsingFilterOnInvertedIndexColumn|ID||||
|https://github.com/raphw/byte-buddy|b19eabacf6a9df26641052037666566b2152ce9f|byte-buddy-dep|net.bytebuddy.description.method.MethodDescriptionLatentTest.testToString|ID||||
|https://github.com/apache/nifi|2bd752d868a8f3e36113b078bb576cf054e945e8|nifi-nar-bundles/nifi-ldap-iaa-providers-bundle/nifi-ldap-iaa-providers|org.apache.nifi.ldap.tenants.LdapUserGroupProviderTest.testSearchUsersAndGroupsMembershipThroughUsersCaseInsensitive|ID||||
|https://github.com/GoogleCloudPlatform/DataflowTemplates|5094c7b39de511c9ed441d9fde28553a88f68e4b|.|com.google.cloud.teleport.bigtable.CassandraRowMapperFnTest.testSmallIntColumn|ID||||
|https://github.com/alibaba/wasp|b2593d8e4b31ca6da0cd2f3e18356338d9b6dace|.|com.alibaba.wasp.master.TestRestartCluster.testClusterRestart|ID||||
|https://github.com/sofastack/sofa-boot|451b5c513ceb13317ea7b53c656dde2a597867df|sofa-boot-project/sofa-boot-starters/log-sofa-boot-starter|com.alipay.sofa.common.boot.logging.test.LogConfigTest.testLogConfig|ID||||