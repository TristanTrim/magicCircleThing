
from PIL import Image
from multiprocessing import Pool
from math import sqrt, sin, cos, pi, fabs
from numpy import arange
from pprint import pprint
from copy import deepcopy

def drawCircle(
        circlePoints=10,
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

    points = tuple((cos(a)*circleRadius,sin(a)*circleRadius) for a in arange(0,2*pi,2*pi/circlePoints))
    pprint(points)

    ## make line functions
    # all functions return a number between 0 and 1
    # (or at least they are supposed to)
    functions = []
    def deltafy(coord,delta):
        x,y = coord
        return(x-delta[0],y-delta[1])
    def circleFunction(coord):
        x,y = deltafy(coord,center)
        distFromCenter = sqrt((x)**2+(y)**2)
        zeroAtRadius = distFromCenter-circleRadius
        return zeroAtRadius
        #return 1/(1+zeroAtRadius**2)
    functions+=[
            circleFunction,
            lambda c:circleFunction(c)+10,
            ]
    def makecircle(p):
        return lambda c: circleFunction(deltafy(c,p))+160
    for p in points:
        functions+=[makecircle(p)]
    def makeline(p1,p2):
        def line(coord):
            x,y = deltafy(coord,p1)
            xd,yd = p1[0]*p2[0],p1[1]*p2[1]#deltafy(p1,p2)
            dd = fabs(xd)+fabs(yd)
            xd,yd = xd/dd, yd/dd
            return(x*yd+y*xd)
        return line
    for p in points:
        functions+=[makeline(center,p)]
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

