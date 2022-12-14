## checkCommitForDeletion

If you find a commit that has `Deleted` a flaky test, you can use this script to verify your findings.

### Usage

1. Some filters need to be specified to `filter-tests.sh` in order for it to filter the contents of `pr-data.csv`. 

2. The script is run like this: `./filter-tests.sh arg1 arg2 arg3 .... argN`. Example usage: `./filter-tests.sh Deleted RocksDbPartition`. In this command, the script will output a file that is `Deleted` and contains `RocksDbPartition` in its test name. `filtered_tests.txt` is generated as an output which contains the test name and the commit link.

3. Any number of arguments can be provided to this script. They need to be space separated.

4. Copy the script `check-deletion.sh` and `filtered_tests.txt` to the directory of the project.

5. Run the script with `./check-deletion.sh`.

The output of this execution will show whether a test method or class has been deleted in that commit.
It will also be stored in a file `check-deletion-output.txt` in the directory where you run the script.