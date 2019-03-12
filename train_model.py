# train_model.py

import numpy as np
from alexnet import alexnet

Width = 80
Height = 60


LR = 1e-3
EPOCHS = 8
modelName = 'aiGTA-car-()-()-()-epochs.model'.format(LR, 'alexnetmodified', EPOCHS)

model = alexnet(Width, Height, LR)

train_data = np.load('training_data.npy')

train = train_data[:-500]

test = train_data[-500:]
# half training and half testing

X = np.array([i[0] for i in train]).reshape(-1, Width, Height, 1)
Y = [i[1] for i in train]

test_x = np.array([i[0] for i in test]).reshape(-1, Width, Height, 1)
test_y = [i[1] for i in test]

model.fit({'input':X}, {'targets':Y}, n_epoch=EPOCHS,
          validation_set = ({'input':test_x}, {'targets': test_y}),
          snapshot_step = 500, show_metric=True, run_id = modelName)


# tensorboard --logdir=foo:C:/Users/.../log {path to log}

model.save(modelName)
