import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import time
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import vlc





# Create a list to store the selected images
selected_images = []
current_image_index = 0

# Turning off the failsafe
pyautogui.FAILSAFE = False

# Define a cooldown variable for presentation control
presentationCooldown = 5  # Adjust the value as needed (in frames)

# Initialize the cooldown counter
cooldownCounter = 0

# Initialize initial hand position
initial_hand_x = 0
initial_hand_y = 0


class VideoPlayer:
    def __init__(self, parent):
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()

        self.init_ui(parent)

    def init_ui(self, parent):

        self.video_widget = tk.Label(parent)
        self.video_widget.grid(row=0, column=1, columnspan=6, padx=10, pady=10, sticky="nsew")  # Adjusted columnspan
        self.slider = tk.Scale(parent, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_position)
        self.slider.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")  # Adjusted column and columnspan
        self.play_button = tk.Button(parent, text="Play", command=self.play)
        self.play_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")  # No change
        self.pause_button = tk.Button(parent, text="Pause", command=self.pause)
        self.pause_button.grid(row=1, column=2, padx=5, pady=5, sticky="ew")  # No change
        self.stop_button = tk.Button(parent, text="Stop", command=self.stop)
        self.stop_button.grid(row=1, column=3, padx=5, pady=5, sticky="ew")  # No change
        self.backward_button = tk.Button(parent, text="Backward", command=self.backward)
        self.backward_button.grid(row=1, column=4, padx=5, pady=5, sticky="ew")  # No change
        self.forward_button = tk.Button(parent, text="Forward", command=self.forward)
        self.forward_button.grid(row=1, column=5, padx=5, pady=5, sticky="ew")  # No change

    def choose_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mkv")])
        if file_path:
            self.media = self.instance.media_new(file_path)  # Change this line
            self.media_player.set_media(self.media)  # And this line
            self.media_player.set_hwnd(self.video_widget.winfo_id())  # Set the window ID for the video to play in the video widget

    def play(self):
        if not self.media_player.is_playing():
            self.media_player.play()

    def pause(self):
        if self.media_player.is_playing():
            self.media_player.pause()

    def stop(self):
        self.media_player.stop()

    def forward(self):
        position = self.media_player.get_position()
        self.media_player.set_position(position + 0.1)

    def backward(self):
        position = self.media_player.get_position()
        self.media_player.set_position(position - 0.1)

    def set_position(self, position):
        self.media_player.set_position(float(position) / 100.0)

    def close(self):
        # Stop the media player
        self.media_player.stop()
        # Release the media player
        self.media_player.release()
        self.media_player = None
        # Release the media
        self.media.release()  # This line should work now
        self.media = None
        # Release the instance
        self.instance = None
        self.video_widget.grid_remove()
        self.play_button.grid_remove()
        self.pause_button.grid_remove()
        self.stop_button.grid_remove()
        self.forward_button.grid_remove()
        self.backward_button.grid_remove()
        self.slider.grid_remove()
        


def open_video_file():
    image_option.pack_forget()
    player = VideoPlayer(root)
    player.choose_file()


def open_file():
    file_paths = filedialog.askopenfilenames()
    if file_paths:
        for file_path in file_paths:
            image = Image.open(file_path)
            image.thumbnail((900, 700))
            selected_images.append(ImageTk.PhotoImage(image))
        show_image(current_image_index)


def show_image(index):
    if 0 <= index < len(selected_images):
        image_option.config(image=selected_images[index])
        image_option.image = selected_images[index]


def next_image():
    global current_image_index
    if current_image_index < len(selected_images) - 1:
        current_image_index += 1
        show_image(current_image_index)


def prev_image():
    global current_image_index
    if current_image_index > 0:
        current_image_index -= 1
        show_image(current_image_index)


def create_player():
    player = VideoPlayer(root)
    player.choose_file()

def show_image_option():
    # Show the image option widget when the image button is clicked
    global image_in_view, video_is_playing
    video_is_playing = False
    image_in_view = True
    global player
    if player is not None:
        player.close()
        player = None
    video_option.grid_remove()
    image_option.grid()
    open_file()

def show_video_option():
    global image_in_view, video_is_playing
    image_in_view = False
    global player
    # Show the video option widget when the video button is clicked
    image_option.grid_remove()
    player = VideoPlayer(root)
    player.choose_file()
    player.play()
    video_is_playing = True
    

def close_option():
    global player, image_in_view, video_is_playing
    video_is_playing = False
    image_in_view = False
    image_option.grid_remove()
    # If there is a video player, stop it and destroy it
    if player is not None:
        player.close()
        player = None

# Camera Setup
width, height = 440, 280  # Set the desired camera feed resolution
cap = cv2.VideoCapture(0)

detector = HandDetector(detectionCon=0.8)

# Create a GUI window
root = tk.Tk()
root.title("Hand Detection App")

# Set fixed column widths for sidebar and main section
root.grid_columnconfigure(0, minsize=250)
root.grid_columnconfigure(1, weight=1)

# Create a left sidebar using the grid layout manager
sidebar = tk.Frame(root, bg="lightgray")
sidebar.grid(row=0, column=0, sticky="nsew")

# Create a section in the top left corner of the sidebar with a specific width and height
section_frame = tk.Frame(sidebar, bg="white", width=width, height=height)
section_frame.grid(padx=10, pady=10, sticky="nw")

# Create a Canvas to display the video feed
canvas = tk.Canvas(section_frame, width=width, height=height)
canvas.grid()

image_option = tk.Label(root, text="Image Option")
image_option.grid(row=0, column=1, sticky="nsew")
video_option = tk.Label(root, text="Video Option")
video_option.grid(row=0, column=1, sticky="nsew")

# Initially hide the image and video option widgets
image_option.grid_remove()
video_option.grid_remove()

# Initially, there is no video player
player = None

image_in_view = False
video_is_playing = False

# Create the image and video buttons
image_button = tk.Button(sidebar, text="Show Image Option", command=show_image_option)
video_button = tk.Button(sidebar, text="Show Video Option", command=show_video_option)
close_button = tk.Button(sidebar, text="close", command=close_option)

# Grid the buttons
image_button.grid()
video_button.grid()
close_button.grid()

# Make the rows expandable
root.grid_rowconfigure(0, weight=1)



def get_frame():
    global initial_hand_x, initial_hand_y, cooldownCounter, image_in_view,video_is_playing, player
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Mirror the frame for a more intuitive experience
    hands, frame = detector.findHands(frame)
    if hands:
        hand = hands[0]

        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        # lmlist = hand['lmList']

        if fingers != [0, 0, 0, 0, 0]:
            dx = (cx - initial_hand_x) * 5
            dy = (cy - initial_hand_y) * 5
            initial_hand_x, initial_hand_y = cx, cy

        # Presentation control
        if image_option:
            if fingers == [1, 1, 1, 1, 1]:
                if cooldownCounter == 0:  # Check if cooldown is over
                    if dx > 150:  # Swipe right
                         # Set cooldown
                        if image_in_view:
                            prev_image()  # Go to the previous image
                        else:
                            if player:
                                player.backward()
                        cooldownCounter = presentationCooldown
                    elif dx < -150:  # Swipe left
                        
                        if image_in_view:
                            next_image()  # Go to the next image
                        else:
                            if player:
                                player.forward()
                        cooldownCounter = presentationCooldown   # Set cooldown

        # Hand pointer
        if fingers == [0, 1, 0, 0, 0]:
            new_x = pyautogui.position().x + dx
            new_y = pyautogui.position().y + dy
            pyautogui.moveTo(new_x, new_y, duration=0.1)

        # Mouse click
        if fingers == [0, 1, 1, 0, 0]:
            pyautogui.click(interval=0.1)
            time.sleep(0.5)  # Wait for 0.5 seconds after clicking

        # Mouse scroll
        if fingers == [0, 1, 1, 1, 0]:
            scroll_factor = 2  # Adjust this value to control scrolling speed
            pyautogui.scroll(dy * scroll_factor)

        if player:
            if video_is_playing and fingers == [1, 0, 0, 0, 1]:
                if cooldownCounter <= 10:
                    player.pause()
                    cooldownCounter = 20
                video_is_playing = False
                
            elif not video_is_playing and fingers == [1, 0, 0, 0, 1]:
                if cooldownCounter <= 10:
                    player.play()
                    cooldownCounter = 20
                
                video_is_playing = True
            
            
        

    cooldownCounter = max(0, cooldownCounter - 1)

    if frame is not None:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=img)
        canvas.create_image(0, 0, image=img, anchor=tk.NW)
        canvas.img = img
        canvas.after(10, get_frame)


# Start capturing and displaying the video feed
get_frame()

# Run the Tkinter main loop
root.mainloop()

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
