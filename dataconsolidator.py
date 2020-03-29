import csv

YEAR = 2019
R = "consolidate.csv"
W = "consolidation_new.csv"
FAKENUMS = ["1111111111", "2222222222", "3333333333", "4444444444", "5555555555", "6666666666", "7777777777", "8888888888", "9999999999", "0000000000", "1234567890", "0987654321"]
"""We're importing a file with the format:
0    first_name,
1    last_name,
2    email,
3    can2_user_address,
4    adress,
5    Age,
6    Age Group,
7    Age: ,
8    Birthdate,
9    birthyear,
10    Cell Phone Number,
11    Email: ,
12    gender,
13    gender identity,
14    Gender Pronouns,
15    Gender_Pronouns,
16    college grad year,
17    Graduation year,
18    Name,
19    Name: ,
20    Phone,
21    Phone #,
22    Phone Sync,
23    phone_number,
24    Phone_Sync,
25    PhoneSync,
26    Preferred Gender Pronouns

We want to return:
0    first_name
1    last_name
2    email
3    age
4    birthyear
5    Phone_Sync
        -standardized 10 digits
6    college_grad_year
7    pronouns
        -standardized
"""

def consolidator(file, wfile):
    with open(file) as readfile:
        with open(wfile, "w") as writefile:
            data = csv.reader((line.replace('\0','') for line in readfile), delimiter=",")
            writer = csv.writer(writefile)
            for row in data:
                first_name = row[0]
                last_name = row[1]
                name = row[18]
                name_colon = row[19]
                email = row[2]
                email_colon = row[11]
                #can2_user_address = row[3] - don't actually need to return
                #adress = row[4] - a useless field
                age = row[5]
                age_group= row[6]
                age_colon  = row[7]
                birth_date = row[8]
                #nothing in here
                birth_year = row[9]
                #pgps = row[26] - a useless field
                gender = row[12]
                gender_identity = row[13]
                gender_pronouns = row[14]
                gender_underscore_pronouns = row[15]
                #seems to be primary
                grad_year = row[16]
                graduation_year = row[17]     
                cell_phone_number = row[10]
                phone = row[20]
                phone_num = row[21]
                phone_space_sync = row[22]
                phone_number = row[23]
                phone_sync = row[24]
                phonesync = row[25]
                
                if first_name == "first_name":
                    final_first_name = "first_name"
                    final_last_name = "last_name"
                    final_email = "email"
                    final_age = "age"
                    final_birth_year = "birthyear"
                    final_phone = "Phone_Sync"
                    final_grad_year = "college_graduation_year"
                    final_pronouns = "pronouns"
                else:
                    final_first_name = first_name
                    final_last_name = last_name
                    final_email = ""
                    final_age = ""
                    final_birth_year = ""
                    final_phone = ""
                    final_grad_year = ""
                    final_pronouns = ""
        #get us the final phone            
                    phonehierarchy = [phone_sync, phone, phone_num, phone_space_sync, phonesync, phone_number, cell_phone_number]
                    i = 0
                    while (final_phone == "" or final_phone == None) and i < len(phonehierarchy):
                        final_phone = phonehierarchy[i]
                        final_phone = phonestrip(final_phone)
                        i += 1
        #get us the final name
                    if "@" in last_name:
                        email = last_name
                        last_name = ""
                    if last_name == "" or last_name == None:
                        if name != "" or name != None:
                            n = name.split(" ")
                        elif name_colon != "" or name_colon != None:
                            n = name_colon.split(" ")
                        if len(n) == 2:
                            final_last_name = n[1]
                            if first_name == "" or first_name == None:
                                final_first_name = n[0]
        #get us the final email
                    if email == "" or email == None:
                        final_email = email_colon
                    else:
                        final_email = email
        #get us the final college grad year
                    if grad_year != "" or grad_year != None:
                        final_grad_year = grad_year
                    else:
                        final_grad_year = graduation_year
        #get us the final age
                    if (birth_year != "" or birth_year != None) and len(birth_year) == 4 and birth_year.isdigit():
                        final_birth_year = birth_year
                        final_age = str(YEAR - int(birth_year))
                    else:
                        agehierarchy = [age, age_colon, age_group]
                        i = 0
                        while (final_age == "" or final_age == None) and i < len(agehierarchy):
                            final_age = agehierarchy[i]
                            final_age = agenormalize(final_age)
                            i += 1
        #get us pgps
                    genderhierarchy = [gender_underscore_pronouns, gender, gender_pronouns, gender_identity]
                    while (final_pronouns == "" or final_pronouns == None) and i < len(genderhierarchy):    
                        final_pronouns = genderhierarchy[i]
                        i += 1
                    final_pronouns = gendernormalize(final_pronouns)
                    final_first_name = namenormalize(final_first_name)
                    final_last_name = namenormalize(final_last_name)
                writer.writerow([final_first_name, final_last_name, final_email, final_age, final_birth_year, final_phone, final_grad_year, final_pronouns])

def phonestrip(num):
    final = ""
    for x in num:
        if x.isdigit():
            final += x
    if len(final) == 11 and final[0] == "1":
        final = final[1:]
    if len(final) != 10 or final in FAKENUMS:
        final = ""
    return final

def agenormalize(age):
    normalized = age
    if age.isdigit() and len(age) == 4:
        normalized = YEAR - int(age)
    elif len(age) > 1 and age[0].isdigit() and age[1].isdigit():
        if "-" in age and len(age) == 5:
            x = age[0:2]
            y = age[3:5]
            x = int(x)
            y = int(y)
            z = (y+x) // 2
            normalized = str(z)
        else:   
            normalized = age[:2]
    elif not age.isdigit():
        normalized = ""
    return str(normalized)

def gendernormalize(g):
    g = g.lower().strip()
    if "/" in g:
        a = g.split("/")
        g = a[0] + "/" + a[1]
    elif g == "m" or g == "male":
        g = "he/him"
    elif g == "f" or g == "female":
        g = "she/her"
    return g
        

def namenormalize(name):
    if len(name) > 1:
        name = name[0].upper() + name[1:].lower()
    elif len(name) == 1:
        name = name.upper()
    i = 0
    while i < len(name):
        if (name[i] == " " or name[i] == "-") and i != len(name)-1:
            n = name[:i+1] + name[i+1].upper() 
            if i != len(name)-2:
                name = n + name[i+2:]
        i += 1
    return name
    
    
    
    
    
    
    
    

if __name__ == '__main__':
    consolidator(R,W)