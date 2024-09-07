import cv2
from tkinter import *
from PIL import Image, ImageTk
from transformers import CLIPProcessor, CLIPModel

# Initialize the CLIP model
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Descriptions of cosmetic products
cosmetic_descriptions = [
    "elf, Power Grip primer",
    "Dior, lip glow oil",
    "Dior, blush",
    "Colourpop, nude mood eyeshadow palette",
    # Add more descriptions as needed
]

def update_frame():
    """Continuously captures and displays webcam frames."""
    ret, frame = cap.read()
    if ret:
        cv_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=cv_image)
        lbl_img.config(image=imgtk)
        lbl_img.image = imgtk
        root.after(10, update_frame)

def capture_image(event):
    """Captures an image from the webcam and identifies the cosmetic product."""
    ret, frame = cap.read()
    if ret:
        image_path = 'captured_image.jpg'
        cv2.imwrite(image_path, frame)

        identified_cosmetic = identify_cosmetic_synchronous(image_path)
        print(f"\033[1;33mIDENTIFIED COSMETIC: {identified_cosmetic['cosmetic'].upper()}, "
              f"CONFIDENCE: {identified_cosmetic['confidence']:.2f}\033[0m")

def identify_cosmetic_synchronous(image_path):
    """Identifies the cosmetic product in the image using the CLIP model."""
    image = Image.open(image_path)

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

# Create and configure the Tkinter window
root = Tk()
root.title("Cosmetic Product Identifier")
root.geometry(f"{root.winfo_screenwidth() // 2}x{root.winfo_screenheight() // 2}")

# Add a label to display the webcam feed
lbl_img = Label(root)
lbl_img.pack(side=TOP, fill=BOTH, expand=True)

# Bind key press to the capture_image function
root.bind('<Key>', capture_image)

# Start the real-time frame update
update_frame()

# Start the Tkinter main loop
root.mainloop()
