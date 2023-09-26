import subprocess
import os

#Purpose: explore RASCALL based on molecule input.
#Note: the filter is requested after the discovery of the functional groups, contrary to what happens in fg_mol_reversed.

#Author: Nicola Paparella


fg = open('funcs_test.txt')
discovered_fg = []


def fg_filter(discovered_fg):
    while True:
        order = input("What wavenumber order? high, low or average?")
        if(order == "high"):
            break
        elif(order == "low"):
            break
        elif(order == "average"):
            break
    while True:
        print("Select the range: ")
        print(" ")
        print("-------------------------------------")
        maximum = input("select maximum value of your range (in cm^-1): ")
        try:
            maxi = int(maximum)
        except ValueError:
            maxi = "err"
        if (maxi == "err"):
            print(" ")
            print("that is not a number!")
            print(" ")
        elif (maxi <= 0):
            print(" ")
            print("max is equal or inferior to zero!")
            print(" ")
        elif (maxi > 4500):
            print(" ")
            print("max is greater than 4500 cm^-1")
            print(" ")
        else:
            minimum = input("select minimum value of your range (in cm^-1):")
            try:
                mini = int(minimum)
            except ValueError:
                mini = "err"
            if(mini == "err"):
                print(" ")
                print("that is not a number!")
                print(" ")
            elif(mini <= maxi):
                break
            elif(mini >= 4500):
                print(" ")
                print("mini is greater than or equal to 4500")
                print(" ")
            else:
                print(" ")
                print("min is greater than max!")
                print(" ")
   
    passed_fg = []
    for x in discovered_fg:
        f = open("functionals.csv")
        for line in f.readlines():
            if x == line.split(",")[0]:

                if(order == "low"):

                    if (int(line.split(",")[2]) <= maxi and int(line.split(",")[2]) >=mini):
                        funct_name = line.split(",")[0] + "---" + line.split(",")[1]
                        passed_fg.append(funct_name)

            
                elif(order == "average"):

                    if( (int(line.split(",")[2]) +
                         int(line.split(",")[3]))/2<=maxi and
                        
                        
                        
                        (int(line.split(",")[2]) + int(line.split(",")[3]))/2
                        >= mini):
                        funct_name = line.split(",")[0] + "---" + line.split(",")[1]
                        passed_fg.append(funct_name)
    
                

                
                elif(order == "high"):
                    if(int(line.split(",")[3]) <= maxi and int(line.split(",")[3]) >=mini):
                       funct_name = line.split(",")[0] + "---" + line.split(",")[1]
                       passed_fg.append(funct_name)

                
        f.close()
    return passed_fg



#-----------------------------------------------------------------------

while True:
    mol = open('RASCALL_Molecule_Identifiers.csv', encoding='iso-8859-1')

    #line_counter = 0 # only for testing purposes

    
    starting_mol = input("Insert the mol with which beginning the exploration (only RASCALL column is considered, not rdkit_RASCALL) otherwise type 'filter' if functional groups were discovered: ")

    #Task: triggers the filter mechanism
    if (len(discovered_fg) != 0 and starting_mol == "filter"):
    
                       print("passed functional groups: " + str(fg_filter(discovered_fg)))
                       
                       
    #Task: Skips the first 7 lines of the RASCALL_Molecule_Identifiers.csv 
    for i in range(0,7):
        mol.readline()
        #line_counter += 1
    #print("starting mol: " + starting_mol)

    #Task: confronts the starting molecule with each molecule in the
    #SMILES column, if there is a match the rascall output is
    #printed. If the SMILES column cell is malfunctioning (typing
    #issues causes RASCALL to not output the results for a requested
    #molecule), the rdkit_SMILES column is attempted instead. If both
    #columns are malfunctioning the user is warned with an appropriate message.
    for m in mol.readlines():
        if m.split(",")[0] == starting_mol:
            try:
                output = subprocess.check_output(['./rascall_list', '--mol',  m.split(",")[0]])
                if  b"with functionals"in output:
                    output_decoded = output.decode("utf-8")
                    out_len = len(output_decoded.split('\n'))
                    funct_gr_primitive = []
                    for v in range(3, out_len-1):
                        funct_gr_primitive.append(output_decoded.split('\n')[v].split(",")[0].replace("(", "").replace("'","").replace(" ",""))
                        
                        
                        
                    #print(output.split('\n'))
                    #print(funct_gr)
                    funct_gr_final = list(dict.fromkeys(funct_gr_primitive))
                    discovered_fg.extend(funct_gr_final)
                    print("-----------------")
                    print("-----------------")
                    print("This molecule contains the following functional groups: ")
                    print(funct_gr_final)
                    print("----------------")
                    print("----------------")
                    for fg in funct_gr_final:
                        fg_output = subprocess.check_output(['./rascall_list', '--fg', fg])
                        if b"Too many" in fg_output:
                            print(fg + "->" + "Too many molecules to list")
                            print("-----------")
                        elif b"not in database" in fg_output:
                            print(fg + "->" + "Requested functional group not in database")
                            print("-----------")
                        else:
                            fg_output_decoded = fg_output.decode("utf-8")
                            print(fg_output_decoded.split("\n")[0])
                            print(fg_output_decoded.split("\n")[4])
                            print("-----------")
                            print("-----------")
                            print("Some functional groups were discovered. Type 'filter' to filter their wavenumber")
                        
                        
            except subprocess.CalledProcessError:
                try:
                    output = subprocess.check_output(['./rascall_list', '--mol', m.split(",")[1]])
                    
                except subprocess.CalledProcessError:
                    print("Both columns' elements are malfunctioning")
                    sys.exit()
                    break

            break
        
    mol.close()
