import subprocess
import os

#Purpose: facilitates the search for a particular molecule or
#functional group corresponding to a certain wavenumber range

#Author: Nicola Paparella

fg = open("funcs_test.txt")
discovered_fg = []

def fg_filter():

    while True:
        print("Select the range: ")
        print(" ")
        print("--------------------")
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
    return maxi, mini


#Task: asks the user if they want to apply the filter to the high end,
#low end, or average of the wavenumber spectrum
def order_choice():
    while True:
        fil_order = input("Choose an order at which the filter will be applied: (low, high or average) ")
        if isinstance(fil_order, str):

            if fil_order == "low" or fil_order == "high" or fil_order == "average":
                return fil_order
            else:
                print("Insert a valid string")
        else:
            print("not a valid command")
        


#Task: stores and display the functional groups and their shapes according to the
#maximum and minimum values chosen for the filter
def adding_funct_gr(order, fg_list, func_gr, shape, minimum, maximum):
    fg_list = open("functionals.csv", encoding='iso-8859-1')
    fg_list_len = 284

    #Task: go through all functional groups until a correspondeance in name and shape is found
    name_and_shape = func_gr + "---" + shape

    for l in range(0, fg_list_len-1):
        fg_info = fg_list.readline()
        fg_info_as_list = fg_info.split(",")
        if name_and_shape == fg_info_as_list[0] + "---" + fg_info_as_list[1]:

            if order == "high":

                if fg_info_as_list[3] < maximum and fg_info_as_list[3] > minimum:
                    
                    fg_list.append(func_gr)

                

            elif order == "low":

                if fg_info_as_list[2] < maximum and fg_info_as_list[2] > minimum:

                    fg_list.append(func_gr)
                    

            else:
                print("ERROR! order name is incoherent!")
                sys.exit()
                    
                    
        
        

    fg_list.close()
    
    #Task: if the wavenumber corresponding to the functional groups
    #and to the order searched is found, check if it is coherent with
    #the filter parameters, if it is, add the functional group to the 'filtered list'.
   
            
        

def librarian(maximum, minimum):

    order = order_choice()
    while True:
        mol = open('RASCALL_Molecule_Identifiers.csv', encoding='iso-8859-1')
        starting_mol = input("Insert the mol with which beginning the exploration (only RASCALL column is considered, not rdkit_RASCALL)")
        
        
        #Task: filters the wavenumbers of all functional groups that were discovered
        if (len(discovered_fg) != 0 and starting_mol == "filter"):
            print("Note to developer: insert filter here!")
            
        #Task: Skips the first 7 lines of the RASCALL_Molecule_Identifiers.csv 
        for i in range(0,7):
            mol.readline()

        #Taks: goes through all molecule list and lets the program
        #continue until it finds a match for starting_mol
        for m in mol.readlines():
            if m.split(",")[0] == starting_mol:
                try:
                    output = subprocess.check_output(['./rascall_list', '--mol', m.split(",")[0]])
                    if b"with functionals" in output:
                        output_decoded = output.decode("utf-8")
                        out_len = len(output_decoded.split('\n')) #output length

                        funct_gr_repetitive = []
                        
                        
                        for v in range(3, out_len-1):
                            
                            funct_gr_repetitive.append(output_decoded.split('\n')[v].split(",")[0].replace("(", "").replace("'","").replace(" ",""))



                            
                        #Meaning: unfiltered functional groups
                        print(funct_gr_repetitive)
                        funct_gr_fil = []
                        if order == "average":
                            for w in range(3, out_len-1):
                                func_gr = output_decoded.split('\n')[w].split(",")[0].replace("(", "").replace(";","").replace(" ", "")
                                shape = output_decoded.split('\n')[w].split(",")[1].replace("(",
                                                                                "").replace(";","").replace(" ","")
                                name_and_shape = func_gr + "---" + shape
                                
                                wavenumber_avg = int(output_decoded.split('\n')[w].split(",")[2].replace("(","").replace(";","").replace("",""))
                                if wavenumber_avg < maximum and wavenumber_avg > minimum:
                                    print("molecule passed")
                                    funct_gr_fil.append(func_gr)
                                    print("fg_list_avg: ", funct_gr_fil)

                        else:
                            for w in range(3, out_len-1):
                                func_gr = output_decoded.split('\n')[w].split(",")[0].replace("(",
                                                                                "").replace(";","").replace(" ","")
                                shape = output_decoded.split('\n')[w].split(",")[1].replace("(",
                                                                                "").replace(";","").replace(" ","")
                            

                                print("func_gr: ", func_gr)
                                print("shape: ", shape)
                            
                                adding_funct_gr(order, funct_gr_fil, func_gr, shape, minimum, maximum)


                        #print(funct_gr_fil)
                        funct_gr_fil_fin = list(dict.fromkeys(funct_gr_fil))
                        print("--------------")
                        print("--------------")
                        print("final unfiltered functional group list: ", funct_gr_fil_fin)
                        
                       # print("This molecule contains the following functional groups: ")
                       # print(funct_gr_final)
                        print("--------------")
                        print("--------------")
                        for fg in funct_gr_fil_fin:
                            print("fg: ", fg.replace('\n', ""))
                            fg_output = subprocess.check_output(['./rascall_list', '--fg', fg.replace("'", "")])
                            if b"Too many" in fg_output:
                                print(fg + "->" + "Too many molecules to list")
                                print("--------")
                            elif b"not in database" in fg_output:
                                print(fg + "->" + "Requested functional group not in database")
                                print("--------")
                            else:
                                fg_output_decoded = fg_output.decode("utf-8")
                                print(fg_output_decoded.split("\n")[0])
                                print(fg_output_decoded.split("\n")[4])
                                print("----------")
                                print("----------")
                           
                except subprocess.CalledProcessError:
                    try:
                        output = subprocess.check_output(['./rascall_list', '--mol', m.split(",")])

                    except subprocess.CalledProcessError:
                        print("Both columns' elements are malfunctioning")
                        sys.exit()
                        break
        
        mol.close()

maximum, minimum = fg_filter()
librarian(maximum, minimum)


