# Overview
This script helps identify if specific test files in a Git repository have been moved or renamed in their commit history. Currently, it only supports detecting whether a test class has been moved to a different location in previous commits.

# Usage Instructions

1. Use a tool like "auto-filter-tests-by-letter" or other methods to identify the test classes you want to verify.

2. Create a text file named `test.txt` and list all the test  you want to check within a specific repository.

3. Copy `test.txt` and the script (`check_moved_or_rename.sh`) to the root directory of the repository you want to check.

4. Execute the script by running:
     ```bash
     chmod +x check_moved_or_rename.sh
     ./check_moved_or_rename.sh
     ```
   The output will be written to a new text file named `output.txt` in the same folder.

# Example Input and Output

### Example Input (`test.txt`)
```
https://github.com/apache/dubbo,737f7a7ea67832d7f17517326fb2491d0a086dd7,dubbo-filter/dubbo-filter-cache,org.apache.dubbo.cache.support.jcache.JCacheFactoryTest.testJCacheGetExpired,OD-Vic,,,
https://github.com/apache/dubbo,5349c13a36d277a090e1dc68fbe7c3b46d78fc90,dubbo-common,org.apache.dubbo.common.beanutil.JavaBeanSerializeUtilTest.testDeserializeBean,OD-Vic,,,
```

### Example Output (`output.txt`)
```
Processing line: https://github.com/apache/dubbo,737f7a7ea67832d7f17517326fb2491d0a086dd7,dubbo-filter/dubbo-filter-cache,org.apache.dubbo.cache.support.jcache.JCacheFactoryTest.testJCacheGetExpired,OD-Vic,,,
File 'dubbo-filter/dubbo-filter-cache/src/test/java/org/apache/dubbo/cache/support/jcache/JCacheFactoryTest.java' was moved or renamed in commit acee3e2f03227894b5aa4d852de1a6a4bcfab60e:
From: dubbo-filter/dubbo-filter-cache/src/test/java/org/apache/dubbo/cache/support/jcache/JCacheFactoryTest.java
To: dubbo-plugin/dubbo-filter-cache/src/test/java/org/apache/dubbo/cache/support/jcache/JCacheFactoryTest.java
Found move or rename for line: https://github.com/apache/dubbo,737f7a7ea67832d7f17517326fb2491d0a086dd7,dubbo-filter/dubbo-filter-cache,org.apache.dubbo.cache.support.jcache.JCacheFactoryTest.testJCacheGetExpired,OD-Vic,,,

Processing line: https://github.com/apache/dubbo,5349c13a36d277a090e1dc68fbe7c3b46d78fc90,dubbo-common,org.apache.dubbo.common.beanutil.JavaBeanSerializeUtilTest.testDeserializeBean,OD-Vic,,,
No move or rename found for line: https://github.com/apache/dubbo,5349c13a36d277a090e1dc68fbe7c3b46d78fc90,dubbo-common,org.apache.dubbo.common.beanutil.JavaBeanSerializeUtilTest.testDeserializeBean,OD-Vic,,,
```

### Explanation

- **Moved File**:
  - For the first record, the script found that `JCacheFactoryTest.java` was moved from `dubbo-filter/dubbo-filter-cache` to a different directory (`dubbo-plugin/dubbo-filter-cache`) at commit `acee3e2f03227894b5aa4d852de1a6a4bcfab60e`.

- **Unchanged File**:
  - For records where the test class was not moved or renamed, the script outputs a message indicating that no changes were found for that specific line:
    ```
    No moved or rename found for line: <input_line>
    ```