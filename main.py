from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

MID = "#50B498"
LIGHT = "#DEF9C4"
DARK = "#468585"
FONT = ("Arial", 16, "bold")

# TODO 1: Fix image resolution size so that when you upload it stays quality
# TODO 2: Write code to reset app

"""This is an application that takes two images and alters the opacity of the second to layer it onto the first
as a watermark. The resulting image can then be saved to files."""


def step_three(img, img_2):
    """Edit buttons to allow changing of both images. Display button to combine images
     as well as the scale to adjust opacity"""
    watermark.grid(column=2, row=2)
    watermark.config(text="Change Watermark")
    upload.grid(column=0, row=2)
    upload.config(text="Change Photo", command=change)
    header.grid_forget()
    combine.config(command=lambda: combine_images(img, img_2))
    combine.grid(column=1, row=1, padx=10, pady=10)
    alpha_scale.grid(column=1, row=2, padx=10, pady=10)


def upload_watermark(img):
    """Open file explorer to choose watermark image. Automatically resize and display on label."""
    watermark_file = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
    img_2 = Image.open(watermark_file).resize((800, 800))
    img_2 = img_2.convert(mode="RGBA")
    watermark_photo = ImageTk.PhotoImage(img_2)
    watermark_label.config(image=watermark_photo, width=800, height=800)
    watermark_label.photo = watermark_photo
    window.minsize(screen_width, screen_height)
    window.state('zoomed')
    step_three(img, img_2)


def save_img(wm_img):
    """On click, open file explorer to save. Automatically saves as jpeg"""
    answer = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
    wm_img.save(fp=answer)


def combine_images(img, img_2):
    """Take number from scale and use as opacity setting for top image. Combine to back image after adjusting opacity
    as needed. Removes both original images to display combined image and creates save button."""
    alpha = (alpha_scale.get()) / 100
    blank = Image.open("blank.png").resize((800, 800))
    blank = blank.convert(mode="RGBA")
    combined_image = Image.blend(im1=img_2, im2=blank, alpha=alpha)
    combined_image = Image.alpha_composite(im1=img, im2=combined_image)
    combined_img = ImageTk.PhotoImage(combined_image)
    combined_img_label.config(image=combined_img, width=800, height=800)
    combined_img_label.photo = combined_img
    combined_image = combined_image.convert("RGB")
    image_label.destroy()
    watermark_label.destroy()
    watermark.destroy()
    upload.destroy()

    combine.config(text="Adjust")
    save.config(command=lambda: save_img(combined_image))
    save.grid(column=0, row=0, columnspan=3)


def change():
    """Changes uploaded image without creating/modifying buttons."""
    image_file = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
    if image_file:
        img = Image.open(image_file).resize((600, 600))
        img = img.convert(mode="RGBA")
        photo = ImageTk.PhotoImage(img)
        image_label.config(image=photo, width=600, height=600)
        image_label.photo = photo


def choose_photo():
    """Select initial photo to be watermarked. Resizes photo and displays as label before
     displaying watermark button."""
    image_file = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
    if image_file:
        img = Image.open(image_file).resize((800, 800))
        img = img.convert(mode="RGBA")
        photo = ImageTk.PhotoImage(img)
        image_label.config(image=photo, width=800, height=800)
        image_label.photo = photo
        watermark.config(command=lambda: upload_watermark(img))
        watermark.grid(column=0, row=1, columnspan=3)
        upload.grid_forget()


# ----------------Window and Canvas Creation----------------------
window = Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.config(width=600, height=600, background=DARK, padx=10, pady=10)
canvas = Canvas(width=200, height=200, bg=DARK, highlightthickness=0)

# ----------------------Labels -----------------------
header = Label(text="Watermarking App", padx=20, pady=20, font=FONT, fg=LIGHT, bg=DARK)
header.grid(column=0, row=0, columnspan=3)

image_label = Label(text="", font=FONT, justify="center", fg=LIGHT, bg=DARK)
image_label.grid(column=0, row=5)

watermark_label = Label(text="", font=FONT, justify="center", fg=LIGHT, bg=DARK)
watermark_label.grid(column=2, row=5)

combined_img_label = Label(text="", font=FONT, justify="center", fg=LIGHT, bg=DARK)
combined_img_label.grid(column=1, row=5)

footer = Label(text="2024", justify="center", padx=20, pady=20, fg=LIGHT, bg=DARK)
footer.grid(column=0, row=7, columnspan=3)
# -------------Buttons -----------------------
upload = Button(text="Upload Photo", font=FONT, bg=MID, fg=LIGHT, highlightthickness=0, command=choose_photo)
upload.grid(column=0, row=1, columnspan=3)

combine = Button(text="Combine", font=FONT, bg=MID, fg=LIGHT, highlightthickness=0)

watermark = Button(text="Upload Watermark", font=FONT, bg=MID, fg=LIGHT, highlightthickness=0, )

save = Button(text="Save", font=FONT, bg=MID, fg=LIGHT, highlightthickness=0, )

# ----------------------Widgets --------------------

alpha_scale = Scale(
    window, from_=100, to=0, orient=HORIZONTAL, tickinterval=10, length=200,
    bg=DARK, fg=LIGHT, troughcolor=MID, label="Opacity Adjuster")
alpha_scale.set(50)

window.mainloop()
