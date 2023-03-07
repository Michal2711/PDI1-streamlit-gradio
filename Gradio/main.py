import tensorflow as tf
import gradio as gr

# pretrained model
model = tf.keras.models.load_model('mnist_model.h5')


def predict_image(image):
    image = tf.cast(image, tf.float32)
    image = tf.reshape(image, (1, 28, 28))

    prediction = model.predict(image)

    return int(tf.argmax(prediction, axis=1))


# Gradio interface
interface = gr.Interface(fn=predict_image, inputs="sketchpad", outputs="number")

if __name__ == "__main__":
    interface.launch(share=True)
