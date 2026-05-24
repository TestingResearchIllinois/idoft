# Overview
This automation script is designed to identify the specific commit that moved or renamed a test function or test file from the ones recorded in the IDOFT repository.

# Instructions
1. Copy and paste `find_moved_or_renamed_commit.sh` to the Repo you are working on.
2. `git checkout xxx` (replace xxx with the commit hash that the flake test was detected in IDOFT)
3. Find and copy the **Relative Path** of the given testing file, it should contain the given FUNCTION_NAME. (Paste it somewhere, this is the FILENAME that will be used later)
4. `git checkout master` (or whichever branch you want that has the latest commit)
5. Execute the script by running:

``` bash
chmod +x find_moved_or_renamed_commit.sh`
./find_moved_or_renamed_commit.sh <FUNCTION_NAME> <FILENAME> <START_COMMIT>
```

## Examples

### A Row in IDOFT
```
https://github.com/apache/ignite-3,a1aa7fd4e2398c72827777ec5417d67915ff4da3,modules/configuration,org.apache.ignite.internal.configuration.asm.ConfigurationAsmGeneratorTest.testConstructInternalConfig,ID,MovedOrRenamed,,https://github.com/apache/ignite-3/commit/b48ddcba7cd2bd3b9a053ae131c25b44a0400e27
```

### Execute
```
./find_moved_or_renamed_commit.sh testConstructInternalConfig modules/configuration/src/test/java/org/apache/ignite/internal/configuration/asm/ConfigurationAsmGeneratorTest.java a1aa7fd4e2398c72827777ec5417d67915ff4da3
```

### Output
```
commit b48ddcba7cd2bd3b9a053ae131c25b44a0400e27
Author: Aleksandr Pakhomov <apkhmv@gmail.com>
Date:   Wed Apr 26 20:02:34 2023 +0400

    IGNITE-19152 Use schema information in LocalFileConfigurationStorage (#1988)
    
    ---------
    
    Co-authored-by: Ivan Bessonov <bessonov.ip@gmail.com>

D       modules/configuration/src/test/java/org/apache/ignite/internal/configuration/asm/ConfigurationAsmGeneratorTest.java
```