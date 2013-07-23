Photo Metadata
====

Collect RAW files' metadata into a SQLite database and create a visualization for them.

License
----

GPLv3

Dependencies
----

* Python:
  * pyexiv2
  * sqlite3

* jQuery and D3.js (included)

Usage
----

Write config.ini to tell the program where your photos are.

    [main]
    path = <path to a directory containing your RAW files>

Run `python run.py`.

Open `vis.html` to see the results.
