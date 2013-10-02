Unofficial UR CampusDish API
==============
I love the University of Rochester, but there are some things I wish it did better. Dining hall menus are one of the things I think could be made much better, so I decided to try my best at improving them on my own!

The first step to making better menus is getting the data, and that's where this project comes in. This is the source for RESTful API that represents the current dining hall menus for Danforth and Douglass. All data comes from screen scraping the [online menus](http://www.campusdish.com/en-US/CSNE/Rochester/Menus/DanforthFreshFoodCompany.htm) provided by CampusDish. They're a bit crusty, so the code for this isn't pretty, but it works!

The scraped data is then put into a Postgres database, (which will allow for some cool statistics over time) which is then used by the flask server to generate a RESTful API full of JSON awesomeness. No nested HTML tables here!

**The API is still under development, but as soon as I get it stable I will make it public for anyone to use.**

Documentation/more info will come soon!
