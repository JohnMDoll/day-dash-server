# [Day Dash](https://www.mydaydash.com/)
###### * An app to get your day started * https://www.mydaydash.com/

## Project Overview

Day Dash is a personal dashboard intended to be used in the morning or evening to quickly see what the rest of the day, or tomorrow, has in store.

For more user UI/UX focused information see the [Client README](https://github.com/JohnMDoll/day-dash-client/edit/main/README.md)

## Design Decision Explanations

• The backend is a Django REST API written with the highest priority on sending minimal data to the client and preserving user privacy.
• WeatherAPI.com is used for weather data because they allow a large number of API hits each month on their free tier.

## Feature Highlights

• User zipcodes are used with WeatherAPI to get relevent weather for users
• Weather data trimmed down as much as possible before responding to client
• pyzipcode used to check user timezones to ensure user day end times are correct
• Event list responses default to same day and later events sorted by starting datetimes

## Tech Stack

![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![NPM](https://img.shields.io/badge/NPM-%23CB3837.svg?style=for-the-badge&logo=npm&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)

## Author Info

|<h3>John Doll</h3>  |
|:--------------------:|
|[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://www.github.com/JohnMDoll) [![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/john-m-doll)|
