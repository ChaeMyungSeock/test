from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential, Model
from keras.layers import Input, Dropout, Conv2D, MaxPool2D, Flatten, Dense
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.utils.testing import all_estimators
from sklearn.model_selection import train_test_split,KFold, cross_val_score, cross_val_predict


# 1. 데이터
(x_train, y_train),(x_test, y_test) = mnist.load_data()

print(x_train.shape)

x_train = x_train.reshape(x_train.shape[0],28,28,1)/255
x_test = x_test.reshape(x_test.shape[0],28,28,1)/255

y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)


# 2. 모델
def build_model(drop = 0.5, optimizer = 'adam'):
    inputs = Input(shape=(28,28,1), name = 'input1')
    x = Conv2D(256, kernel_size = (2,2), strides = (2,2), padding = 'same', activation='relu', name = 'hidden1')(inputs)
    x = Dropout(drop)(x)
    x = Conv2D(128, kernel_size = (2,2), strides = (2,2), padding = 'same',  name = 'hidden2')(x)
    x = Dropout(drop)(x)
    x = Conv2D(64, kernel_size = (2,2), strides = (2,2), padding = 'same',  name = 'hidden3')(x)
    x = Dropout(drop)(x)
    x = Flatten()(x)
    outputs = Dense(10, activation='softmax', name = 'outputs')(x)
    model = Model(inputs = inputs, outputs = outputs)
    model.compile(optimizer=optimizer, metrics=['acc'], loss = 'categorical_crossentropy')
    return model

def create_hyperparameter():
    batches = [10, 20, 30, 40 ,50]
    optimizer = ['rmsprop', 'adam', 'adadelta']
    dropout = np.linspace(0.1,0.5,5)
    return{"batch_size" : batches, "optimizer" : optimizer, "drop" : dropout}


from keras.wrappers.scikit_learn import KerasClassifier, KerasRegressor
# wrappers 싸다 

model = KerasClassifier(build_fn=build_model, verbose=1 )

hyperparameters = create_hyperparameter()

from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
search = RandomizedSearchCV(model, hyperparameters, cv=3)
search.fit(x_train,y_train)

print(search.best_params_)

print("최적의 매개변수 : ", int(search.best_estimator_))

y_pred = search.predict(x_test)
# print("최종 정답률 = ", accuracy_score(y_test, y_pred))
# scores = cross_val_score(model, x,y, cv=kfold)
score = search.score(x_test,y_test)
print(score)
