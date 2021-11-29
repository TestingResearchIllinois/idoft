# `runNondex`

This script runs individual modules in the specified project with the `Nondex` tool and shows results automatically in the `markdown` format.

Output file is located inside the project folder and called `report_md.md` The output would only contain tests that are detected by the nondex tool as flaky, and the result includes the seeds used for the test and the status of the test result.

### Usage:
```bash
./runNondex <project_folder_path>
```