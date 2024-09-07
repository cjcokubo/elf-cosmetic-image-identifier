import cv2
from tkinter import *
from PIL import Image, ImageTk
from transformers import CLIPProcessor, CLIPModel

# Initialize the CLIP model
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

cosmetic_descriptions = [
    "elf, Power Grip primer",
    "Dior, lip glow oil",
    "Dior, blush",
    "Colourpop, nude mood eyeshadow palette",
    # Add more descriptions as needed
]

def update_frame():
    # Capture a single frame from the webcam
    ret, frame = cap.read()

    if ret:
        # Convert the image to a format that Tkinter can use
        cv_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=cv_image)
        lbl_img.config(image=imgtk)
        lbl_img.image = imgtk
        # Call update_frame again after a short delay to update the image
        root.after(10, update_frame)

def capture_image(event):
    # Capture a single image from the webcam
    ret, frame = cap.read()
    if ret:
        # Save the captured frame
        cv2.imwrite('captured_image.jpg', frame)

        # Identify the cosmetic product in the captured image
        identified_cosmetic = identify_cosmetic_synchronous('captured_image.jpg')
        # print(f"\033[1;31mIDENTIFIED COSMETIC: {identified_cosmetic['cosmetic'].upper()}, CONFIDENCE: {identified_cosmetic['confidence']:.2f}\033[0m")
        print(
            f"\033[1;33mIDENTIFIED COSMETIC: {identified_cosmetic['cosmetic'].upper()}, CONFIDENCE: {identified_cosmetic['confidence']:.2f}\033[0m")

def identify_cosmetic_synchronous(image_path):
    image = Image.open(image_path)

    # Process the image and descriptions
    inputs = processor(text=cosmetic_descriptions, images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)

    # Get similarity scores
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)

    # Determine the most likely cosmetic
    max_prob_index = probs.argmax().item()
    most_likely_cosmetic = cosmetic_descriptions[max_prob_index]
    confidence = probs[0][max_prob_index].item()

    return {"cosmetic": most_likely_cosmetic, "confidence": confidence}

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Create a Tkinter window
root = Tk()
root.title("Cosmetic Product Identifier")

# Get half of the screen width and height and set it as the window size
screen_width = root.winfo_screenwidth() // 2
screen_height = root.winfo_screenheight() // 2
root.geometry(f"{screen_width}x{screen_height}")

# Add a label to display the webcam feed
lbl_img = Label(root)
lbl_img.pack(side=TOP, fill=BOTH, expand=True)

# Bind any key press to the capture_image function
root.bind('<Key>', capture_image)

# Start updating the frame for real-time display
update_frame()

# Start the Tkinter main loop
root.mainloop()


# DOCU
## Uses CLIP — zero-shot model; little to no training required
### We just have database of brands and product names and it matches it
### Also by OpenAI

## Rewards brands and products with signature packaging and formulations

## Applications are endless: gamification, ingredients list rating, shade and formulation finder