import pandas as pd
import subprocess
from glob import glob
import os
import shutil
from tqdm import tqdm
import json

archieved = [
	"https://github.com/gooddata/GoodData-CL"
]


df = pd.read_csv("../pr-data.csv")
error_log = []
test_file_deleted = []
test_method_deleted = []
base_dir = os.getcwd()

df = df.groupby("Project URL").agg(lambda x: list(x))

for url, row in tqdm(df.iterrows(), total=df.shape[0]):

	testname_list, status_list, note_list = row["Fully-Qualified Test Name (packageName.ClassName.methodName)"], row["Status"], row["Notes"]
	print("url", url)
	if url in archieved:
		print("this url has been archieved! skip")
		continue

	clone_cmd = "git clone --quiet {} tmp && cd tmp".format(url)
	subprocess.run(clone_cmd, shell=True, stdout=open(os.devnull, 'wb'))
	print("clone done!!!")
	for full_testname, status, note in zip(testname_list, status_list, note_list):
		testfile_name, test_method_name = full_testname.split(".")[-2], full_testname.split(".")[-1]
		
		if pd.isna(status) and pd.isna(note):
			
			if "[" in test_method_name or "\"" in test_method_name:
				print("{}, {} is a PUT; skip".format(url, full_testname))
				continue
			if testfile_name[-4:] != "Test":
				error_log.append("{}, {}".format(url, full_testname))
				continue
				
			fnames = glob("**/{}.java".format(testfile_name), recursive=True)
			if len(fnames) == 0:
				# try to get the commit id
				git_find_SHA = "cd tmp && git rev-list -n 1 HEAD -- **/{}.java".format(testfile_name)
				commit_SHA = subprocess.check_output(git_find_SHA, shell=True).decode("utf-8")

				if len(commit_SHA) > 0:
					test_file_deleted.append("{}, {}, {}".format(url, full_testname, url+"/commit/"+commit_SHA))
					print("[INFO]:detected Test File " + "{}, {} was deleted at SHA {}".format(url, full_testname, commit_SHA))
				# test file not found; add to log
				else:
					print("[INFO]: detected deleted Test File WITHOUT FINDING SHA: ", "{}, {}".format(url, full_testname))


	# clean the repo and repeat
	os.chdir(base_dir)
	shutil.rmtree("tmp")


with open("new_test_file_deleted.json", "w") as f:
	json.dump(test_file_deleted, f)






