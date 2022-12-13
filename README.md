# MongoDB Scraper PoC
Mongo databases are open in the wild! Here's a Proof of Concept scraper!

Apparently people still leave out open databases out there in the wild, here's how to scrape them.

## How to run
Put one leg ahead of another. Just kidding.
To run, change address on line 75 to your desired address and
```
python3 mongo.py
```

This will (or atleast try to) scrape the contents of the target database and neatly place them into data/ according to their filenames.
I've only tested this on "perfect-conditions", so expect stuff to not work. No guarantees given.
