"""Combine rendered slide PNGs (POI fallback) into one PDF. Usage: to_pdf.py <png_dir> <prefix> <out.pdf>"""
import glob, os, sys
from PIL import Image

files = sorted(glob.glob(os.path.join(sys.argv[1], sys.argv[2] + '-*.png')))
ims = [Image.open(f).convert('RGB') for f in files]
ims[0].save(sys.argv[3], save_all=True, append_images=ims[1:], resolution=100.8, quality=82)
