
# 과적합 피하기 2
# Dropout



# 과적합 잡는법

# 훈련 데이터를 늘린다.
# 피처수를 늘린다.
# Regularizer를 사용한다.

'''
L1규제 : 가중치의 절대값 합
regularizer.l1(l=0.01)

L2규제: 가중치의 제곱 합
regularizer.l2(l=0.01)

loss = L1 * reduce_sum(abs(x)) #abs 절댓값
loss = L2 * reduce_sum(abs(x)) 

'''

import numpy as np
import matplotlib.pyplot as plt
from   keras.datasets  import cifar10
from   keras.layers    import Conv2D, Dropout, Input, MaxPooling2D, Flatten, Dense, BatchNormalization, Activation
from   keras.models    import Sequential, Model
from   keras.utils     import np_utils
from   keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard
from keras.optimizers import Adam

from keras.regularizers import l1, l2, l1_l2

(x_train, y_train), (x_test, y_test) = cifar10.load_data()

print('x_train :',x_train.shape)
print('x_test :',x_test.shape)
print('y_train :',y_train.shape)
print('y_test :',y_test.shape)

#1. 데이터 전처리
# y_train = np_utils.to_categorical(y_train)
# y_test  = np_utils.to_categorical(y_test)

# print('x_train :',x_train.shape)
# print('x_test :',x_test.shape)
print('y_train :',y_train.shape)
print('y_test :',y_test.shape)

#2. 데이터 정규화
x_train = x_train/255
x_test  = x_test/255

print('x_train :',x_train.shape)
print('x_test :',x_test.shape)

#.3 모델구성

model = Sequential()

model.add(Conv2D(32, kernel_size=3, padding='same', activation='elu', input_shape=(32,32,3)))
model.add(BatchNormalization())
model.add(Conv2D(32, kernel_size=3, padding='same', activation='elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2), strides=2, padding='same'))

model.add(Conv2D(64, kernel_size=3, padding='same', activation='elu' ))
model.add(BatchNormalization())
model.add(Conv2D(64, kernel_size=3, padding='same', activation='elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2), strides=2, padding='same'))

model.add(Conv2D(128, kernel_size=3, padding='same', activation='elu'))
model.add(BatchNormalization())
model.add(Conv2D(128, kernel_size=3, padding='same', activation='elu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2), strides=2, padding='same'))

model.add(Flatten())
model.add(Dense(256, activation='elu'))
model.add(BatchNormalization())

model.add(Dense(10, activation='softmax'))


model.summary()

model.compile(optimizer=Adam(1e-4), loss='sparse_categorical_crossentropy', metrics=['acc']) #0.0001


#.4 모델 훈련
# tb            = TensorBoard(log_dir='graph', histogram_freq=0, write_graph=True, write_images=True)
# es            = EarlyStopping(monitor='acc', patience=5, mode='auto')
# modelpath     = './model/{epoch:02d}-{val_acc:.4f}.hdf5'
# cp            = ModelCheckpoint(filepath=modelpath, monitor='val_acc', save_best_only=True, mode='auto')
# model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])
hist          = model.fit(x_train, y_train, validation_split=0.2, epochs=20, batch_size=32, verbose=1)#, callbacks=[es,cp,tb])
# D:\Study\study\graph>cd tensorboard --logdir=.(텐서보드 확인 cmd에서)

#.5 평가 예측
loss,acc = model.evaluate(x_test, y_test)



print('loss : ', loss)
print('acc : ',acc)


loss_acc = loss,acc


loss     = hist.history['loss']
acc      = hist.history['acc']
val_loss = hist.history['val_loss']
val_acc  = hist.history['val_acc']

# print('acc : ', acc)
# print('val_acc : ', val_acc)
# print('loss_acc : ', loss_acc)

# 그래프 사이즈
plt.figure(figsize=(10, 6))

# loss 그래프
plt.subplot(2, 1, 1) 
plt.plot(hist.history['loss'],     marker='.', c='red',  label='loss')  
plt.plot(hist.history['val_loss'], marker='.', c='blue', label='val_loss') 
plt.grid() 
plt.title('loss')       
plt.ylabel('loss')       
plt.xlabel('epoch')         
plt.legend(loc = 'upper right')

# acc 그래프
plt.subplot(2, 1, 2) 
plt.plot(hist.history['acc'],     marker='.', c='red',  label='acc')  
plt.plot(hist.history['val_acc'], marker='.', c='blue', label='val_acc') 
plt.grid() 
plt.title('acc')     
plt.ylabel('acc')        
plt.xlabel('epoch')           
plt.legend(loc = 'upper right')  
plt.show()


y_pre  = model.predict(x_test)

y_pre  = np.argmax(y_pre,axis=-1)
y_test = np.argmax(y_test,axis=-1)

print(f"y_test[0:20]:{y_test[0:20]}")
print(f"y_pre[0:20]:{y_pre[0:20]}")
'''
BatchNormalization은 activation적용 이전에 사용하는것이 목적



'''