from PIL import Image
from io import BytesIO


def roundtrip(im, **options):
    out = BytesIO()
    im.save(out, "JPEG2000", **options)
    bytes = out.tell()
    out.seek(0)
    im = Image.open(out)
    im.bytes = bytes  # for testing only                                                             
    im.load()
    return im

j2k = Image.open('./Carrier.j2k')
#im = roundtrip(j2k)
#print (im.tobytes() == j2k.tobytes())
#self.assert_image_equal(im, j2k)   

