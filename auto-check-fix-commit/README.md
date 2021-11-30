## autoCheckFixCommit
There are many flaky tests marked as ```DeveloperFixed```. Once you find the first commit that fixed a flaky test, you can use this script to automatically run the test with the first fixed commit and the last flaky commit and output the log.

### Usage
1. Move the script ```auto_check_fix_commit.sh``` to the directory of the project where the fixed flaky test is.
2. Create a file named ```flaky_tests.csv```. The format of each line of this file is ```MODULE```,```TEST_CLASS```,```TEST_NAME```,```NONDEX_RUN_TIMES```,```FIRST_FIX_SHA```. An example is ```dropwizard-jersey,io.dropwizard.jersey.errors.LoggingExceptionMapperTest,handlesMethodNotAllowedWithHeaders,10,430c1b9f04bb3d299a059d5f9a7b849231fa603a```.
3. Run the script with ```bash auto_check_fix_commit.sh```