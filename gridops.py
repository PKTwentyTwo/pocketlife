'''Some operations for the grid storage method to save time.'''
import hashlib
def cleanupgrid(grid):
    '''Removes all non-zero coordinates from the grid.'''
    newgrid = {}
    for x in grid:
        if grid[x] != 0:
            newgrid[x] = 1
    return newgrid
def shiftgrid(grid, dx, dy):
    '''Translate a grid by a given quantity.'''
    grid = cleanupgrid(grid)
    newgrid = {}
    for x, y in grid:
        if grid[(x, y)] != 0:
            newgrid[(x + dx, y + dy)] = 1
    return newgrid
def firstcell(grid):
    '''Find the first cell in a grid.'''
    whys = [coord[1] for coord in grid]
    topcoord = min(whys)
    exes =  [coord[0] for coord in grid if coord[1] == topcoord]
    leftcoord = min(exes)
    return (leftcoord, topcoord)
def transformgrid(grid, transformgridation):
    '''Apply a transformgridation to a grid.'''
    grid = cleanupgrid(grid)
    newgrid = {}
    transformgridations = ['flip_x', 'flip_y', 'identity', 'rot_90', 'rot_180', 'rot_270', 'flip_xy', 'rcw', 'rccw']
    if transformgridation not in transformgridations:
        raise ValueError('Only the following transformgridations are supported: '+str(transformgridations))
    match transformgridation:
        case 'flip_x':
            newgrid = {(-x, y):1 for x, y in grid}
        case 'flip_y':
            newgrid = {(x, -y):1 for x, y in grid}
        case 'identity':
            newgrid = {(x, y):1 for x, y in grid}
        case 'rot_90':
            newgrid = {(-y, x):1 for x, y in grid}
        case 'rot_180':
            newgrid = {(-x, -y):1 for x, y in grid}
        case 'rot_270':
            newgrid = {(y, -x):1 for x, y in grid}
        case 'flip_xy':
            newgrid = {(-x, -y):1 for x, y in grid}
        case 'rcw':
            newgrid = {(-y, x):1 for x, y in grid}
        case 'rccw':
            newgrid = {(y, -x):1 for x, y in grid}
    return newgrid
def getbbox(grid):
    '''Returns the bounding box of a grid in the form [x, y, dx, dy].'''
    grid = cleanupgrid(grid)
    if len(grid) == 0:
        #Empty patterns do not have a proper bounding box.
        return None
    exes = [c[0] for c in grid]
    whys = [c[1] for c in grid]

    x = min(exes)
    y = min(whys)
    dx = max(exes) - x + 1
    dy = max(whys) - y + 1
    return [x, y, dx, dy]
def sha1(instring):
    '''Return an integer representation of the SHA-1 hash of a string.'''
    hashed = hashlib.sha1(instring.encode('utf-8')).digest()
    totalint = 0
    for x in range(20):
        totalint += (256**x) * hashed[x]
    return totalint
def defaultshiftgrid(grid):
    '''Move a grid so that all coordinates are non-negative.'''
    grid = cleanupgrid(grid)
    bbox = getbbox(grid)
    return shiftgrid(grid, -bbox[0], -bbox[1])
def calcdigest(grid):
    '''Returns a digest of a grid, dependent on rotation and reflection but not absolute position.'''
    grid = defaultshiftgrid(grid)
    total = 0
    for x in grid:
        total += sha1(str(x))
    return total
def calcoctodigest(grid):
    '''Return a digest of a grid, independent of rotation, reflection, and position.'''
    total = 0
    transformgrided = [grid, transformgrid(grid, 'rot_90'), transformgrid(grid, 'rot_180'), transformgrid(grid, 'rot_270')]
    transformgrided += [transformgrid(transformgrid(grid, 'flip_x'), 'rot_90'), transformgrid(transformgrid(grid, 'flip_x'), 'rot_180'), transformgrid(transformgrid(grid, 'flip_x'), 'rot_270'), transformgrid(transformgrid(grid, 'flip_x'), 'identity')]
    for x in transformgrided:
        total += calcdigest(x)
    return total
def applyop(grid1, grid2, operation):
    '''Apply an operation to two grids.'''
    grid1 = cleanupgrid(grid1)
    grid2 = cleanupgrid(grid2)
    operations = ['add', 'sub', 'xor']
    operation = operation.lower()
    newgrid = {}
    set1 = {x for x in grid1}
    set2 = {x for x in grid2}
    match operation:
        case 'add':
            set3 = set1 + set2
            newgrid = {x:1 for x in set3}
        case 'sub':
            set3 = set1 - set2
            newgrid = {x:1 for x in set3}
        case 'xor':
            set3 = (set1 - set2) + (set2 - set1)
            newgrid = {x:1 for x in set3}
    return newgrid

    
