# Datathon-SCOR
Web app and data treatment for datathon organized by SCOR

### How to use the script get_data.py to get all the data from NHANES website
It's necessary to have the following python libraries installed on your machine: os, re and BeautifulSoup. If you don't have some of them you can install it through pip.
Then just run it as a common python program:
```
python3 get_data.py
```
It will automatically create adequate folders and install the corresponding files in each folder.

### How to merge the data using the R scripts which are inside the "Merging" folder
You need to create a "Member Data" inside the "Merging folder" with the NHANES data you want to use for your analyses. The format of the files and folders inside it are given as example for a particular subset of NHANES dataset.
The installation of the needed libraries are commented in the code. If you don't have some of them installed on your machine, just uncomment the corresponding part.
Firstly, run the script 1_Mortality_Data.R:
```
Rscript 1_Mortality_Data.R
```
This script will merge the mortality data from NCHS website.
Then, run the script 2_2_Member_Data.R:
```
Rscript 2_2_Member_Data.R
```
This script will download the description files from NHANES website, use them to code the variables located in "Member Data" folder and merge them. The "download" part is commented. If you are running the script for the first time, uncomment the lines which refer to downloads.
Finally, run the script 3_Merge_Member_Mortality.R:
```
3_Merge_Member_Mortality.R
```
This script will merge the NHANES data and the mortality data.
At each part, a .csv file is generated with the corresponding merged dataset. 
