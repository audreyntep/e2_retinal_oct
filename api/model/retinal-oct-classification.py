import numpy as np
from tensorflow import keras


# It can be used to reconstruct the model identically.
reconstructed_model = keras.models.load_model("retinal-oct.h5")

# Let's check:
np.testing.assert_allclose(
    model.predict(test_generator), 
    reconstructed_model.predict(test_generator)
)
# The reconstructed model is already compiled and has retained the optimizer
# state, so training can resume:
reconstructed_model.fit(test_input, test_target)