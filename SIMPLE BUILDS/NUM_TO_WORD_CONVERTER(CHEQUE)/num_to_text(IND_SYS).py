def givetext(num):
    len_of_num = len(str(num))
    refdict = {0:"zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six",
        7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve",
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
            return res.lstrip("zero")

def num_to_text(number):
    strnum  = str(number)
    strnum = strnum.zfill(14)

    c_lak_digit = int(strnum[:2])
    c_tho_digit = int(strnum[ 2:4 ])
    c_hun_digit = int(strnum[ 4 ])
    cror_digit = int(strnum[5:7])
    lak_digit = int(strnum[7:9])
    tho_digit = int(strnum[9:11])
    hun_digit = int(strnum[11])
    two_digit = int(strnum[11:13])


    cr_l = givetext(c_lak_digit)
    cr_t = givetext(c_tho_digit)
    cr_h = givetext(c_hun_digit)
    cd = givetext(cror_digit)
    ld = givetext(lak_digit)
    td = givetext(tho_digit)
    hd = givetext(hun_digit)
    twod = givetext(two_digit)
    
    txt = ""
    if(cr_l != "zero"):
        txt += cr_l
        txt+= " lakh "
    if(cr_t != "zero"):
        txt += cr_t
        txt+= " thousand "
    if(cr_h != "zero"):
        txt += cr_h
        txt+= " hundred "
    if(cd != "zero" or (cr_l != "zero" or cr_t != "zero" or cr_h!="zero")):
        txt += cd
        txt+= " crore "
    if(cd != "zero"):
        txt += cd
        txt+= " crore "
    if(ld != "zero"):
        txt += ld
        txt+= " lakh "
    if(td != "zero"):
        txt += td
        txt+= " thousand "
    if(hd != "zero"):
        txt += hd
        txt+= " hundred "
    if(twod != "zero"):
        txt += twod
    standardization = f"{x[:2]},{x[2:4]}{x[5]},{x[5:7]},{x[7:9]},{x[9:11]},{x[11]}{x[11:13]}"
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
            num_s = input("ENTER NUMERICAL VALUE:::(<99 lakh crore) upto 14 digit:::")
            if(num_s.isnumeric() and len(num_s)<=14):
                x = num_s.zfill(14)
                num = int(num_s)
                print(num_to_text(num))
            else:
                print("INVALID INPUT")

    elif(choice == 2):
        print("QUITTING....")
        break
    else:
        print("ENTER CORRECT CHOICE FROM THE MENU...")


