from blockMeshDictClass import *


# parameters
cTM = 1e-2
LS = 100*cTM
LB = 50*cTM
H = 1*cTM
W = 9*cTM

dX = dY = dZ = 1.4e-3

nCZ = 1
nCYGrad = 10

x0 = y0 = z0 = 0.0
grX = grY = grZ = "1.0"
grYtop = "2.0"

# create mesh
fvMesh = mesh()

### BLOCKS ###
# -- top left block
xC, yC, zC = x0, y0+H, z0
xE, yE, zE = xC+LS, y0+W, zC+dZ

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
neighbours = [topRight]

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
walls.append(topLeft.retFXZ0())

walls.append(topRight.retFXZE())

walls.append(bottomRight.retFXZ0())
walls.append(bottomRight.retFYZ0())

fvMesh.addPatch("walls", "wall", walls)

### WRITE ###
fvMesh.writeBMD("./system/")
