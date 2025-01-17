# LSTM 모델로 랜덤서치 적용

import numpy as np
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential, Model
from keras.layers import Dense, Input, LSTM
from keras.layers import Conv2D, Flatten
from keras.layers import MaxPooling2D, Dropout
from keras.wrappers.scikit_learn import KerasClassifier     # 케라스를 사이킷런으로 감싼다. (사이킷런에서 쓸 수 있게)
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV


# 1. 데이터
(x_train, y_train), (x_test, y_test) = mnist.load_data()
print(x_train.shape)                # (60000, 28, 28)
print(x_test.shape)                 # (10000, 28, 28)
print(y_train.shape)                # (60000,)
print(y_test.shape)                 # (10000,)

# x_train = x_train.reshape(x_train.shape[0], 28, 28, 1) / 255          # 정규화(min_max)
# x_test = x_test.reshape(x_test.shape[0], 28, 28, 1) / 255             # 정규화(min_max)
# x_train = x_train.reshape(x_train.shape[0], 28 * 28) / 255            # 정규화(min_max)
# x_test = x_test.reshape(x_test.shape[0], 28 * 28) / 255               # 정규화(min_max)
# print(x_train.shape)                # (60000, 28, 28, 1)
# print(x_test.shape)                 # (10000, 28, 28, 1)

y_train = np_utils.to_categorical(y_train)      # label이 0부터 시작함
y_test = np_utils.to_categorical(y_test)        # label이 0부터 시작함
print(y_train.shape)                # (60000, 10)
print(y_test.shape)                 # (10000, 10)


# 2. 모델링
def build_model(drop, optimizer, learning_rate):
    inputs = Input(shape = (28, 28), name = 'input')
    x = LSTM(64, activation = 'relu', return_sequences = True, name = 'hidden1')(inputs)
    x = Dropout(drop)(x)
    x = LSTM(32, activation = 'relu', name = 'hidden2')(x)
    x = Dropout(drop)(x)
    x = Dense(16, activation = 'relu', name = 'hidden3')(x)
    x = Dropout(drop)(x)
    outputs = Dense(10, activation = 'softmax', name = 'output')(x)
    model = Model(inputs = inputs, outputs = outputs)
    model.compile(optimizer = optimizer(learning_rate=learning_rate), metrics = ['accuracy'],
                  loss = 'categorical_crossentropy')
    return model
    
from keras.optimizers import Adam, RMSprop, SGD, Adadelta,Adagrad, Nadam, Adamax

def create_hyperparameter():
    batches = [10, 20, 30, 40, 50]
    optimizers = [RMSprop, Adam, Adadelta]
    dropout = np.linspace(0.1, 0.5, 5).tolist()
    learning_rate = np.linspace(0.001, 0.01, 10).tolist()

    return {'batch_size': batches,
            'optimizer': optimizers,
            'drop': dropout,
            'learning_rate':learning_rate}

# KerasClassifier 모델 구성하기
model = KerasClassifier(build_fn = build_model, verbose = 1)

# hyperparameters 변수 정의
hyperparameters = create_hyperparameter()

search = RandomizedSearchCV(estimator = model,
                            param_distributions = hyperparameters, cv = 3)

# 모델 훈련
search.fit(x_train, y_train)
score = search.score(x_test, y_test)
print(search.best_params_)              # {'optimizer': 'adadelta', 'drop': 0.2, 'batch_size': 20}
print("score : ", score)                # 0.9661999940872192

def sum_of_squares(v):
    return sum(v_i**2 for v_i in v)
# 실수 벡터를 입력하면 요소의 제곱으ㅢ 합을 리턴해주는 비용함수

def difference_quotient(f,x,h):
    return (f(x+h) - f(x))/h

# f라는 함수에 대해서 x위치에서의 미분값 즉 기울기를 리턴함
# x가 lr의 역활을 수행 => 최소 기울기를 찾아가자


def partial_difference_quotient(f, v, i, h):
# 함수 f의 i번째 편도함수가 v에서 가지는 값

    w = [v_j + (h if j == i else 0) # h를 v의 i번째 변수에서만 더해주자
        for j, v_j  in enumerate(v)] # 즉 i 번째 변수만 변화할 경우
    
    return (f(w) - f(v))/h

