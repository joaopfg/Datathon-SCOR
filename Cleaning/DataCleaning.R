##########################################################################
# Clean data
##########################################################################

# count columns
EXAM_2013_2014 <- read.csv("EXAM_2013_2014.csv")
ncol(EXAM_2013_2014)

# delete all the columns which has only 1 variable
valid1 <- EXAM_2013_2014[ apply(EXAM_2013_2014, 2, function(x) length(unique(x))) > 1]
ncol(valid1)

# create a table which has less than 60 % of n/a
valid2 <- valid1[ lapply(valid1, function(x) sum(is.na(x)) / length(x) ) < 0.6 ]
valid2
ncol(valid2)

# extract all the numerical values
numerical <- valid2[,sapply(valid2, is.numeric)]

# extract all the string columns
strings1 <- valid2[,sapply(valid2,is.factor)]
ncol(strings1)

# count number of unique variables by each columns
# this is because if there are too many variables, it is less likely correlated
apply(strings1, 2, function(x) length(unique(x)))

# select only the colums which contain less than 90% unique data
string2 <- strings1[ lapply(strings1, function(x) length(unique(x)) / length(x) ) < 0.9 ]
string2

# concatenate numerical and cleaned string value
cleaned <- cbind(numerical, string2)
View(cleaned)


##########################################################################
# impute missing data
##########################################################################

library(missMDA)

# estimate the optimal number of dimensions for the Principal Component Analysis by cross-validation
# this is to avoid overfitting
nb <- estim_ncpPCA(cleaned, scale = TRUE)
nb

comp <- imputePCA(cleaned, ncp = , scale = TRUE)

res.pca <- PCA(comp)


