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

1. Fork/clone this repo with the auto-check-fix-commit module containing the `git-bisect-runner.sh` and `git-bisect-script.sh` scripts.

2. Copy scripts `git-bisect-runner.sh` and `git-bisect-script.sh` to the directory of the project containing the fixed flaky test.

3. Within the project containing the DeveloperFixed test, run the script using the command below. Modify arguments to specific flaky commit, fixed commit, module path, test case of your project, mvn install options, and NonDex version. This command will also ensure standard error and output messages go to `git_bisect_output.log`, while running command in the background (since using nohup).
```shell
nohup ./git-bisect-runner.sh --flaky <FLAKY_COMMIT> --fixed <FIXED_COMMIT> --module <MODULE_PATH> --test <TEST_CASE> --nondex-version "<NONDEX VERSION>" --mvn-install "<MAVEN_OPTIONS>" &> git_bisect_output.log
```
Example:
```shell
nohup ./git-bisect-runner.sh --flaky ecf41be2ecd007853c2db19e1c6a038cf356cb9e --fixed f69557e325c5bb9e4e250bb0ec2db12d85298211 --module pinot-core --test org.apache.pinot.queries.ForwardIndexHandlerReloadQueriesTest#testSelectQueries --nondex-version "2.1.7" --mvn-install "-Dspotless.skip" &> git_bisect_output.log 
```

The output of this execution will give the commit where the flaky test was fixed. Messages within process can be found in log file within project directory.

To check for errors during process, run: `git bisect status`
To check log as process is running, run: `git bisect log`
To stop and reset bisect process, run: `git bisect reset`