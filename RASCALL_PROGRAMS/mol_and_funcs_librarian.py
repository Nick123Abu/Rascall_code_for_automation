import os
import subprocess

#Purpose: Writes on a file called func_library.txt the output of all
#functional groups given by Rascall List

#Author: Nicola Paparella

def removeDuplicates(arr, n):
    if n ==0 or n == 1:
        return n
    temp = list(range(n))
    j = 0
    for i in range(0, n-1):
        if arr[i] != arr[i+1]:
            temp[j] = arr[i]
            j += 1
     
     
    temp[j] = arr[n-1]
    j += 1
    for i in range(0, j):
        arr[i] = temp[i]
    return j



with open("functional_groups.txt") as infile:
    funcs_groups = []
    for fg in infile.readlines():
        funcs_groups.append(fg)
funcs_groups.sort()
removeDuplicates(funcs_groups, len(funcs_groups))

outfile = open("funcs_library.txt", "w")
for fg in funcs_groups:
    output = subprocess.check_output(['./rascall_list', '--fg', f"{fg[:-1]}"])

    top_and_bottom = "-----------------------------------------"
    name = fg
        
    outfile.write(top_and_bottom + " \n")
    outfile.write(" " + " \n")
    outfile.write("name: " + name + " \n")
    outfile.write(" " + " \n")
    outfile.write(output.decode() + " \n")
    outfile.write(" " + " \n")
    outfile.write(top_and_bottom + " \n")

outfile.close()
    
    
