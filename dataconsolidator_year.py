#a second script, designed to be run after the first, to include additional year data.

import csv

YEAR = 2019
R = "c_year.csv"
W = "consolidation_new_year.csv"
"""We're importing a file with the format:
0    first_name,
1    last_name,
2    email,
3    zip,
4    bad year field,
5    bad year field,
6    bad year field,
7    birthyear
"""

def consolidator(file, wfile):
    with open(file) as readfile:
        with open(wfile, "w") as writefile:
            data = csv.reader((line.replace('\0','') for line in readfile), delimiter=",")
            writer = csv.writer(writefile)
            for row in data:
                first_name = row[0]
                last_name = row[1]
                email = row[2]
                zipcode = row[3]
                year3 = row[4]
                year2 = row[5]
                year1 = row[6]
                birthyear = row[7]

                if first_name == "first_name":
                    final_first_name = "first_name"
                    final_last_name = "last_name"
                    final_email = "email"
                    final_zipcode = "age"
                    final_birthyear = "birthyear"
                    
                else:
                    final_first_name = first_name
                    final_last_name = last_name
                    final_email = email
                    final_zipcode = zipcode
                    final_birthyear = ""

                    yearhierarchy = [birthyear, year1, year2, year3]
                    i = 0
                    while final_birthyear == "" and i<len(yearhierarchy):
                        if yearhierarchy[i] != None and len(yearhierarchy[i])>=4:
                            year = yearhierarchy[i][:4]
                            if year.isdigit():
                                final_birthyear = year
                        i += 1
                    
                writer.writerow([final_first_name, final_last_name, final_email, final_zipcode, final_birthyear])

if __name__ == '__main__':
    consolidator(R,W)