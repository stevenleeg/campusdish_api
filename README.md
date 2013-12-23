Unofficial UR CampusDish API
===
I love the University of Rochester, but there are some things I wish it did better. Dining hall menus are one of the things I think could be made much better, so I decided to try my best at improving them on my own!

The first step to making better menus is getting the data, and that's where this project comes in. This is the source for a RESTful API that represents the current dining hall menus for Danforth and Douglass. All data comes from screen scraping the [online menus](http://www.campusdish.com/en-US/CSNE/Rochester/Menus/DanforthFreshFoodCompany.htm) provided by CampusDish. They're a bit crusty, so the code for this isn't pretty, but it works!

The scraped data is then put into a Postgres database, (which will allow for some cool statistics over time) which is then used by the flask server to generate a RESTful API full of JSON awesomeness. No nested HTML tables here!

Documentation
===
**NOTICE:** This API is still under heavy development. Anything on `/v0` endpoints are subject to change at any time. Having said that, I'll do my best to keep it as backwards compatible as possible (I should be mostly adding things, rather than moving/subtracting), so you should be able to build something off of it so long as you're willing to make adjustments to your code. Until the `/v1` endpoints are up you should assume that this is an unstable API.

**The base URL for all endpoints is `http://dining.stevegattuso.me`.**

## `/v0/dining_halls/<dining_hall>/<meal>`
Returns a menu for the given dining hall at the given meal time.

**Parameters:**
* `URL: dining_hall` - The name of the dining hall you're requesting a menu for.
* `URL: meal` - The meal you are requesting a menu for (see `/v0/meal` for options).
* `GET: date` - The date of the menu you're looking for. **(PLANNED)**

Example response:
```json
{
    "date": "2013-12-21", 
    "meal": "dinner", 
    "stations": {
        "bistro home zone": [
            {
                "title": "cornbread"
            }, 
            {
                "title": "three bean chili"
            }
        ], 
        "brick oven": [
            {
                "title": "classic cheese pizza"
            }
        ], 
        "dessert": [
            {
                "title": "oatmeal raisin cookie"
            }, 
            {
                "title": "chocolate chip cookie"
            }, 
            {
                "title": "chocolate waffle"
            }
        ], 
        "grill": [
            {
                "title": "ballpark hot dogs"
            }, 
            {
                "title": "crispy french fries"
            }
        ], 
        "produce market": [
            {
                "title": "salad bar "
            }
        ]
    }, 
    "status": 200
}

```

## `/v0/dining_hall`
Returns a list of dining halls available.

**Parameters:** None

Example response:
```json
{
    "dining_halls": [
        {
            "name": "Danforth"
        }, 
        {
            "name": "Douglass"
        }, 
        {
            "name": "Commons"
        }
    ], 
    "status": 200
}
```

## `/v0/meal`
Returns a list of meal options available.

**Parameters:** None

Example response:
```json
{
    "meals": [
        {
            "name": "lunch"
        }, 
        {
            "name": "dinner"
        }
    ], 
    "status": 200
}
```

## `/v0/schedule`
Returns a schedule for each dining hall.

```json
{
    "dining_halls": {
        "Commons": {
            "next_open": null, 
            "state": false
        }, 
        "Danforth": {
            "closes": "20:00:00", 
            "opened": "04:30:00", 
            "state": true
        }, 
        "Douglass": {
            "next_open": "2014-01-15 07:00:00", 
            "state": false
        }
    }, 
    "status": 200
}
```

Feedback
===
Hopefully people find this API to be useful! If you have any question/comments feel free to email me (steve at stevegattuso dot me) or create an issue and I'll be happy to help!
