-- Colors for each cell
data Color = Black | White deriving (Eq, Show)

-- Quadtrees
data Quadtree = Cell Color | Quadrant Quadtree Quadtree Quadtree Quadtree deriving (Eq, Show)

allBlack :: Int -> Quadtree
allBlack _ = Cell Black

allWhite :: Int -> Quadtree
allWhite _ = Cell White

clockwise :: Quadtree -> Quadtree -> Quadtree -> Quadtree -> Quadtree
clockwise = Quadrant

anticlockwise :: Quadtree -> Quadtree -> Quadtree -> Quadtree -> Quadtree
anticlockwise a b c d = Quadrant a d c b


-- New type of quadtree which takes into account its neighbours as a list
data QtWithNeighbors = CellWN Color [Color] | QuadWithN QtWithNeighbors QtWithNeighbors QtWithNeighbors QtWithNeighbors deriving (Eq, Show)

-- Neighbors which stores surrounding Quadtrees of a Quadtree
data Neighbor = Empty | NQuadtree Quadtree 
data Neighbors = Neighbors {
    top :: Neighbor,
    bottom :: Neighbor,
    left :: Neighbor,
    right :: Neighbor
} 

-- Helper functions to get the specific sub-quadtree of a quadtree taking input Neighbor and outputting a Neighbor
getQuadrantA :: Neighbor -> Neighbor
getQuadrantA Empty = Empty
getQuadrantA (NQuadtree (Cell co)) = NQuadtree (Cell co)
getQuadrantA (NQuadtree (Quadrant a b c d)) = NQuadtree a

getQuadrantB :: Neighbor -> Neighbor
getQuadrantB Empty = Empty
getQuadrantB (NQuadtree (Cell co)) = NQuadtree (Cell co)
getQuadrantB (NQuadtree (Quadrant a b c d)) = NQuadtree b

getQuadrantC :: Neighbor -> Neighbor
getQuadrantC Empty = Empty
getQuadrantC (NQuadtree (Cell co)) = NQuadtree (Cell co)
getQuadrantC (NQuadtree (Quadrant a b c d)) = NQuadtree c

getQuadrantD :: Neighbor -> Neighbor
getQuadrantD Empty = Empty
getQuadrantD (NQuadtree (Cell co)) = NQuadtree (Cell co)
getQuadrantD (NQuadtree (Quadrant a b c d)) = NQuadtree d

-- Note:
-- *-----*-----*
-- |  b  |  a  |
-- *-----*-----*
-- |  c  |  d  |
-- *-----*-----*

-- Helper functions to get cells of a quadtree in a given direction like shown in the example above
getTopCells :: Neighbor -> [Color]
getTopCells Empty = []
getTopCells (NQuadtree (Cell co)) = [co]
getTopCells (NQuadtree (Quadrant a b c d)) = getTopCells (NQuadtree b) ++ getTopCells (NQuadtree a)

getBottomCells :: Neighbor -> [Color]
getBottomCells Empty = []
getBottomCells (NQuadtree (Cell co)) = [co]
getBottomCells (NQuadtree (Quadrant a b c d)) = getBottomCells (NQuadtree c) ++ getBottomCells (NQuadtree d)

getLeftCells :: Neighbor -> [Color]
getLeftCells Empty = []
getLeftCells (NQuadtree (Cell co)) = [co]
getLeftCells (NQuadtree (Quadrant a b c d)) = getLeftCells (NQuadtree b) ++ getLeftCells (NQuadtree c)

getRightCells :: Neighbor -> [Color]
getRightCells Empty = []
getRightCells (NQuadtree (Cell co)) = [co]
getRightCells (NQuadtree (Quadrant a b c d)) = getRightCells (NQuadtree a) ++ getRightCells (NQuadtree d)


-- Updating borders of cells using given Neighbors and the quadtree with its Neighbors (recursing from root to leaves)
updateQuadtreeNeighbors :: QtWithNeighbors -> Neighbors -> QtWithNeighbors
updateQuadtreeNeighbors (CellWN co neigs) surrs = CellWN co (neigs ++
        getBottomCells (top surrs) ++
        getTopCells (bottom surrs) ++
        getRightCells (left surrs) ++
        getLeftCells (right surrs) 
    )

updateQuadtreeNeighbors (QuadWithN a b c d) surrs = QuadWithN
    (updateQuadtreeNeighbors a (Neighbors {
        top = getQuadrantD (top surrs),
        bottom = Empty,
        left = Empty,
        right = getQuadrantB (right surrs)
    }))

    (updateQuadtreeNeighbors b (Neighbors {
        top = getQuadrantC (top surrs),
        bottom = Empty,
        left = getQuadrantA (left surrs),
        right = Empty
    }))

    (updateQuadtreeNeighbors c (Neighbors {
        top = Empty,
        bottom = getQuadrantB (bottom surrs),
        left = getQuadrantD (left surrs),
        right = Empty
    }))

    (updateQuadtreeNeighbors d (Neighbors {
        top = Empty,
        bottom = getQuadrantA (bottom surrs),
        left = Empty,
        right = getQuadrantC (right surrs)
    }))


-- Finding neighbors of each cell (from leaves to root)
findQuadtreeNeighbors :: Quadtree -> QtWithNeighbors
findQuadtreeNeighbors (Cell co) = CellWN co []

-- Using surroundings of each level to update neighbors
findQuadtreeNeighbors (Quadrant a b c d) = QuadWithN
    (updateQuadtreeNeighbors (findQuadtreeNeighbors a) (Neighbors {
        top = Empty,
        bottom = NQuadtree d,
        left = NQuadtree b,
        right = Empty
    }))

    (updateQuadtreeNeighbors (findQuadtreeNeighbors b) (Neighbors {
        top = Empty,
        bottom = NQuadtree c,
        left = Empty,
        right = NQuadtree a
    }))

    (updateQuadtreeNeighbors (findQuadtreeNeighbors c) (Neighbors {
        top = NQuadtree b,
        bottom = Empty,
        left = Empty,
        right = NQuadtree d
    }))
    
    (updateQuadtreeNeighbors (findQuadtreeNeighbors d) (Neighbors {
        top = NQuadtree a,
        bottom = Empty,
        left = NQuadtree c,
        right = Empty
    }))

-- Checking if the color needs to be changed based on the colors of neighbors
ifchangeColor :: Color -> [Color] -> Bool
ifchangeColor Black [] = False
ifchangeColor White [] = False
ifchangeColor Black list = countBlack list < countWhite list
ifchangeColor White list = countBlack list > countWhite list

-- Finding number of black cells in the given list of neighbors
countBlack :: [Color] -> Int
countBlack [] = 0
countBlack list = length(filter (== Black) list)

-- Finding number of white cells in the given list of neighbors
countWhite :: [Color] -> Int
countWhite [] = 0
countWhite list = length(filter (== White) list)

-- Reversing the given Color
changeColor :: Color -> Quadtree
changeColor Black = Cell White
changeColor White = Cell Black

-- Helper function for blur
blurhelper :: QtWithNeighbors -> Quadtree
blurhelper (CellWN c l) = if ifchangeColor c l then changeColor c else Cell c
blurhelper (QuadWithN a b c d) = Quadrant (blurhelper a) (blurhelper b) (blurhelper c) (blurhelper d)

-- Blurring a Quadtree as given the requirements
blur :: Quadtree -> Quadtree
blur (Cell a) = Cell a
blur (Quadrant a b c d) = blurhelper(findQuadtreeNeighbors (Quadrant a b c d))
