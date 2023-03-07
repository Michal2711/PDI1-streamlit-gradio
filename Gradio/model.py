import tensorflow as tf

# download model
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# normalization
x_train = x_train / 255.0
x_test = x_test / 255.0

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dense(10, activation="softmax")
])

# compilation
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# training
model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

# model acc
test_loss, test_acc = model.evaluate(x_test, y_test)
print("Test accuracy:", test_acc)

# save model
model.save("mnist_model.h5")
