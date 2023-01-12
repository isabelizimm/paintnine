import random
import pandas as pd
from pandas import concat
from math import sqrt
from plotnine import ggplot, aes, geom_polygon, coord_equal, theme_void, theme, element_rect

# code adapted from https://art-from-code.netlify.app/day-1/session-3/

def get_square():
    square = pd.DataFrame(
        {'x': [0, 1, 1, 0, 0],
        'y': [0, 0, 1, 1, 0],
        'seg_len': [1, 1, 1, 1, 0]}
        )
    return square

def sample_edge(polygon: pd.DataFrame):
    return(random.randint(0, len(polygon)-2))

def edge_length(x1, x2, y1, y2):
    return(sqrt((x1-x2)**2 + (y1-y2)**2))

def edge_noise(size):
  return random.uniform(-size/2, size/2)

def insert_edge(polygon, noise):
  
  # sample and edge and remember its length
  ind = sample_edge(polygon)
  edge_len = polygon.seg_len[ind]

  # one endpoint of the old edge
  last_x = polygon.x[ind]
  last_y = polygon.y[ind]
  
  # the other endpoint of the old edge
  next_x = polygon.x[ind + 1]
  next_y = polygon.y[ind + 1]
  
  # location of the new point to be inserted: noise
  new_x = (last_x + next_x) / 2 + edge_noise(edge_len * noise)
  new_y = (last_y + next_y) / 2 + edge_noise(edge_len * noise)
  
  # the new row for insertion
  # containing coords and length of the 'new' edge
  new_row = dict(
    x = [new_x],
    y = [new_y],
    seg_len = [edge_length(new_x, new_y, next_x, next_y)]
  )
  
  # update the length of the 'old' edge
  polygon.seg_len[ind] = edge_length(
    last_x, last_y, new_x, new_y
  )
  
  # insert a row
  if ind != len(polygon)-1:
    new_polygon = concat(
      [polygon.iloc[0:ind],
      pd.DataFrame(new_row),
      polygon.iloc[ind:]]
  ).reset_index(drop=True)
  else:
    new_polygon = concat(polygon, pd.DataFrame(new_row)).reset_index(drop=True)


  return new_polygon

def show_polygon(polygon, show_vertices = True):
  
  pic = (ggplot(polygon, aes('x', 'y')) +
    geom_polygon(colour = "purple", fill = None, show_legend = False) + 
    coord_equal() + 
    theme_void())
  
  if show_vertices:
    pic = pic + geom_point(colour = "white", size = 2)

  return pic

def grow_polygon(polygon, iterations, noise=0.5, seed = None):
    
    if seed:
      random.seed(seed)

    for i in range(1, iterations):
      polygon = insert_edge(polygon, noise)
  
    return polygon

def grow_multipolygon(base_shape, iterations, n, seed = None):
  if seed:
    random.seed(seed)

  polygons = pd.DataFrame(columns=['x', 'y', 'seg_len', 'id'])
  
  for i in range(1, n):
    new = pd.DataFrame(grow_polygon(base_shape, iterations))
    new["id"] = i
    polygons = concat([polygons, new]) 

  return polygons

def show_multipolygon(polygon, fill, alpha = .2, bgd = None):
  pic = (ggplot(polygon, aes('x', 'y', group = 'id')) +
    geom_polygon(colour = None, alpha = alpha, fill = fill) + 
    coord_equal() +
    theme_void()+ 
    theme(rect=element_rect(fill=bgd))
    )

  return pic