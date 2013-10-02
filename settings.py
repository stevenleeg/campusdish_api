import os

SPIDER_MODULES = ["scraper.spiders"]
ITEM_PIPELINES = [
    "scraper.pipelines.PostgresPipeline"
]

DATABASE =  {
    "drivername": "postgres",
    "host": os.environ["DB_HOST"],
    "port": os.environ["DB_PORT"],
    "username": os.environ["DB_USERNAME"],
    "password": os.environ["DB_PASSWORD"],
    "database": os.environ["DB_NAME"],
}
