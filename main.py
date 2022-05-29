from function.textDetection import textDetection
from function.sacn import scan
from function.mosaic import imageMosaic

if __name__ == "__main__":
    imagePath = "./sample/Korean-ID sample.png"
    result = textDetection(imagePath)
    for k, v in result.items():
        imageMosaic(v, imagePath)
