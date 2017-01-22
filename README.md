# Requirements

1. [Python 3.5](https://www.python.org/downloads/release/python-350/) or similar
2. [numpy](http://www.numpy.org/)
3. [OpenCV 3](https://www.solarianprogrammer.com/2016/09/17/install-opencv-3-with-python-3-on-windows/) for Python

Python [Pillow](https://pypi.python.org/pypi/Pillow/) is no longer a requirement

# File Structure

- The `driver.py` is the testing script.
- `Tests_PNG_32` has the results of the tests mentioned in the paper
- `Embedder.py` is used for embedding the biometric onto the carrier
- `Extractor.py` is used for recovering the biometric
- The `TextTest` folder has the text encoding and decoding scripts along with results
- `JpgTests` and `LFSR` explore the problems due to lossy compression