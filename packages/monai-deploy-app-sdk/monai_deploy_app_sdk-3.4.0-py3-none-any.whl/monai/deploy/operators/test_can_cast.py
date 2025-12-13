import numpy as np


def create_and_cast_array(larger_than_uint16=False):
    """
    Initializes a 2D float64 NumPy array and attempts to downcast it
    to int16 or float32 if possible.

    Returns:
        numpy.ndarray: The casted array or the original array if no
                       casting was performed.
    """
    # 1. Initialize a 2D numpy array with dtype float64
    # This example contains only positive whole numbers, so it can be cast to uint16.
    # To test the float32 case, change a value to, e.g., 50.5
    info = np.iinfo(np.uint16)
    uint16_max = info.max
    vol_data = np.array([[44000.0, 2000.0], [30000.0, uint16_max]], dtype=np.float64)
    if larger_than_uint16:
        vol_data = vol_data * 2.1
    print(f"Step 1: Initial array created with dtype: {vol_data.dtype}")
    print("Initial array:\n", vol_data)

    if vol_data.dtype == np.uint8 or vol_data.dtype == np.uint16:
        print("Rescaled pixel array is already of type uint8 or uint16.")
    # Check if casting to uint16 and back to float results in the same values.
    elif np.all(vol_data > 0) and np.array_equal(vol_data, vol_data.astype(np.uint16)):
        print("Rescaled pixel array can be safely cast to uint16 with equivalence test.")
        vol_data = vol_data.astype(dtype=np.uint16)
    # Check if casting to int16 and back to float results in the same values.
    elif np.array_equal(vol_data, vol_data.astype(np.int16)):
        print("Rescaled pixel array can be safely cast to int16 with equivalence test.")
        vol_data = vol_data.astype(dtype=np.int16)
    # Check casting to float32 with equivalence test
    elif np.array_equal(vol_data, vol_data.astype(np.float32)):
        print("Rescaled pixel array can be cast to float32 with equivalence test.")
        vol_data = vol_data.astype(np.float32)
    else:
        print("Rescaled pixel data remains as of type float64.")

    return vol_data


if __name__ == "__main__":
    # Execute the flow and get the final array
    final_array = create_and_cast_array()

    # Print the dtype of the new (or original) array
    print(f"\nFinal Step: The dtype of the final array is: {final_array.dtype}")
    print("Final array:\n", final_array)

    # Test with initial array with value larger than uint16
    print("\nNow test with larger array val > uint16 max:\n", final_array)
    final_array = create_and_cast_array(larger_than_uint16=True)

    # Print the dtype of the new (or original) array
    print(f"\nFinal Step: With val larger than uint16, the dtype of the final array is: {final_array.dtype}")
    print("Final array:\n", final_array)
