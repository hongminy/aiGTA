import numpy  as np
import pandas as pd
import cv2
from collections import Counter
from random      import shuffle



train_data = np.load('training_data.npy')

df = pd.DataFrame(train_data)
print(len(train_data))
print(df.head())
print(Counter(df[1].apply(str)))
#balance data to avoid overwholming number of 'w'

lefts = []
rights = []
forwards = []

shuffle(train_data)
#every frame is independent so shuffle the data to
#get rid of the linearnality

for data in train_data:
    img = data[0]
    choice = data[1]

    if choice == [1,0,0]:
        lefts.append([img, choice])
    elif choice == [0,1,0]:
        forwards.append([img, choice])
    elif choice == [0,0,1]:
        rights.append([img, choice])
    else:
        print("no match")

forwards = forwards[:len(lefts)][:len(rights)]
lefts = lefts[:len(forwards)]
rights = rights[:len(rights)]

final_data = forwards + lefts + rights

shuffle(final_data)

print(len(final_data))

np.save("training_data_v2.npy",final_data)




'''
for data in train_data:
    img = data[0]
    print(img.shape)
    choice = data[1]
    cv2.imshow('test',img)
    print(choice)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
        '''
    
