def givetext(num):
    len_of_num = len(str(num))
    refdict = {0:"zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six",
        7: "seven", 8: "Eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve",
        13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen",
        18: "eighteen", 19: "nineteen", 20: "twenty", 30: "thirty", 40: "forty",
        50: "fifty", 60: "sixty", 70: "seventy", 80: "Eighty", 90: "ninety"}
    if(len_of_num == 1):
        return refdict[num]
        
    elif(len_of_num == 2):
        if(num in refdict):
            return refdict[num]

        else:
            tensdig = int(str(num)[0])*10
            onesdigit = int(str(num)[1])
            res = refdict[tensdig] +" "+ refdict[onesdigit]
            return res
    elif(len_of_num == 3):
            hundig = int(str(num)[0])
            two_dig = int(str(num)[-2:])
            if(two_dig == 0):
                 res = refdict[hundig]
            else:
                 res = refdict[hundig]+" hundred "+givetext(two_dig)
            return res
def num_to_text(number):
    strnum  = str(number)
    strnum = strnum.zfill(15)

    trillion_digit = int(strnum[:3])
    billion_dig = int(strnum[3:6])
    million_digit = int(strnum[6:9])
    tho_digit = int(strnum[9:12])
    hun_digit = int(strnum[12])
    two_digit = int(strnum[13:])


    tri_d = givetext(trillion_digit)
    bil_d = givetext(billion_dig)
    mil_d = givetext(million_digit)
    td = givetext(tho_digit)
    hd = givetext(hun_digit)
    twod = givetext(two_digit)
    
    txt = ""
    if(tri_d != "zero" ):
        txt += tri_d
        txt+= " trillion "
    if(bil_d != "zero"):
        txt += bil_d
        txt+= " billion "
    if(mil_d != "zero"):
        txt += mil_d
        txt+= " million "
    if(td != "zero"):
        txt += td
        txt+= " thousand "
    if(hd != "zero"):
        txt += hd
        txt+= " hundred "
    if(twod != "zero"):
        txt += twod
    standardization = f"{strnum[:3]},{strnum[3:6]},{strnum[6:9]},{strnum[9:12]},{strnum[12]}{strnum[13:]}"
    while(standardization.startswith('0')) or (standardization.startswith(',')):
           standardization  = standardization[1:]
    print(standardization)
    if(len(txt) == 0):
        return "Zero Rupee"
    return txt +" Rupees"
 
while(1):
    print("\t\t")
    print("\t***NUM TO TEXT ***")
    print("\t1.Text generator")
    print("\t2.EXIT")
    choice = int(input("ENTER YOUR CHOICE FROM THE MENU "))
    if(choice == 1):
            num_s = input("ENTER NUMERICAL VALUE:::(<999 trillion) upto 15 digit:::")
            if(num_s.isnumeric() and len(num_s)<=15):
                num = int(num_s)
                print(num_to_text(num))
            else:
                print("INVALID INPUT")

    elif(choice == 2):
        print("QUITTING....")
        break
    else:
        print("ENTER CORRECT CHOICE FROM THE MENU...")


