from bs4 import BeautifulSoup
import requests
import csv
from itertools import zip_longest

# define lists to add elements inside them and use them elsewhere
job_title = []
company_name = []
location_name = []
skills = []
links = []
page_num = 0

# while loop To repeat until the last minimum number of pages
while True:
    # to catch any error
    try:
        page = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={page_num}")
        # add page content to a variable to use
        src = page.content
        soup = BeautifulSoup(src)
        # to search for the number of result pages
        page_limit = int(soup.find("strong").text)

        # if statement to in order not to exceed the minimum number of pages allowed
        if( page_num > page_limit // 15 ):
            print("pages ended, terminate")
            break

        # extracting the desired content from the page and linking it to variables
        job_titles = soup.find_all("h2", { "class": "css-m604qf" } )
        company_names = soup.find_all("a", { "class": "css-17s97q8" } )
        locations_names = soup.find_all("span", { "class": "css-5wys0k" } )
        job_skills = soup.find_all("div", { "class": "css-y4udm8" } )

        #  to add page content from html code to text and add it in lists
        for i in range(len(job_titles)):
            job_title.append(job_titles[i].text)
            links.append(job_titles[i].find("a").attrs['href'])
            company_name.append(company_names[i].text.replace("-", "").strip())
            location_name.append(locations_names[i].text)
            skills.append(job_skills[i].text)
        # to change the page
        page_num += 1
        print("page switched")

    # to catch any error and alert us
    except:
        print("error occurred")
        break

# write the names of the data extracted from the site in the CSV file
file_list = [job_title, company_name, location_name, skills, links]
exported = zip_longest(*file_list)  # to unpacking our list # x = [1 , 2]  ,  y = [a , b]
                                                            # z = [x , y]  --> *z = [[1 , 2] , [a , b]]
                                                            # zip_longest  -->         [1,a] [2,b]      
# to open/create a CSV file to write our data inside it
with open("/Users/Connect/Desktop/Beautiful Soup - PJ_1/jobs-tutorial.csv", "w") as myfile:
    # to fill the data in the file rows
    wr = csv.writer(myfile)
    wr.writerow(["job title", "company name", "location", "skills", "links"])
    wr.writerows(exported)