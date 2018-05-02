#Author: Larbi Bedrani
#Date: 01 May 2018
#Version: 0.9

#This script allows to merge tables with common and non common columns. Each of the tables has different set of row names.
#The script returns a table with all row names and all columns. In case one row name doesn't have a value in a column, a NA is inserted

########################################################################################
#Get All unique labels from the n tables to be merged
########################################################################################
get_labels <- function(tables, labels_column){
  labels <- c()
  d = lapply(tables, function(x, y){
    labels <<- c(labels, as.character(unlist(x[labels_column])))
    return()
  }, labels_column)
  
  labels = data.frame(unique(labels), stringsAsFactors = F)
  names(labels) = labels_column
  return(labels)
}

########################################################################################
#Get All columns in the tables
########################################################################################
get_columns<- function(tables, labels_column){
  columns <- c()
  d = lapply(tables, function(x, y){
    columns <<- c(columns, colnames(x))
    return()
  })
  #Remove the label column from the columns list
  columns = columns[!columns%in%labels_column]
  return(unique(columns))
}

########################################################################################
#Merging a list of tables
########################################################################################
merge_list_tables = function(tables, labels_column){
  #Getting all the labels from the tables
  final_table <- get_labels(tables, labels_column)
  #Getting the list of all columns in the tables
  columns <- get_columns(tables, labels_column)
  #Loop through the column
  for(i in 1:length(columns)){
    tab_intermed = matrix(ncol=2, nrow=0)
    colnames(tab_intermed) = c(labels_column, columns[i])
    #Check if the column is present in all or few of the tables
    for (j in 1:length(tables)){
      if(columns[i]%in%colnames(tables[[j]])){
        tab_intermed = rbind(tab_intermed, tables[[j]][c(labels_column, columns[i])])
      }
    }
    if(nrow(final_table) == nrow(tab_intermed)){
      #If the column is present in all table, the number of labels is equal to the nember of values
      final_table = merge(final_table, tab_intermed, by.x=labels_column, by.y=labels_column)
    }else{
      #Getting the common samples
      common_labels =  merge(final_table, tab_intermed, by.x=labels_column, by.y=labels_column)
      #Getting the samples that are not common 
      not_common_labels = as.matrix(final_table[!final_table[,labels_column]%in%common_labels[,labels_column],])
      #Adding an NA column to be able to cbind the common labels table with the non common
      not_common_labels = as.matrix(cbind(not_common_labels, rep(NA, nrow(not_common_labels))))
      colnames(not_common_labels) = colnames(common_labels)
      #cbind the two tables
      final_table = rbind(common_labels, not_common_labels)
    }
  }
  return(final_table)
}


#Generating testing data
labels = paste0("sample_", 1:1000)
df1 = data.frame("Samples" = sample(labels, 600, replace=F), "Blood_pressure"= rnorm(600, 12,3), stringsAsFactors = F)
labels = paste0("sample_", 1001:1500)
df2 = data.frame("Samples" = sample(labels, 400, replace=F), "Cholesterol"= rnorm(400, 12,3),
                 "Blood_pressure"= rnorm(400, 12,3), "Height"= rnorm(400, 180,20),stringsAsFactors = F)
labels = paste0("sample_", 1501:2200)
df3 = data.frame("Samples" = sample(labels,500, replace=F), "Weight"= rnorm(500, 80,20), stringsAsFactors = F)
labels = paste0("sample_", 2201:2800)
df4 = data.frame("Samples" = sample(labels,500, replace=F), "Weight"= rnorm(500, 80,20),"Height"= rnorm(500, 180,20),
                 stringsAsFactors = F)



#Merge the tables
final_table = merge_list_tables(tables=list(df1, df2, df3, df4), labels_column="Samples")


