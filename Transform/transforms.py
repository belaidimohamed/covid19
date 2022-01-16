from Transform.waterShed import watershed
from skimage.morphology import skeletonize

# read an image as input using OpenCV
class Transform():
  def __init__(self,info):
    self.info = info
  def run(self):
    if self.info['type'] == 'normal':
      return self.info['image']
    if self.info['type'] == 'watershed':
      return watershed(self.info['image'])
    if self.info['type'] == 'skeleton':
      return  skeletonize(self.info['image'])
