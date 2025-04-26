### Issue Title:
https://github.com/authorjapps/zerocode,cf84ccd70e6f70a2cfbac4e9242db911ba841859,org.jsmart.zerocode.core.kafka.DeliveryDetailsTest.testSerDeser

### Issue Description:

#### **Flaky Test Information**
- **Project URL**: [https://github.com/authorjapps/zerocode](https://github.com/authorjapps/zerocode)
- **SHA Detected**: `cf84ccd70e6f70a2cfbac4e9242db911ba841859`
- **Fully-Qualified Test Name**: `org.jsmart.zerocode.core.kafka.DeliveryDetailsTest.testSerDeser`

#### **Steps to Reproduce**
1. Clone the repository:
   ```bash
   git clone https://github.com/authorjapps/zerocode.git
   cd zerocode
   ```
2. Checkout the flaky commit:
   ```bash
   git checkout cf84ccd70e6f70a2cfbac4e9242db911ba841859
   ```
3. Build the project:
   ```bash
   mvn clean install -DskipTests
   ```
4. Run the test with NonDex:
   ```bash
   mvn edu.illinois:nondex-maven-plugin:2.1.1:nondex \
       -pl core \
       -Dtest=org.jsmart.zerocode.core.kafka.DeliveryDetailsTest#testSerDeser
   ```

#### **Expected Behavior**
- The test should pass consistently regardless of the field order in the JSON.

#### **Actual Behavior**
- The test fails intermittently due to field order changes in the serialized JSON.

#### **Relevant Logs**
Attach the following files:
1. **NonDex Log Output**:
   - `nondexMode` and `nondexSeed` from `.nondex/{testid}/config`.
   - Example:
     ```
     nondexMode: FULL
     nondexSeed: 12345678
     ```
2. **Relevant Files**:
   - Attach `flaky-list.txt` and `original-order.txt` from `.dtfixingtools` if detected by iDFlakies.

#### **Proposed Fix**
1. Use `JSONAssert` with `LENIENT` mode for JSON validation.
2. Configure `Gson` for deterministic field order serialization.

---

### **Step 2: Add Entry to `pr-data.csv`**
Add the following entry to the `pr-data.csv` file to document the flaky test and PR:

````csv name=pr-data.csv
Project URL,SHA Detected,Module Path,Fully-Qualified Test Name (packageName.ClassName.methodName),Category,Status,PR Link,Notes
https://github.com/authorjapps/zerocode,cf84ccd70e6f70a2cfbac4e9242db911ba841859,core/org.jsmart.zerocode.core.kafka,org.jsmart.zerocode.core.kafka.DeliveryDetailsTest.testSerDeser,ID,Open,https://github.com/TestingResearchIllinois/flaky-test-dataset/issues/<ISSUE_NUMBER>,Test became flaky due to non-deterministic field order in JSON serialization using Gson