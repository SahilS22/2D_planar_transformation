from tkinter import Tk, Button, Label, Entry, StringVar, Frame, messagebox, OptionMenu, DoubleVar, Canvas
import numpy as np
import matplotlib.pyplot as plt

# Transformation Functions
def translation(points, tx, ty):
    T = np.array([[1, 0, tx],
                  [0, 1, ty],
                  [0, 0, 1]])
    return np.dot(T, points)

def euclidean(points, angle_deg, tx, ty):
    angle_rad = np.radians(angle_deg)
    R = np.array([[np.cos(angle_rad), -np.sin(angle_rad), tx],
                  [np.sin(angle_rad), np.cos(angle_rad), ty],
                  [0, 0, 1]])
    return np.dot(R, points)

def similarity(points, scale, angle_deg, tx, ty):
    angle_rad = np.radians(angle_deg)
    S = np.array([[scale * np.cos(angle_rad), -scale * np.sin(angle_rad), tx],
                  [scale * np.sin(angle_rad), scale * np.cos(angle_rad), ty],
                  [0, 0, 1]])
    return np.dot(S, points)

def affine(points, a, b, c, d, tx, ty):
    A = np.array([[a, b, tx],
                  [c, d, ty],
                  [0, 0, 1]])
    return np.dot(A, points)


# Create Geometry (Square)
def create_square():
    return np.array([[0, 1, 1, 0, 0],
                     [0, 0, 1, 1, 0],
                     [1, 1, 1, 1, 1]])  # Homogeneous coordinates

# Plot Results
def plot_transform(original, transformed, transformation_name):
    plt.figure(figsize=(8, 8))
    plt.plot(original[0, :], original[1, :], label="Original Shape", linestyle='--', marker='o')
    plt.plot(transformed[0, :], transformed[1, :], label="Transformed Shape", linestyle='-', marker='o')
    plt.legend()
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"2D Planar Transformation: {transformation_name}")
    plt.grid(True)
    plt.show()

# GUI Application
def apply_transformation():
    try:
        tx = tx_var.get()
        ty = ty_var.get()
        angle = angle_var.get()
        scale = scale_var.get()
        a, b, c, d = a_var.get(), b_var.get(), c_var.get(), d_var.get()
        transformation = transformation_type.get()

        square = create_square()
        if transformation == "Translation":
            result = translation(square, tx, ty)
        elif transformation == "Euclidean":
            result = euclidean(square, angle, tx, ty)
        elif transformation == "Similarity":
            result = similarity(square, scale, angle, tx, ty)
        elif transformation == "Affine":
            result = affine(square, a, b, c, d, tx, ty)
        else:
            messagebox.showerror("Error", "Select a valid transformation")
            return

        plot_transform(square, result, transformation)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values!")

# Reset all input fields
def reset_inputs():
    tx_var.set(0)
    ty_var.set(0)
    angle_var.set(0)
    scale_var.set(1)
    a_var.set(1)
    b_var.set(0)
    c_var.set(0)
    d_var.set(1)
    transformation_type.set("Translation")

# Main Application Window
root = Tk()
root.title("2D Planar Transformations Simulator")
root.geometry("600x500")

# Variables
transformation_type = StringVar(value="Translation")
tx_var = DoubleVar(value=0)
ty_var = DoubleVar(value=0)
angle_var = DoubleVar(value=0)
scale_var = DoubleVar(value=1)
a_var = DoubleVar(value=1)
b_var = DoubleVar(value=0)
c_var = DoubleVar(value=0)
d_var = DoubleVar(value=1)

# Transformation Selection
frame_transform = Frame(root, padx=10, pady=10)
frame_transform.pack(pady=10)

Label(frame_transform, text="Select Transformation:").grid(row=0, column=0, sticky="w")
OptionMenu(frame_transform, transformation_type, "Translation", "Euclidean", "Similarity", "Affine").grid(row=0, column=1)

# Input Section
frame_inputs = Frame(root, padx=10, pady=10)
frame_inputs.pack(pady=10)

Label(frame_inputs, text="Translation (tx, ty):").grid(row=0, column=0, sticky="w")
Entry(frame_inputs, textvariable=tx_var).grid(row=0, column=1)
Entry(frame_inputs, textvariable=ty_var).grid(row=0, column=2)

Label(frame_inputs, text="Rotation Angle (degrees):").grid(row=1, column=0, sticky="w")
Entry(frame_inputs, textvariable=angle_var).grid(row=1, column=1)

Label(frame_inputs, text="Scale:").grid(row=2, column=0, sticky="w")
Entry(frame_inputs, textvariable=scale_var).grid(row=2, column=1)

Label(frame_inputs, text="Affine Params (a, b, c, d):").grid(row=3, column=0, sticky="w")
Entry(frame_inputs, textvariable=a_var).grid(row=3, column=1)
Entry(frame_inputs, textvariable=b_var).grid(row=3, column=2)
Entry(frame_inputs, textvariable=c_var).grid(row=4, column=1)
Entry(frame_inputs, textvariable=d_var).grid(row=4, column=2)

# Buttons
frame_buttons = Frame(root, padx=10, pady=10)
frame_buttons.pack(pady=10)

Button(frame_buttons, text="Apply Transformation", command=apply_transformation).grid(row=0, column=0, padx=5)
Button(frame_buttons, text="Reset", command=reset_inputs).grid(row=0, column=1, padx=5)

root.mainloop()
