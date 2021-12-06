import pandas as pd
import subprocess
from glob import glob
import os
import shutil
from tqdm import tqdm
import json

archieved = [
	"https://github.com/gooddata/GoodData-CL",
]

df = pd.read_csv("../pr-data.csv")
error_log = []
test_file_deleted = []
test_method_deleted = []
df_copy = df.copy()
base_dir = os.getcwd()

df = df.groupby("Project URL").agg(lambda x: list(x))

for url, row in tqdm(df.iterrows(), total=df.shape[0]):
	if url in archieved:
		continue
	testname_list, status_list = row["Fully-Qualified Test Name (packageName.ClassName.methodName)"], row["Status"]
	print("url", url)

	clone_cmd = "git clone --quiet {} tmp && cd tmp".format(url)
	process = subprocess.run(clone_cmd, shell=True, stdout=open(os.devnull, 'wb'))
	print("clone done!!!")
	for full_testname, status in zip(testname_list, status_list):
		testfile_name, test_method_name = full_testname.split(".")[-2], full_testname.split(".")[-1]
		
		if status == "RepoArchived" or status == "Deleted":
			continue
		else:
			
			if "[" in test_method_name or "\"" in test_method_name:
				print("{}, {} is a PUT; skip".format(url, full_testname))
				continue
			if testfile_name[-4:] != "Test":
				error_log.append("{}, {}".format(url, full_testname))
				continue
				
			fnames = glob("**/{}.java".format(testfile_name), recursive=True)
			if len(fnames) == 0:
				# test file not found; add to log
				test_file_deleted.append("{}, {}".format(url, full_testname))
				print("[INFO]: detected deleted Test File: ", "{}, {}".format(url, full_testname))
			else:
				if len(fnames) > 1:
					print("{}, {} has multiple files with same test file name!".format(url, full_testname))
				for fname in fnames:
					with open(fname) as f:
						found = False
						for line in f.readlines():
							# make sure it's a method
							if test_method_name + "(" in line: 
								found = True
								break

						if not found:
							print("[INFO]: detected deleted Test Method: ", "{}, {}".format(url, full_testname))
							test_method_deleted.append("{}, {}".format(url, full_testname))
							df_copy.loc[df_copy["Fully-Qualified Test Name (packageName.ClassName.methodName)"] == full_testname, "Status"] = "Deleted"
							# find the commit that delete the test using git-pickaxe
							# @TODO here

	# clean the repo and repeat
	os.chdir(base_dir)
	shutil.rmtree("tmp")

# save the record
df_copy.to_csv("new_pr_data.csv")
with open("error_log.json", "w") as f:
	json.dump(error_log, f)

with open("test_file_deleted.json", "w") as f:
	json.dump(test_file_deleted, f)

with open("test_method_deleted.json", "w") as f:
	json.dump(test_method_deleted, f)





