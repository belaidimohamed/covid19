import os
import cv2
from tqdm import tqdm
import numpy as np
import json
from Transform.transforms import Transform
import yaml
#object1 [0,1] , object2 [1,0]

REBUILD_DATA = True
class CreateData:
    def __init__(self,config):
        self.config = config 
        self.img_size = config['image_resolution']
        self.obj1 = config['input_data'][0] #covid [0,1] 
        self.obj2 = config['input_data'][1] #normal [1,0] 
        self.labels = {  self.obj1:1 , self.obj2:0 }
        self.training_data = []
        self.objCount1 = 0
        self.objCount2 = 0
        self.error = 0

    def getMinNumber(self):
        l = []
        for label in self.labels :
            l.append(len([x for x in os.walk(label)][0][2]))
        return min(l)

    def run(self):
        min = self.getMinNumber()
        print(min)
        for label in self.labels :
                print(label)
                paths = [x for x in os.walk(label)][0][2]
                for path in tqdm(paths):
                    # try :
                    img = cv2.imread(os.path.join(label,path))

                    img = Transform({"type":self.config['transforms'] , "image":img}).run()
                    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    # cv2.imshow("name",img)
                    # cv2.waitKey(0)

                    try:
                        img = cv2.resize(img , (self.img_size,self.img_size))
                    except:
                        pass
                    # img = C.contour(img)
                    self.training_data.append([np.array(img, dtype="object"), np.eye(2)[self.labels[label]]])

                    if label == self.obj1 :
                        self.objCount1 +=1
                        if(self.objCount1 > min +20):
                            break
                    elif label == self.obj2 :
                        self.objCount2 += 1
                        if(self.objCount2 > min +200):
                            break
                      
        np.random.shuffle(self.training_data)
        try:
            np.save(os.path.join(self.config['output_folder'][0] , 'training_data#' + self.config['transforms'] + '.npy'),self.training_data)
        except :
            os.mkdir(self.config['output_folder'][0])
            np.save(os.path.join(self.config['output_folder'][0] , 'training_data#' + self.config['transforms'] + '.npy'),self.training_data)

        print('Object 1: ',self.objCount1)
        print('Object 2: ',self.objCount2)
        print('error',self.error)




with open("config.yaml",encoding='utf8') as f:
        config = yaml.safe_load(f)['Create']

create = CreateData(config)
create.run()