## autoCheckFixCommit
There are many flaky tests marked as ```DeveloperFixed```. Once you find the first commit that fixed a flaky test, you can use this script to automatically run the test with the first fixed commit and the last flaky commit and output the log.

### Usage
1. Move the script ```auto_check_fix_commit.sh``` to the directory of the project where the fixed flaky test is.
2. Create a file named ```flaky_tests.csv```. The format of each line of this file is ```MODULE```,```TEST_CLASS```,```TEST_NAME```,```NONDEX_RUN_TIMES```,```FIRST_FIX_SHA```. An example is ```dropwizard-jersey,io.dropwizard.jersey.errors.LoggingExceptionMapperTest,handlesMethodNotAllowedWithHeaders,10,430c1b9f04bb3d299a059d5f9a7b849231fa603a```.
3. Run the script with ```bash auto_check_fix_commit.sh```


## Find the commit which fixed the flaky test using Git Bisect

Git Bisect uses a binary search algorithm to find which commit fixed a flaky test. This tool uses custom terminology: "flaky" for the old broken state and "non-flaky" for the new fixed state, making the process more intuitive.

Reference - https://git-scm.com/docs/git-bisect/

### Usage

1. Fork/clone this repo with the auto-check-fix-commit module containing the `git-bisect-runner.sh` and `git-bisect-script.sh` scripts.

2. Copy scripts `git-bisect-runner.sh` and `git-bisect-script.sh` to the directory of the project containing the fixed flaky test.

3. Within the project containing the DeveloperFixed test, run the script using the command below. Modify arguments to specific flaky commit, fixed commit, module path, test case of your project, mvn install options, and NonDex version.

```shell
./git-bisect-runner.sh --flaky <FLAKY_COMMIT> --fixed <FIXED_COMMIT> --module <MODULE_PATH> --test <TEST_CASE> --nondex-version "<NONDEX_VERSION>" [--mvn-install "<MAVEN_OPTIONS>"]
```

To run in background with logging:
```shell
nohup ./git-bisect-runner.sh --flaky <FLAKY_COMMIT> --fixed <FIXED_COMMIT> --module <MODULE_PATH> --test <TEST_CASE> --nondex-version "<NONDEX_VERSION>" --mvn-install "<MAVEN_OPTIONS>" &> git_bisect_output.log &
```

Example:
```shell
./git-bisect-runner.sh \
  --flaky ecf41be2ecd007853c2db19e1c6a038cf356cb9e \
  --fixed f69557e325c5bb9e4e250bb0ec2db12d85298211 \
  --module pinot-core \
  --test org.apache.pinot.queries.ForwardIndexHandlerReloadQueriesTest#testSelectQueries \
  --nondex-version "2.1.7" \
  --mvn-install "-Dspotless.skip"
```
Or, you can manually input the default values into `git-bisect-runner.sh`
```shell
flaky_commit="ecf41be2ecd007853c2db19e1c6a038cf356cb9e"
fixed_commit="f69557e325c5bb9e4e250bb0ec2db12d85298211"
test_module="pinot-core"
test_case="org.apache.pinot.queries.ForwardIndexHandlerReloadQueriesTest#testSelectQueries"
nondex_version="2.1.7"
mvn_options="-Dspotless.skip"
``` 
### Output

The script will:
1. Display configuration settings
2. Validate all inputs and commits
3. Run the bisect process with colored status updates
4. Show the commit that fixed the flaky test
5. Display the bisect log
6. Automatically reset the bisect session

### Troubleshooting

The script includes built-in error handling, but you can also use these git commands:

- Check bisect status: `git bisect log`
- View current state: `git bisect visualize` or `git bisect view`
- Manually reset if needed: `git bisect reset`

### Exit Codes

- `0`: Test is flaky (old state)
- `1`: Test is non-flaky (new state)  
- `125`: Build failed, skip this commit (git bisect special code)