
from PIL import Image
from multiprocessing import Pool
from math import sqrt, sin, cos, pi, fabs
from numpy import arange
from pprint import pprint
from copy import deepcopy

def drawCircle(
        circlePoints=4,
        imageSize=(500,500),
        circleRadius=200,
        circleColour=(0,255,0),
        backgroundColour=(255,255,255),
        title=None,
        ):
   ### initialize image!
    image = Image.new("RGB",imageSize,backgroundColour)
    pixels = image.load()

   ### make some helpful vars
    width = imageSize[0]
    height= imageSize[1]
    center = (width/2,height/2)
    # the amount backgroundColour needs to change to be circleColour
    relativeColour = (circleColour[0]-backgroundColour[0],
                      circleColour[1]-backgroundColour[1],
                      circleColour[2]-backgroundColour[2])
    ## points around the circle
    points = tuple((cos(a)*circleRadius,sin(a)*circleRadius) for a in arange(0,2*pi,2*pi/circlePoints))

    ## Some tools for making functions
    functions = []
    def getDelta(coord,delta):
        x,y = coord
        return(x-delta[0],y-delta[1])
    def makecircle(p,r):
        def circle(coord):
            x,y = getDelta(getDelta(coord,p),center)
            distFromCenter = sqrt((x)**2+(y)**2)
            zeroAtRadius = distFromCenter-r
            return zeroAtRadius
        return circle
    def makeline(p1,p2):
        def line(coord):
            x,y = getDelta(getDelta(coord,p1),center)
            xd,yd = p2[0]-p1[0],p1[1]-p2[1]#getDelta(p1,p2)
            dd = fabs(xd)+fabs(yd)
            xd,yd = xd/dd, yd/dd
            return(x*yd+y*xd)
        return line
    ## actually define some functions to be drawn
    # these are 3d functions, they take x,y coordinates and return z
    # where z is close to 0 a line will be drawn
    functions+=[
            makecircle((0,0),circleRadius)
            ]
    for p in points:
        functions+=[makecircle(p,30)]
    for i in range(len(points)):
        for j in range(i+1,len(points)):
            functions+=[makeline(points[i],points[j])]
    # this function evaluates a coordinate against all the functions
    def runFunctions(coord):
        current = 0
        for function in functions:
            current += 1/(1+function(coord)**2)
        return current if current < 1 else 1

    ## iterate over pixels filling them with pretty colours!
    coords=list((x,y) for x in range(width) for y in range(height))
    def renderPixel(coord):
        # get the amount this pixel is closer to circle colour
        # than it is to backgroundColour
        intensity = runFunctions(coord)
        thisPixColour = (
                int(backgroundColour[0]+(relativeColour[0]*intensity)),
                int(backgroundColour[1]+(relativeColour[1]*intensity)),
                int(backgroundColour[2]+(relativeColour[2]*intensity))
                )
        pixels[coord] = thisPixColour
    map(renderPixel,coords)

    ## save image
    if not title:
        title = "{0}pointed{1[0]}by{1[1]}circle.jpg".format(circlePoints,imageSize)
    image.save(title)

if __name__=="__main__":
    drawCircle()

