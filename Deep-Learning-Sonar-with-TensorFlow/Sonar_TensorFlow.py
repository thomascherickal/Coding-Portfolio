# Code from the tutorial TensorFlow Tutorial | Deep Learning Using TensorFlow | Edureka
# Sonar Mines vs Rocks
# https://www.youtube.com/watch?v=yX8KuPZCAMo
# With small corrections and additions of missing parts by Claude COULOMBE - PhD candidate TÉLUQ / UQAM - Montréal
# Many errors - more modifications by @Developer Thomas M. Cherickal

import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

# Reading the dataset
# Get the dataset "sonar.csv" at 
# https://archive.ics.uci.edu/ml/machine-learning-databases/undocumented/connectionist-bench/sonar/sonar.all-data
# Just save the file as sonar.csv
def read_dataset():
    dir_path = ""
    df = pd.read_csv(dir_path+"sonar.csv")
    print("Nbr columns: ",len(df.columns))
    X = df[df.columns[0:60]].values
    y = df[df.columns[60]]
    
    # Encode the dependent variable
    encoder = LabelEncoder()
    encoder.fit(y)
    y = encoder.transform(y)
    Y = one_hot_encode(y)
    print("X.shape",X.shape)
    return (X,Y)

# Define the encoder function M => 1, R => 0
def one_hot_encode(labels):
    n_labels = len(labels)
    n_unique_labels = len(np.unique(labels))
    one_hot_encode = np.zeros((n_labels,n_unique_labels))
    one_hot_encode[np.arange(n_labels),labels] = 1
    return one_hot_encode

# Read the dataset
X, Y = read_dataset()

# Shuffle the dataset to mix up the rows
X, Y = shuffle(X, Y)

# Convert the dataset into train and test datasets
train_x, test_x, train_y, test_y = train_test_split(X, Y, test_size=0.20)

# Inspect the shape of the train and test datasets
print("train_x.shape",train_x.shape)
print("train_y.shape",train_y.shape)
print("test_x.shape",test_x.shape)
print("test_y.shape",test_y.shape)

# Define the hyperparameters
learning_rate = 0.1
training_epochs = 80
cost_history = np.empty(shape=[1], dtype=float)
# Number of features <=> number of columns
n_dim = X.shape[1] 
print("n_dim",n_dim)
n_class = 2
model_path = "C:\\Users\\ADMIN\\OneDrive\\My Projects\\Coding-Portfolio\\Deep Learning Sonar with TensorFlow\\model"

# Define the number of hidden layers and the
# number of neurons for each layer
n_hidden_1 = 120
n_hidden_2 = 120
n_hidden_3 = 120
n_hidden_4 = 120

# Inputs and outputs
x = tf.placeholder(tf.float32,[None, n_dim])
y_ = tf.placeholder(tf.float32,[None, n_class])

# Model parameters
W = tf.Variable(tf.zeros([n_dim,n_class]))
b = tf.Variable(tf.zeros([n_class]))

# Model
def multilayer_perceptron(x, weights, biases):
    # Hidden layer with RELU activations
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)
    # Hidden layer with sigmoid activations
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.sigmoid(layer_2)
    # Hidden layer with sigmoid activations
    layer_3 = tf.add(tf.matmul(layer_2, weights['h3']), biases['b3'])
    layer_3 = tf.nn.sigmoid(layer_3)
    # Hidden layer with sigmoid activations
    layer_4 = tf.add(tf.matmul(layer_3, weights['h4']), biases['b4'])
    layer_4 = tf.nn.sigmoid(layer_4)
    # Output layer with linear activations
    out_layer = tf.matmul(layer_4, weights['out']) + biases['out']
    return out_layer

# define the weights and the biases for each layer

weights = {
    'h1': tf.Variable(tf.truncated_normal([n_dim, n_hidden_1])),
    'h2': tf.Variable(tf.truncated_normal([n_hidden_1, n_hidden_2])),
    'h3': tf.Variable(tf.truncated_normal([n_hidden_2, n_hidden_3])),
    'h4': tf.Variable(tf.truncated_normal([n_hidden_3, n_hidden_4])),
    'out': tf.Variable(tf.truncated_normal([n_hidden_4, n_class])),
    }
biases = {
    'b1': tf.Variable(tf.truncated_normal([n_hidden_1])),
    'b2': tf.Variable(tf.truncated_normal([n_hidden_2])),
    'b3': tf.Variable(tf.truncated_normal([n_hidden_3])),
    'b4': tf.Variable(tf.truncated_normal([n_hidden_4])),
    'out': tf.Variable(tf.truncated_normal([n_class])),
    }

# Initialization
init = tf.global_variables_initializer()
saver = tf.train.Saver()

# Call your model defined
y = multilayer_perceptron(x, weights, biases)

# Define the cost function and optimizer
cost_function = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y, labels=y_))
training_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost_function)

# Launch the graph
sess = tf.Session()
sess.run(init)



# Calculate the cost and the accuracy for each epoch
for epoch in range(training_epochs):
    sess.run(training_step, feed_dict={x:train_x, y_:train_y})
    cost = sess.run(cost_function,feed_dict={x:train_x, y_:train_y})
    
    pred_y = sess.run(y,feed_dict={x:train_x} )
    correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(y_,1))
    train_accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    print("Train Accuracy: ", (sess.run(train_accuracy, feed_dict={x:train_x, y_:train_y})))
    pred_y = sess.run(y,feed_dict={x:test_x} )
    correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(y_,1))
    test_accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    
    print("Test Accuracy: ", (sess.run(test_accuracy, feed_dict={x:test_x, y_:test_y})))
    mse = tf.reduce_mean(tf.square(pred_y - test_y))
    mse_ = sess.run(mse)
    print('epoch: ', epoch,' - ', 'cost: ', cost, " - MSE: ", mse_)
    
save_path = saver.save(sess, model_path)
print("Model saved in file: %s", save_path)

# Print the final mean square error
pred_y = sess.run(y, feed_dict={x:test_x})
mse = tf.reduce_mean(tf.square(pred_y- test_y))
print("MSE: %.4f" % sess.run(mse))