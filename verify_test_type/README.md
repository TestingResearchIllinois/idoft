# Verify Test Type

Script Purpose: Ensure the identification of the test type (e.g., ID, OD, NOD, etc.) for new tests discovered in a repository.

## Steps to Run the Script locally

#### 1. Go to the root directory

Go to the root directory of the repository which has the newly found flaky test.

#### 2. Download the script in your repository

Download or clone the scipt in the root of your repository. Here is the script file:

```
https://raw.githubusercontent.com/TestingResearchIllinois/idoft/main/verify_test_type/verify_test_type.sh
```

#### 3. Run the script

Run the script for a particular test using this command:

```
./verify_test_type.sh <module-name> <commit-hashcode> <test-name> <class-name>
```

Example of an invocation:
```
./verify_test_type.sh bundles/org.openhab.core.thing 660102e3f93f928473b66f56f2955090dfa3c30e testCreateChannelDescriptionChangedEventOnlyNewValue ThingEventFactoryTest
```

Description of the script:
The repository is forcefully reset to the exact commit SHA specified by $commit_hash. This guarantees that all operations performed by the script will use this specific state of the repository. It assumes the repository is already cloned.