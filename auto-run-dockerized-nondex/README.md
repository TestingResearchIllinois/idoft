# Dockerized Maven NonDex Runner

This module provides a **generic and standardized Docker-based NonDex execution platform**, to detect flaky tests in Maven based Java projects.

## Usage

### Step 1: Build the Docker Image
With the provided `Dockerfile` and `entrypoint.sh` files in your current directory, build the Docker image using:

```bash
docker build --build-arg JAVA_VERSION=17 -t nondex-runner .
```
### Step 2: Run the Docker Image
Run the Docker container using the following command (sample below):

```bash
docker run \
  -e REPO_URL=https://github.com/apache/myfaces-tobago.git \
  -e RUN_NONDEX_WITH_FN=true \
  -e MODULE="tobago-core" \
  -e NONDEX_RUNS=50 \
  -e TESTS="org.apache.myfaces.tobago.webapp.TobagoResponseWriterUnitTest" \
  -v $(pwd)/nondex_logs:/app/nondex_logs \
  nondex-runner

```

### Arguments

| **Environment Variable**   | **Required** | **Description**                                                                                     |
|-----------------------------|--------------|-----------------------------------------------------------------------------------------------------|
| `REPO_URL`                 | **Yes**      | URL of the GitHub repository to clone and test.                                                    |
| `RUN_NONDEX_WITH_FN`       | No           | Runs NonDex with the `--fail-never` flag if set to `true`. Default: `false`.                       |
| `MODULE`                   | No           | The specific Maven module to target (passed with `-pl`).                                           |
| `NONDEX_RUNS`              | No           | The number of NonDex runs (`-DnondexRuns=<value>`).                                                |
| `TESTS`                    | No           | Specify a particular test or suite to run using Maven’s `-Dtest` option.                           |

---

The `-v` flag in the command mounts a local directory, `<nondex_logs>`, to the container directory `app/<nondex_logs>`. This ensures that logs generated during execution are saved directly to the user's local system. You can customize this behavior by binding a different local directory to the container, based on your preference.

---

## Script Workflow

### 1. Clone the Repository
The script clones the repository provided in the `REPO_URL` argument.

### 2. Maven Clean Install
The script runs:

```bash
mvn clean install -DskipTests
```

If the MODULE argument is provided, it uses:

```bash
mvn clean install -pl <module_name> -DskipTests
```
### 3. Execute Nondex
The script executes

```bash
mvn edu.illinois:nondex-maven-plugin:2.1.7:nondex
```

With additional arguments if applicable:
- `--fail-never` if `RUN_NONDEX_WITH_FN=true`.
- `-pl <module_name>` if `MODULE` is provided.
- `-DnondexRuns=<value>` if `NONDEX_RUNS` is set 
- `-Dtest=<test_name>` if `TESTS` is specified.

### Output

- NonDex execution logs are written to the file `$(pwd)/nondex_logs/nondex-<datetime>.log`
- The **final list of flaky tests** is extracted and saved in `$(pwd)/nondex_logs/nondex-flaky-tests-<datetime>.log`

