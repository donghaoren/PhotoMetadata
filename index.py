# index.py

import sqlite3 as sqlite
import os
import sys
import hashlib
import time

from canon import process as process_canon
from generic import process as process_generic

acceptable_extensions = set([
    "cr2", "rw2"
])

def sha256_file(path):
    f = open(path, "rb")
    sha256 = hashlib.sha256()
    for chunk in iter(lambda: f.read(1048576), b''):
        sha256.update(chunk)
    return unicode(sha256.hexdigest())

def update(db = "db.sqlite", root = "."):
    print "Update: DB = %s, ROOT = %s" % (db, root)

    conn = sqlite.connect(db)
    c1 = conn.cursor()
    c1.execute("""CREATE TABLE IF NOT EXISTS photos (path TEXT UNIQUE, size INT, hash TEXT, mtime INT,
                original_time INT,
                camera_model TEXT, lens_model TEXT,
                focal_length TEXT,
                exposure_program TEXT, exposure_bias TEXT,
                shutter TEXT, aperture TEXT, iso_speed TEXT)
               """)
    c1.execute("CREATE INDEX IF NOT EXISTS idx_path ON photos(path)")
    c1.execute("CREATE INDEX IF NOT EXISTS idx_hash ON photos(hash)")
    c1.execute("CREATE INDEX IF NOT EXISTS idx_otime ON photos(original_time)")

    # Scan for RAW files.
    for folder, dirs, files in os.walk(root):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for f in files:
            try:
                path = os.path.join(folder, f)
                # Filter, only accept RAW files.
                ext = os.path.splitext(path)[1][1:].lower()
                if not ext in acceptable_extensions: continue

                # Read filesystem metadata.
                stat_v = os.stat(path)
                mtime = int(stat_v.st_mtime)
                size = stat_v.st_size

                # Is the file already processed?
                exist = False
                for (_mtime, _size, ) in c1.execute("SELECT mtime, size FROM photos WHERE path = ?", (path, )):
                    if size == size and mtime == _mtime:
                        exist = True
                    else:
                        print "Photo mismatch: %s, mtime = %d -> %d, size = %d -> %d" % (path, _mtime, mtime, _size, size)
                        c1.execute("DELETE FROM photos WHERE path = ?", (path, ))
                if exist:
                    print "Exist: %s" % path
                    continue

                print "File: %s" % path
                hash_value = sha256_file(path)
                for (_path, ) in c1.execute("SELECT path FROM photos WHERE hash = ?", (hash_value, )):
                    print "  Duplicate: %s" % _path

                # Initial metadata, everything is unknown.
                metadata = {
                    "shutter": "unknown",
                    "aperture": "unknown",
                    "iso_speed": "unknown",
                    "focal_length": "unknown",
                    "exposure_bias": "unknown",
                    "exposure_program": "unknown",
                    "camera_model": "unknown",
                    "lens_model": "unknown",
                    "original_date_time": 0
                }



                if ext == "cr2":
                    process_canon(path, metadata)
                else:
                  process_generic(path, metadata)

                print ", ".join([ str(metadata[x]) for x in metadata ]), mtime, size

                c1.execute("""INSERT INTO photos
                     (
                      path, size, hash, mtime,
                      original_time,
                      camera_model, lens_model,
                      focal_length,
                      exposure_program, exposure_bias,
                      shutter, aperture, iso_speed
                     ) VALUES (
                      ?, ?, ?, ?,
                      ?,
                      ?, ?,
                      ?,
                      ?, ?,
                      ?, ?, ?)
                     """,
                     (
                      path, size, hash_value, mtime,
                      metadata["original_date_time"],
                      metadata["camera_model"], metadata["lens_model"],
                      metadata["focal_length"],
                      metadata["exposure_program"], metadata["exposure_bias"],
                      metadata["shutter"], metadata["aperture"], metadata["iso_speed"],
                     )
                )
            except:
                # Commit before we die.
                conn.commit()
                raise
    conn.commit()
