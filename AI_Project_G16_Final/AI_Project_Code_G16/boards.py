"""
B1 : 4x4

      0    1    2    3
  0 | r1 | 00 | 00 | r2 |
  1 | b1 | r3 | r3 | b2 |
  2 | 00 | b3 | b3 | 00 |
  3 | y1 | 00 | 00 | y2 |
  
"""

b1 = {"blank" : [(1,0),(2,0),(0,2),(3,2),(1,3),(2,3)],
      "red" : {
               1 : [(0,0)],
               2 : [(3,0)],
               3 : [(1,1),(2,1)]
              },
      "blue" : {
               1 : [(0,1)],
               2 : [(3,1)],
               3 : [(1,2),(2,2)]
              },
      "yellow" : {
               1 : [(0,3)],
               2 : [(3,3)]
              },
      "size" : (4,4)
     }

b1_sol = {'blank': [(0, 2), (3, 2), (1, 2), (2, 2), (0, 3), (1, 3)], 
          'red': {1: [], 2: [], 3: [(1, 0), (2, 0), (0, 0), (3, 0)]}, 
          'blue': {1: [], 2: [], 3: [(1, 1), (2, 1), (0, 1), (3, 1)]}, 
          'yellow': {1: [(2, 3), (3, 3)], 2: []},
          'size' : (4,4)
          }

"""
B2 : 4x4

      0    1    2    3
  0 | r1 | r1 | g1 | b1 |
  1 | 00 | r1 | 00 | g2 |
  2 | 00 | r1 | b2 | 00 |
  3 | r1 | r1 | g3 | b3 |
  
"""

b2 = {"blank" : [(0,1),(0,2),(2,1),(3,2)],
      "red" : {
               1 : [(0,0),(1,0),(1,1),(1,2),(1,3),(0,3)]
              },
      "blue" : {
               1 : [(3,0)],
               2 : [(2,2)],
               3 : [(3,3)]
              },
      "green" : {
               1 : [(2,0)],
               2 : [(3,1)],
               3 : [(2,3)]
              },
      "size" : (4,4)
     }


"""
B3 : 4x4

      0    1    2    3
  0 | o1 | o1 | r1 | 00 |
  1 | 00 | r2 | o2 | o2 |
  2 | o3 | o3 | r3 | 00 |
  3 | 00 | 00 | o4 | o4 |

"""

b3 = {"blank" : [(3,0),(0,1),(3,2),(0,3),(1,3)],
      "red" : {
               1 : [(2,0)],
               2 : [(1,1)],
               3 : [(2,2)]
              },
      "orange" : {
               1 : [(0,0),(1,0)],
               2 : [(2,1),(3,1)],
               3 : [(0,2),(1,2)],
               4 : [(2,3),(3,3)]
               },
      "size" : (4,4)
     }

b3_sol = {'blank': [(1, 2), (0, 0), (1, 0), (2, 0), (3, 0)], 
          'red': {1: [(1, 1), (0, 1), (0, 2)], 2: [], 3: []}, 
          'orange': {1: [(2, 1), (3, 1), (2, 2), (3, 2), (2, 3), (3, 3), (1, 3), (0, 3)], 2: [], 3: [], 4: []}, 
          'size': (4, 4)}

"""
B4 : 4x4

      0    1    2    3
  0 | 00 | o1 | o1 | 00 |
  1 | 00 | b1 | b1 | 00 |
  2 | 00 | o2 | o2 | 00 |
  3 | r1 | b2 | b2 | g1 |

"""

#This board is not solvable by my algorithms since it can get stuck in infinity 

b4 = {"blank" : [(0,0),(0,1),(0,2),(3,0),(3,1),(3,2)],
      "red" : {
               1 : [(0,3)]
              },
      "orange" : {
               1 : [(1,0),(2,0)],
               2 : [(1,2),(2,2)]
               },
      "blue" : {
                1 : [(1,1),(2,1)],
                2 : [(1,3),(2,3)]
                },
      "green" : {
                1 : [(3,3)]
                },     
      "size" : (4,4)
     }

"""
B5 : 4x4

      0    1    2    3
  0 | 00 | 00 | 00 | b1 |
  1 | r1 | g1 | g1 | b1 |
  2 | r1 | r1 | g1 | g1 |
  3 | b2 | b2 | 00 | 00 |

"""

b5 = {"blank" : [(0,0),(1,0),(2,0),(2,3),(3,3)],
      "red" : {
               1 : [(0,1),(0,2),(1,2)]
              },
      "blue" : {
                1 : [(3,0),(3,1)],
                2 : [(0,3),(1,3)]
                },
      "green" : {
                1 : [(1,1),(2,1),(2,2),(3,2)]
                },     
      "size" : (4,4)
     }

"""
B6 : 4x4

      0    1    2    3
  0 | 00 | b1 | r1 | r1 |
  1 | r2 | r2 | 00 | b1 |
  2 | 00 | o1 | b1 | b1 |
  3 | o2 | 00 | b1 | b1 |

"""

b6 = {"blank" : [(0,0),(2,1),(0,2),(1,3)],
      "red" : {
               1 : [(2,0),(3,0)],
               2 : [(0,1),(1,1)]
              },
      "blue" : {
                1 : [(1,0)],
                2 : [(3,1),(3,2),(3,3),(2,2),(2,3)]
                },
      "orange" : {
                1 : [(1,2)],
                2 : [(0,3)]
              },   
      "size" : (4,4)
     }

b6_sol = {'blank': [(1, 0), (0, 0), (0, 1), (0, 2)], 
          'red': {1: [], 2: [(1, 1), (2, 1), (2, 0), (3, 0)]}, 
          'blue': {1: [(1, 2), (2, 2), (3, 2), (2, 3), (3, 1), (3, 3)], 2: []}, 
          'orange': {1: [(1, 3), (0, 3)], 2: []}, 
          'size': (4, 4)}


b7 = {"blank" : [(0,0),(1,0),(2,0),(2,3),(3,3)],
      "red" : {
               1 : [(0,1),(0,2),(1,2)]
              },
      "blue" : {
                1 : [(3,0),(3,1)],
                2 : [(0,3),(1,3)]
                },
      "green" : {
                1 : [(1,1),(2,1),(2,2),(3,2)]
              },   
      "size" : (4,4)
     }

b7_sol = {"blank" : [(0,0),(1,0),(2,0),(3,0),(2,1)],
      "red" : {
               1 : [(0,2),(0,3),(1,3)]
              },
      "blue" : {
                1 : [(3,1),(3,2),(2,3),(3,3)],
                2 : []
                },
      "green" : {
                1 : [(0,1),(1,1),(1,2),(2,2)]
                },     
      "size" : (4,4)
     }