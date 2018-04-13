#Author: Larbi Bedrani
#Version: 0.5
#Date: May 12th, 2018


#This code aims to devide a column of a dataset in n number of quantiles. n is lower than the total number of rows in the dataset.
#My challenge was to implement the code without using any library allowing to deal easily with dataframes or matrices (i.e numpy, pandas).  

import math
import random

###################################################
#Function that loads the dataset into a dictionary
###################################################

def load_dataset(file_name, sep):
	#load the data in a dictionary of lists
	dataset = {}	
	n_line = 0	
	headers=[]
	#Create the keys of the dict that correspond to the first line
	for line in open(file_name, "r"):		
		if n_line == 0:
			headers = line.strip().split(sep)
			for h in headers:
				dataset[h.strip()]=[]
			n_line +=1
		#Add the elements to the correponding key
		else:
			vals = line.strip().split(sep)
			for i in range(len(headers)):
				dataset[headers[i]].append(vals[i])
			n_line += 1
	#Keep track of the initial columns order
	dataset["Column_order"] = headers

	return(n_line - 1 , dataset)	#return the number of lines without the header


#################################################################################################################################
#Function that calculates the number of elements per quantile and returns a dictionary with the values belonging to every quantile
#################################################################################################################################
def values_in_quantile(vector, number_of_quantiles):
	#Calculate the length of every quantile
	len_quantile = math.floor(len(vector)/number_of_quantiles)
	#If the len_quantile is not a whole number, calculate the remiader and add 1 to the length of the remainder first quartile lengths
	remainder = len(vector) % number_of_quantiles
	
	#Generate a list with the length of each quantile 
	len_quantiles_list = [len_quantile for i in range(number_of_quantiles)]
	if remainder > 0:
		for i in range(int(remainder)):
			len_quantiles_list[i] = len_quantiles_list[i] + 1
	#Create a dictionary with the quantile as key and the corresponding list of values
	quantile_dict = dict(list())
	sorted_vector = sorted([float(i) for i in vector]) #convert the values to floats in case they are in str	
	for i in range(len(len_quantiles_list)):		
		for j in range(len_quantiles_list[i]):						
			if ("Q" + str(i + 1)) in quantile_dict.keys():
				quantile_dict["Q" + str(i + 1)].append(sorted_vector[j])				
			else:
				quantile_dict["Q" + str(i + 1)] = []
				quantile_dict["Q" + str(i + 1)].append(sorted_vector[j])		
		#Trim the vector for next iteration	
		sorted_vector = sorted_vector[j + 1:]
		
	return(quantile_dict)	
		
###########################################################################################################
#Function to attribute the label of the quantile it belongs to while preserving the ordering in the dataset
###########################################################################################################
def attribute_quantile(vector, number_of_quantiles):
	if number_of_quantiles > len(vector):
		return 		

	#Return a dictionary with the quantile number as a key and the values in this quantile		
	#create the keys for the quantile_dict
	quantile_dict = values_in_quantile(vector, number_of_quantiles)

	final_labels = []
	sorted_keys = sorted(quantile_dict.keys())
	for i in range(len(vector)):	
		for key in sorted_keys:				
			#If the value is higher than the max of values go to the next quantile		
			if float(vector[i]) > max(quantile_dict[key]):
				continue
			if float(vector[i]) in quantile_dict[key]:
				final_labels.append(key)
				quantile_dict[key].pop(quantile_dict[key].index(float(vector[i])))
				#Check if the value of the key is empty then remove it
				if len(quantile_dict[key]) == 0:
					del quantile_dict[key]
					sorted_keys.pop(sorted_keys.index(key))				
			
	return(final_labels)		

	

#################################################################################
#Function that reconstruct the initial dataset and append to it quantiles labels
#################################################################################
def return_final_table_in_file(dataset, quantile_labels, column_name,output_file_name, sep): 
	OUT = open(output_file_name, "w")
	#Append the name of the quantile label column to headers
	dataset["Column_order"].append("Quantile" + column_name)
	#Add the quantile labels vector to the dictionary
	dataset["Quantile" + column_name] = quantile_labels
	#Print headers into the file
	OUT.write(sep.join(dataset["Column_order"]) + "\n")
	
	#print the rest of the values
	#get the length of the values (take any of the values)
	val_len = len(dataset[dataset["Column_order"][0]])
	
	for element_number in range(val_len):
		line=[]
		#Loop through the ordered headers that are also the keys of the values correponding to every column
		for headerIndex in range(len(dataset["Column_order"])):
			line.append(dataset[dataset["Column_order"][headerIndex]][element_number])			
		#Write the line into the file
		OUT.write(sep.join(line) + "\n")
	
	OUT.close()

##############################################################################
#Final function
##############################################################################
def attribute_quantiles(file_name, column, sep, number_of_quantiles, output_file_name):
	#Load the dataset
	n_line, dataset = load_dataset(file_name, sep)	
	if number_of_quantiles > n_line:
		print('The number of quantiles cannnot be higher that the number of rows in the dataset')
		return 
	#Get the column for which the quantiles are to be determined
	col = dataset[column]
	#Get the labels vector
	quantile_labels = attribute_quantile(col, number_of_quantiles)	
	#Write the file with new dataset
	return_final_table_in_file(dataset, quantile_labels, column, output_file_name, sep)


##############################################################################
#Simple function that creates a fake dataset for testing and write it into a file
##############################################################################
def fake_dataset(number_of_lines, fileName ="test.txt", sep = ","):
	#Create a dictionary and write it into a file
	dataset = {
		"Examples":["E" + str(i) for i in range(number_of_lines)],
		"Floats" : [random.uniform(1,2) * i for i in range(number_of_lines)],
		"Integers" : sorted([int(random.uniform(1,2) * i) for i in range(number_of_lines)]) #test
		}
	
	#write the data into a file called test
	OUT = open(fileName, "w")
	OUT.write(sep.join(sorted(dataset.keys())) + "\n")
	
	for i in range(number_of_lines):
		line = [str(dataset[j][i]) for j in sorted(dataset.keys())]		
		OUT.write(sep.join(line) + "\n")

	OUT.close()

##############################################################################
#Testing of the Code
##############################################################################

#Generate the dataset in "test.txt"
fake_dataset(100)

#Get table and calculate quantiles
attribute_quantiles("test.txt", "Integers", ",", 11, "test_plus_quantiles.txt")





