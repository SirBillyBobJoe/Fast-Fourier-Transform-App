# Import necessary libraries
import cv2  # OpenCV for image processing
import numpy as np  # NumPy for numerical operations
import tkinter as tk  # Tkinter for GUI
from tkinter import filedialog  # File dialog for opening images
from PIL import Image, ImageTk  # Pillow library for image manipulation and conversion

# Define the ImageApp class
class ImageApp:
    # Constructor for the ImageApp class
    def __init__(self, root):
        self.root = root  # Store the reference to the root window
        self.root.title("Image FFT App")  # Set the title of the main window

        # Create buttons and canvas for the main window
        self.create_widgets()

    # Method to create and configure the widgets
    def create_widgets(self):
        # Create the Load Image button and set its command to self.load_image
        load_button = tk.Button(self.root, text="Load Image", command=self.load_image)
        load_button.pack(side=tk.TOP, pady=10)  # Add the button to the top of the window with padding

        # Create the canvas for displaying images
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(side=tk.TOP, pady=10)  # Add the canvas to the top of the window with padding

    # Method to open a file dialog and load an image
    def load_image(self):
        # Open a file dialog to select an image file
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])

        if file_path:
            # Read the image using OpenCV in grayscale mode
            self.original_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

            # Perform Fast Fourier Transform on the image
            self.fft_image = self.perform_fft(self.original_image)

            # Display both the original and FFT images on the canvas
            self.display_images()

    # Method to perform Fast Fourier Transform on an image
    def perform_fft(self, image):
        f = np.fft.fft2(image)  # Perform 2D FFT on the input image
        fshift = np.fft.fftshift(f)  # Shift the zero-frequency component to the center of the spectrum
        magnitude_spectrum = 20 * np.log(np.abs(fshift))  # Compute the magnitude spectrum

        # Scale the FFT image for display purposes as the original values might have 
        # a very large range that cannot be represented directly as pixel intensities.
        magnitude_spectrum = (magnitude_spectrum - np.min(magnitude_spectrum)) / (np.max(magnitude_spectrum) - np.min(magnitude_spectrum)) * 255

        return magnitude_spectrum  

    # Method to display the original and FFT images side by side on the canvas
    def display_images(self):
        self.canvas.delete("all")  # Clear the canvas

        # Define the box dimensions to display the 2 images in
        box_width = 500
        box_height = 500

        # Calculate scaling factors for width and height
        scale_width = box_width / (2 * self.original_image.shape[1])
        scale_height = box_height / self.original_image.shape[0]
        scale_factor = min(scale_width, scale_height)

        # Calculate the resized dimensions for the images
        new_width = int(self.original_image.shape[1] * scale_factor)
        new_height = int(self.original_image.shape[0] * scale_factor)

        # Resize the canvas according to the new dimensions
        #times 2 because we have 2 images putting side by side
        self.canvas.config(width=new_width * 2, height=new_height)

        # Convert and resize the original image for display
        # converts the NumPy array to a image object.
        original_pil_image = Image.fromarray(self.original_image)
        original_resized = original_pil_image.resize((new_width, new_height), Image.ANTIALIAS)
        #converts to a format that is compatible with Tkinter for display on the canvas. 
        self.original_photo = ImageTk.PhotoImage(original_resized)

        # Display the resized original image on the left side of the canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.original_photo)

        # Normalize the FFT image to the range [0, 255]
        fft_normalized = cv2.normalize(self.fft_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

        # Convert and resize the FFT image for display
        fft_pil_image = Image.fromarray(fft_normalized)
        fft_resized = fft_pil_image.resize((new_width, new_height), Image.ANTIALIAS)
        self.fft_photo = ImageTk.PhotoImage(fft_resized)

        # Display the resized FFT image on the right side of the canvas
        self.canvas.create_image(new_width, 0, anchor=tk.NW, image=self.fft_photo)




# checks if the script is being run as the main module and if it is run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
