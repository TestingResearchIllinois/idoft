# Find Which Commit a Test Was Deleted
`find_deletion_commit.py` clones the given repository, checks the file history, outputs the commit the test was deleted.
(Tested only for python, could work for Java) 

# To Run
```bash
python find_deleted_test_function.py <repository_url_or_path> <file_path> <test_function_name>
```
## Example:
```bash
python find_deletion_commit.py https://github.com/solegalli/feature_engine tests/test_missing_data_imputer.py test_ArbitraryNumberImputer
```
