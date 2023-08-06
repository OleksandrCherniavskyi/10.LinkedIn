# 10.LinkedIn

Project content 2 functions 

![image](https://github.com/OleksandrCherniavskyi/10.LinkedIn/assets/105165580/363b0094-1a27-4bd7-8e71-e80179ff7772)

1. Collect data for applicants from LinkedIn page, just put link for page add in DB


![image](https://github.com/OleksandrCherniavskyi/10.LinkedIn/assets/105165580/1512fdf2-c2c0-4472-a7e3-73347c4cd0c1)


2. Collect data about firms you need adjust filters on linkedin pages, copy generate link in terminal, next program collect needed data in DB.
   1. Link for your case: https://www.linkedin.com/search/results/COMPANIES/?companyHqGeo=%5B%22102974008%22%2C%22104341318%22%2C%22106137034%22%2C%22101464403%22%2C%22104738515%22%2C%22103819153%22%2C%22100456013%22%2C%22103119917%22%2C%22104514075%22%2C%22105333783%22%2C%22101855366%22%2C%22106693272%22%2C%22101452733%22%2C%22100288700%22%2C%22100364837%22%2C%22104677530%22%2C%22104508036%22%2C%22105117694%22%2C%22100565514%22%2C%22102890719%22%2C%22106670623%22%2C%22101165590%22%2C%22101282230%22%2C%22102264497%22%2C%22103350119%22%2C%22105015875%22%2C%22105072130%22%2C%22105646813%22%5D&companySize=%5B%22I%22%5D&industryCompanyVertical=%5B%221862%22%5D&origin=FACETED_SEARCH&sid=rLp"

In code you must input your ```login``` and ```password``` from your LinkedIn page.
In my case ```from client_info import password, login``` i created file ```client_info``` where located my private setting

## You can use docker desktop to run project
- copy repository
- created ```client_info.py``` where add you login and password 
- docker build -t image_name .
- docker run  image_name
