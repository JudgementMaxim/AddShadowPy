import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from PIL import Image

def add_shadow(input_image_path, output_image_path, file_name, shadow_offset=(10, 10), shadow_opacity=0.5):
    # Load the original image
    original_image = Image.open(input_image_path).convert("RGBA")

    # Create a transparent image with the same size
    shadow_image = Image.new("RGBA", original_image.size, (0, 0, 0, 0))

    # Apply a shadow by offsetting the image
    shadow_offset = (shadow_offset[0], shadow_offset[1])
    shadow_image.paste(original_image, shadow_offset, original_image)

    # Convert the shadow image to NumPy array
    shadow_array = np.array(shadow_image)

    # Extract the alpha channel
    alpha_channel = shadow_array[:, :, 3]

    # Apply the shadow opacity to the alpha channel
    alpha_channel = (alpha_channel * shadow_opacity).astype(np.uint8)

    # Set the color of shadow pixels to black
    shadow_array[:, :, :3] = 0

    # Create a new shadow array with the modified color
    shadow_array[:, :, 3] = alpha_channel

    # Create a new shadow image from the modified array
    shadow_image = Image.fromarray(shadow_array, 'RGBA')

    # Create a mask to keep the non-transparent parts
    mask = original_image.split()[3]

    # Composite the original image and the shadow using the mask
    result_image = Image.alpha_composite(Image.new("RGBA", original_image.size, (0, 0, 0, 0)), shadow_image)
    result_image.paste(original_image, mask=mask)

    # Save the final result to the specified output path with the user-specified file name as PNG
    result_image.save(f"{output_image_path}/{file_name}.png", format="PNG")

def select_input_image():
    file_path = filedialog.askopenfilename(title="Select Input Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, file_path)

def select_output_directory():
    output_directory = filedialog.askdirectory(title="Select Output Directory")
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_directory)

def process_image():
    input_image_path = input_entry.get()
    output_directory = output_entry.get()
    file_name = file_name_entry.get()
    
    if not input_image_path or not output_directory or not file_name:
        messagebox.showerror("Error", "Please provide input image, output directory, and file name.")
        return

    add_shadow(input_image_path, output_directory, file_name)

    messagebox.showinfo("Success", f"Image processed and saved to:\n{output_directory}/{file_name}.png")

# Create the main Tkinter window
root = tk.Tk()
root.title("Image Shadow Adder")
root.geometry("400x400")

# Styling
root.configure(bg="#f0f0f0")
font_style = ("Arial", 12)

# Create and place GUI components
input_label = tk.Label(root, text="Input Image:", font=font_style, bg="#f0f0f0")
input_label.pack(pady=5)

input_entry = tk.Entry(root, width=30, font=font_style)
input_entry.pack(pady=5)

input_button = tk.Button(root, text="Browse", command=select_input_image, font=font_style)
input_button.pack(pady=5)

output_label = tk.Label(root, text="Output Directory:", font=font_style, bg="#f0f0f0")
output_label.pack(pady=5)

output_entry = tk.Entry(root, width=30, font=font_style)
output_entry.pack(pady=5)

output_button = tk.Button(root, text="Browse", command=select_output_directory, font=font_style)
output_button.pack(pady=5)

file_name_label = tk.Label(root, text="File Name:", font=font_style, bg="#f0f0f0")
file_name_label.pack(pady=5)

file_name_entry = tk.Entry(root, width=30, font=font_style)
file_name_entry.pack(pady=5)

process_button = tk.Button(root, text="Process Image", command=process_image, font=font_style, bg="#4CAF50", fg="white")
process_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()