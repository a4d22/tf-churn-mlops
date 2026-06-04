import tensorflow as tf
from src.train import build_model

def test_model_output_shape():
    model = build_model()
    
    # Create a dummy input data mimicing 5 customers, each with 10 input features
    input_data = tf.random.normal(shape=(5, 10))
    
    # PAss data through the model
    output = model(input_data)
    
    # Write assert statement  to verify the output shape (5,1)
    assert output.shape == (5, 1)
    