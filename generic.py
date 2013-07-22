import pyexiv2
import time

def process(path, opt):
    # Read image metadata.
    meta = pyexiv2.ImageMetadata(path)
    meta.read()
    ks = meta.exif_keys

    # # Display all entries.
    # for key in ks:
    #     try:
    #         if len(meta[key].human_value) < 100:
    #             print "%s = %s" % (key, meta[key].human_value)
    #     except: pass

    if "Exif.Image.Model" in ks:
        opt["camera_model"] = meta["Exif.Image.Model"].value.strip()

    if "Exif.Photo.DateTimeOriginal" in ks:
        opt["original_date_time"] = int(time.mktime(meta["Exif.Photo.DateTimeOriginal"].value.timetuple()))

    if "Exif.Photo.FocalLength" in ks:
        opt["focal_length"] = meta["Exif.Photo.FocalLength"].human_value

    if "Exif.Photo.ExposureTime" in ks:
        opt["shutter"] = meta["Exif.Photo.ExposureTime"].human_value

    if "Exif.Photo.FNumber" in ks:
        opt["aperture"] = meta["Exif.Photo.FNumber"].human_value

    if "Exif.Photo.ISOSpeedRatings" in ks:
        opt["iso_speed"] = meta["Exif.Photo.ISOSpeedRatings"].human_value

    if "Exif.Photo.ExposureBiasValue" in ks:
        opt["exposure_bias"] = meta["Exif.Photo.ExposureBiasValue"].human_value

    if "Exif.Photo.ExposureProgram" in ks:
        opt["exposure_program"] = meta["Exif.Photo.ExposureProgram"].human_value

    # This may not exist in Canon's raw files.
    if "Exif.Photo.LensModel" in ks:
        opt["lens_model"] = meta["Exif.Photo.LensModel"].human_value
    # This instead.
    if "Exif.Canon.LensModel" in ks:
        opt["lens_model"] = meta["Exif.Canon.LensModel"].human_value
    
    for key in opt:
        if isinstance(opt[key], str):
            opt[key] = unicode(opt[key], "utf-8", errors = 'ignore')
