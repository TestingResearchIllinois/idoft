0. We can use ``repoArchivedCheck.py`` to find archived projects in [pr-data.csv](https://github.com/TestingResearchIllinois/idoft/blob/main/pr-data.csv), [py-data.csv](https://github.com/TestingResearchIllinois/idoft/blob/main/py-data.csv), and [gr-data.csv](https://github.com/TestingResearchIllinois/idoft/blob/main/gr-data.csv).

1. Environment:  
    - python3.6  

2. Libraries:  
    - pandas
    - requests_html

3. Usage:
    - ``python3 repoArchivedCheck.py <filename.csv>``

4. The example results in console:  
    - if no update on ```status``` is needed, it'll print ```No need to update```, otherwise ```Need to Update``` with the contents which user can copy to replace the corresesponding line in ```<filename.csv>``` file;
    - ![image](https://user-images.githubusercontent.com/46290389/142753068-c5234bb5-d037-49c5-bf6a-b238f650eb3f.png)
