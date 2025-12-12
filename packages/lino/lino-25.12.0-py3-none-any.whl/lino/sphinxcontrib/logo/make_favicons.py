from favicons import Favicons

png_file = "src/synodal-icon.png"
out_path = "static/favicons"

with Favicons(png_file, out_path) as favicons:
    favicons.generate()
    for icon in favicons.filenames():
        print(icon)
