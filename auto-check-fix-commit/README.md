## autoCheckFixCommit
There are many flaky tests marked as ```DeveloperFixed```. Once you find the first commit that fixed a flaky test, you can use this script to automatically run the test with the first fixed commit and the last flaky commit and output the log.

### Usage
1. Move the script ```auto_check_fix_commit.sh``` to the directory of the project where the fixed flaky test is.
2. Create a file named ```flaky_tests.csv```. The format of each line of this file is ```MODULE```,```TEST_CLASS```,```TEST_NAME```,```NONDEX_RUN_TIMES```,```FIRST_FIX_SHA```. An example is ```dropwizard-jersey,io.dropwizard.jersey.errors.LoggingExceptionMapperTest,handlesMethodNotAllowedWithHeaders,10,430c1b9f04bb3d299a059d5f9a7b849231fa603a```.
3. Run the script with ```bash auto_check_fix_commit.sh```


## Find the commit which fixed the flaky test using Git Bisect

Git Bisect command uses a binary search algorithm to find which commit in your project’s history introduced a bug. You use it by first telling it a "bad" commit that is known to contain the bug, and a "good" commit that is known to be before the bug was introduced.

The git-bisect-script-alluxio.sh script handles the case where the flaky test is fixed in the latest commit.

Reference - https://git-scm.com/docs/git-bisect/

### Usage

1. Copy scripts `git-bisect-runner.sh` and `git-bisect-script.sh` to the directory of the project containing the fixed flaky test.


2. Run the script using the below command
```shell
./git-bisect-runner.sh --flaky e6d76803f27133d7700811585f5310470e50e487 --fixed 5828d56a824748e7c91076842fad75efb42f92f9 --module core/server/worker --test alluxio.worker.block.BlockLockManagerTest#lockAlreadyReadLockedBlock
```

The output of this execution will give the commit where the flaky test was fixed.