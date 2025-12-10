
from blockMeshDictClass import *

# parameters
cTM = 1e-2
LS = 1.01
LB = 49*cTM
H = 0.01091
W = 9*cTM

dX = dY = dZ = 1.3e-3

nCZ = 1
nCYGrad = 10

x0 = y0 = z0 = 0.0
grX = grY = grZ = "1.0"
grYtop = "2.0"

# create mesh
fvMesh = mesh()

### BLOCKS ###
# -- lambda block
xC, yC, zC = x0, y0, z0
xE, yE, zE = xC+LS, y0+H, zC+dZ

# vertices
vertices = [
        [xC, yC, zC],
        [xE, yC, zC],
        [xE, yE, zC],
        [xC, yE, zC],
        [xC, yC, zE],
        [xE, yC, zE],
        [xE, yE, zE],
        [xC, yE, zE],
    ]

# neighbouring blocks
neighbours = []

# number of cells
nCX = int(round(abs(xE-xC)/dX))
nCY = int(round(abs(yE-yC)/dY))
nCells = [nCX, nCY, nCZ]

# grading
grading = [grX, grY, grZ]

# create the block
lambdaBlock = fvMesh.addBlock(vertices, neighbours, nCells, grading, name = 'lambdaZone', cellZone=True)

# -- top left block
xC, yC, zC = x0, y0+H, z0
xE, yE, zE = xC+LS, y0+W, zC+dZ

# vertice
vertices = [
        [xC, yC, zC],
        [xE, yC, zC],
        [xE, yE, zC],
        [xC, yE, zC],
        [xC, yC, zE],
        [xE, yC, zE],
        [xE, yE, zE],
        [xC, yE, zE],
    ]

# neighbouring blocks
neighbours = [lambdaBlock]

# number of cells
nCX = int(round(abs(xE-xC)/dX))
nCY = int(round(abs(yE-yC)/dY))
nCells = [nCX, nCY, nCZ]

# grading
grading = [grX, grY, grZ]

# create the block
topLeft = fvMesh.addBlock(vertices, neighbours, nCells, grading)

# -- top right block
xC, yC, zC = xE, yC, z0
xE, yE, zE = xC+LB, yE, zC+dZ

# vertices
vertices = [
        [xC, yC, zC],
        [xE, yC, zC],
        [xE, yE, zC],
        [xC, yE, zC],
        [xC, yC, zE],
        [xE, yC, zE],
        [xE, yE, zE],
        [xC, yE, zE],
    ]

# neighbouring blocks
neighbours = [topLeft]

# number of cells
nCX = int(round(abs(xE-xC)/dX))
nCells = [nCX, nCY, nCZ]

# grading
grading = [grX, grY, grZ]

# create the block
topRight = fvMesh.addBlock(vertices, neighbours, nCells, grading)

# -- bottom right block
xC, yC, zC = xC, y0, z0
xE, yE, zE = xE, y0+H, zC+dZ

# vertices
vertices = [
        [xC, yC, zC],
        [xE, yC, zC],
        [xE, yE, zC],
        [xC, yE, zC],
        [xC, yC, zE],
        [xE, yC, zE],
        [xE, yE, zE],
        [xC, yE, zE],
    ]

# neighbouring blocks
neighbours = [lambdaBlock, topRight]

# number of cells
nCY = int(round(abs(yE-yC)/dY))
nCells = [nCX, nCY, nCZ]

# grading
grading = [grX, grY, grZ]

# create the block
bottomRight = fvMesh.addBlock(vertices, neighbours, nCells, grading)

### PATCHES ###
# -- empty
empty = list()
for block in fvMesh.blocks:
    empty.append(block.retFXY0())
    empty.append(block.retFXYE())

fvMesh.addPatch("frontAndBack", "empty", empty)

# -- inlet
inlet = list()
inlet.append(topLeft.retFYZ0())

fvMesh.addPatch("inlet", "patch", inlet)

# -- outlet
outlet = list()
outlet.append(topRight.retFYZE())
outlet.append(bottomRight.retFYZE())

fvMesh.addPatch("outlet", "patch", outlet)

# -- walls
walls = list()
walls.append(topLeft.retFXZE())

walls.append(topRight.retFXZE())

walls.append(bottomRight.retFXZ0())

fvMesh.addPatch("walls", "wall", walls)

# -- wallInsideLambda
wallInsideLambda = list()
wallInsideLambda.append(lambdaBlock.retFXZ0())
wallInsideLambda.append(lambdaBlock.retFYZ0())

fvMesh.addPatch("wallInsideLambda", "wall", wallInsideLambda)

### WRITE ###
fvMesh.writeBMD("./system/")
