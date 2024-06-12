--Colors
data Color = Black | White deriving (Eq, Show)

--QuadTree
data Quadtree = Cell Color | Quadrant Quadtree Quadtree Quadtree Quadtree deriving (Eq, Show)

allBlack :: Int -> Quadtree
allBlack _ = Cell Black

allWhite :: Int -> Quadtree
allWhite _ = Cell White

clockwise :: Quadtree -> Quadtree -> Quadtree -> Quadtree -> Quadtree
clockwise = Quadrant

anticlockwise :: Quadtree -> Quadtree -> Quadtree -> Quadtree -> Quadtree
anticlockwise a b c d = Quadrant a d c b


-- define Quadtree with Neighbours which is represented as a list of cell colors
data QuadtreeWN = CellWN Color [Color] | QuadrantWN QuadtreeWN QuadtreeWN QuadtreeWN QuadtreeWN deriving (Eq, Show)

-- define Surroundings that stores surrounding quadtrees of a quadtree
data Surrounding = Empty | SQuadtree Quadtree 
data Surroundings = Surroundings {
    top :: Surrounding,
    bottom :: Surrounding,
    left :: Surrounding,
    right :: Surrounding
    -- ,
    -- topLeft :: Surrounding,
    -- topRight :: Surrounding,
    -- bottomLeft :: Surrounding,
    -- bottomRight :: Surrounding
} 

-- define helper functions to get the specific sub-quadtree of a quadtree
getQuadrantA :: Surrounding -> Surrounding
getQuadrantA Empty = Empty
getQuadrantA (SQuadtree (Cell co)) = SQuadtree (Cell co)
getQuadrantA (SQuadtree (Quadrant a b c d)) = SQuadtree a

getQuadrantB :: Surrounding -> Surrounding
getQuadrantB Empty = Empty
getQuadrantB (SQuadtree (Cell co)) = SQuadtree (Cell co)
getQuadrantB (SQuadtree (Quadrant a b c d)) = SQuadtree b

getQuadrantC :: Surrounding -> Surrounding
getQuadrantC Empty = Empty
getQuadrantC (SQuadtree (Cell co)) = SQuadtree (Cell co)
getQuadrantC (SQuadtree (Quadrant a b c d)) = SQuadtree c

getQuadrantD :: Surrounding -> Surrounding
getQuadrantD Empty = Empty
getQuadrantD (SQuadtree (Cell co)) = SQuadtree (Cell co)
getQuadrantD (SQuadtree (Quadrant a b c d)) = SQuadtree d
-- Note:
-- *-----*-----*
-- |  d  |  c  |
-- *-----*-----*
-- |  b  |  a  |
-- *-----*-----*
-- define helper functions to get cells of a quadtree in a given direction, e.g. `getTopCells` gives cells that compose the top edge of a quadtree
getTopCells :: Surrounding -> [Color]
getTopCells Empty = []
getTopCells (SQuadtree (Cell co)) = [co]
getTopCells (SQuadtree (Quadrant a b c d)) = getTopCells (SQuadtree b) ++ getTopCells (SQuadtree a)
getBottomCells :: Surrounding -> [Color]
getBottomCells Empty = []
getBottomCells (SQuadtree (Cell co)) = [co]
getBottomCells (SQuadtree (Quadrant a b c d)) = getBottomCells (SQuadtree c) ++ getBottomCells (SQuadtree d)
getLeftCells :: Surrounding -> [Color]
getLeftCells Empty = []
getLeftCells (SQuadtree (Cell co)) = [co]
getLeftCells (SQuadtree (Quadrant a b c d)) = getLeftCells (SQuadtree b) ++ getLeftCells (SQuadtree c)
getRightCells :: Surrounding -> [Color]
getRightCells Empty = []
getRightCells (SQuadtree (Cell co)) = [co]
getRightCells (SQuadtree (Quadrant a b c d)) = getRightCells (SQuadtree a) ++ getRightCells (SQuadtree d)
-- getTopLeftCell :: Surrounding -> [Color]
-- getTopLeftCell Empty = []
-- getTopLeftCell (SQuadtree (Cell co)) = [co]
-- getTopLeftCell (SQuadtree (Quadrant a b c d)) = getTopLeftCell (SQuadtree b)
-- getTopRightCell :: Surrounding -> [Color]
-- getTopRightCell Empty = []
-- getTopRightCell (SQuadtree (Cell co)) = [co]
-- getTopRightCell (SQuadtree (Quadrant a b c d)) = getTopRightCell (SQuadtree a)
-- getBottomLeftCell :: Surrounding -> [Color]
-- getBottomLeftCell Empty = []
-- getBottomLeftCell (SQuadtree (Cell co)) = [co]
-- getBottomLeftCell (SQuadtree (Quadrant a b c d)) = getBottomLeftCell (SQuadtree c)
-- getBottomRightCell :: Surrounding -> [Color]
-- getBottomRightCell Empty = []
-- getBottomRightCell (SQuadtree (Cell co)) = [co]
-- getBottomRightCell (SQuadtree (Quadrant a b c d)) = getBottomRightCell (SQuadtree d)

-- update border cells of given surroundings into neighbour list of each cell (recursion from root to leaves)
updateNeighbours :: QuadtreeWN -> Surroundings -> QuadtreeWN
updateNeighbours (CellWN co neigs) surrs = CellWN co (neigs ++
        getBottomCells (top surrs) ++
        getTopCells (bottom surrs) ++
        getRightCells (left surrs) ++
        getLeftCells (right surrs) 
        -- ++
        -- getBottomRightCell (topLeft surrs) ++
        -- getBottomLeftCell (topRight surrs) ++
        -- getTopRightCell (bottomLeft surrs) ++
        -- getTopLeftCell (bottomRight surrs)
    )

-- pass specific sub-quadtree of given surrounding quadtree to form use sub-Surroundings
updateNeighbours (QuadrantWN a b c d) surrs = QuadrantWN
    (updateNeighbours a (Surroundings {
        top = getQuadrantD (top surrs),
        bottom = Empty,
        left = Empty,
        right = getQuadrantB (right surrs)
        -- ,
        -- topLeft = getQuadrantC (top surrs),
        -- topRight = getQuadrantC (topRight surrs),
        -- bottomLeft = Empty,
        -- bottomRight = getQuadrantC (right surrs)
    }))
    (updateNeighbours b (Surroundings {
        top = getQuadrantC (top surrs),
        bottom = Empty,
        left = getQuadrantA (left surrs),
        right = Empty
        -- ,
        -- topLeft = getQuadrantD (topLeft surrs),
        -- topRight = getQuadrantD (top surrs),
        -- bottomLeft = getQuadrantD (left surrs),
        -- bottomRight = Empty
    }))
    (updateNeighbours c (Surroundings {
        top = Empty,
        bottom = getQuadrantB (bottom surrs),
        left = getQuadrantD (left surrs),
        right = Empty
        -- ,
        -- topLeft = getQuadrantA (left surrs),
        -- topRight = Empty,
        -- bottomLeft = getQuadrantA (bottomLeft surrs),
        -- bottomRight = getQuadrantA (bottom surrs)
    }))
    (updateNeighbours d (Surroundings {
        top = Empty,
        bottom = getQuadrantA (bottom surrs),
        left = Empty,
        right = getQuadrantC (right surrs)
        -- ,
        -- topLeft = Empty,
        -- topRight = getQuadrantB (right surrs),
        -- bottomLeft = getQuadrantB (bottom surrs),
        -- bottomRight = getQuadrantB (bottomRight surrs)
    }))


-- compute neighbour list of each cell (from leaves to root)
computeNeighbours :: Quadtree -> QuadtreeWN
computeNeighbours (Cell co) = CellWN co []

-- pass surroundings at each level to updateNeighbours
computeNeighbours (Quadrant a b c d) = QuadrantWN
    (updateNeighbours (computeNeighbours a) (Surroundings {
        top = Empty,
        bottom = SQuadtree d,
        left = SQuadtree b,
        right = Empty
        -- ,
        -- topLeft = Empty,
        -- topRight = Empty,
        -- bottomLeft = SQuadtree c,
        -- bottomRight = Empty
    }))
    (updateNeighbours (computeNeighbours b) (Surroundings {
        top = Empty,
        bottom = SQuadtree c,
        left = Empty,
        right = SQuadtree a
        -- ,
        -- topLeft = Empty,
        -- topRight = Empty,
        -- bottomLeft = Empty,
        -- bottomRight = SQuadtree d
    }))
    (updateNeighbours (computeNeighbours c) (Surroundings {
        top = SQuadtree b,
        bottom = Empty,
        left = Empty,
        right = SQuadtree d
        -- ,
        -- topLeft = Empty,
        -- topRight = SQuadtree a,
        -- bottomLeft = Empty,
        -- bottomRight = Empty
    }))
    (updateNeighbours (computeNeighbours d) (Surroundings {
        top = SQuadtree a,
        bottom = Empty,
        left = SQuadtree c,
        right = Empty
        -- ,
        -- topLeft = SQuadtree b,
        -- topRight = Empty,
        -- bottomLeft = Empty,
        -- bottomRight = Empty
    }))

ifchangeColor :: Color -> [Color] -> Bool
ifchangeColor Black [] = False
ifchangeColor White [] = False
ifchangeColor Black list = countBlack list < countWhite list
ifchangeColor White list = countBlack list > countWhite list

countBlack :: [Color] -> Int
countBlack [] = 0
countBlack list = length(filter (== Black) list)

countWhite :: [Color] -> Int
countWhite [] = 0
countWhite list = length(filter (== White) list)

changeColor :: Color -> Quadtree
changeColor Black = Cell White
changeColor White = Cell Black

blurhelper :: QuadtreeWN -> Quadtree
blurhelper (CellWN c l) = if ifchangeColor c l then changeColor c else Cell c
blurhelper (QuadrantWN a b c d) = Quadrant (blurhelper a) (blurhelper b) (blurhelper c) (blurhelper d)

blur :: Quadtree -> Quadtree
blur (Cell a) = Cell a
blur (Quadrant a b c d) = blurhelper(computeNeighbours (Quadrant a b c d))

str4_i = let
  c = clockwise
  w = allWhite
  b = allBlack in
   (c(c(b 1)(w 1)(w 1)(b 1))(c(b 1)(w 1)(w 1)(b 1))(c(b 1)(w 1)(w 1)(b 1))(c(b 1)(w 1)(w 1)(b 1)))
str4_o = let
  c = clockwise
  w = allWhite
  b = allBlack in
   (c(c(b 1)(b 1)(w 1)(b 1))(c(w 1)(w 1)(w 1)(b 1))(c(b 1)(w 1)(w 1)(w 1))(c(b 1)(w 1)(b 1)(b 1)))

main = print(blur str4_i)