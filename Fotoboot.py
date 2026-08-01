import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime
from PIL import Image, ImageTk

# =========================
# SETUP
# =========================
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Kamera tidak bisa dibuka")

os.makedirs("strip", exist_ok=True)

EVENT_NAME = "Photobooth Rumahan"
shots = [None, None, None]
selected_slot = 0
preview_strip = None
CURRENT_TEMPLATE = "clean"

# =========================
# ROOT
# =========================
root = tk.Tk()
root.title("Photobooth Rumahan")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
root.resizable(False, False)
root.configure(bg="#1b1b1b")

# =========================
# TEMPLATES
# =========================
TEMPLATES = {
    "clean": {
        "bg": (245, 245, 245),
        "title_color": (40, 40, 40),
        "subtitle_color": (90, 90, 90),
        "footer_color": (50, 50, 50),
        "border_color": (230, 230, 230),
        "name": "Clean",
    },
    "dark": {
        "bg": (30, 30, 30),
        "title_color": (255, 255, 255),
        "subtitle_color": (190, 190, 190),
        "footer_color": (235, 235, 235),
        "border_color": (80, 80, 80),
        "name": "Dark",
    },
    "warm": {
        "bg": (235, 225, 210),
        "title_color": (70, 50, 30),
        "subtitle_color": (110, 80, 50),
        "footer_color": (80, 60, 40),
        "border_color": (210, 190, 170),
        "name": "Warm",
    },
}

# =========================
# UTIL
# =========================
def cv_to_tk(frame):
    if frame is None:
        return None
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb)
    return ImageTk.PhotoImage(img)

def capture_frame():
    ret, frame = cap.read()
    if not ret:
        return None
    return cv2.flip(frame, 1)

def add_frame(frame):
    if frame is None:
        return None
    h, w = frame.shape[:2]
    cv2.rectangle(frame, (10, 10), (w - 10, h - 10), (200, 200, 200), 6)
    cv2.rectangle(frame, (24, 24), (w - 24, h - 24), (255, 255, 255), 2)
    return frame

def make_thumb(frame, size=(120, 82)):
    if frame is None:
        img = np.full((size[1], size[0], 3), 230, dtype=np.uint8)
        cv2.putText(img, "Empty", (16, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (110, 110, 110), 2)
        return img
    return cv2.resize(frame, size)

def make_strip(images):
    tw, th = 380, 260
    margin_x = 40
    top_space = 110
    gap = 18
    caption_h = 170

    tpl = TEMPLATES[CURRENT_TEMPLATE]
    canvas_w = tw + (margin_x * 2)
    canvas_h = top_space + (th * 3) + (gap * 2) + caption_h
    canvas = np.full((canvas_h, canvas_w, 3), tpl["bg"], dtype=np.uint8)

    cv2.putText(canvas, EVENT_NAME, (margin_x, 42),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, tpl["title_color"], 2)
    cv2.putText(canvas, datetime.now().strftime("%d-%m-%Y"), (margin_x, 72),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, tpl["subtitle_color"], 2)
    cv2.putText(canvas, f"Template: {tpl['name']}", (margin_x, 98),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, tpl["title_color"], 2)

    y = top_space
    for i, img in enumerate([cv2.resize(img, (tw, th)) for img in images]):
        x = margin_x
        canvas[y:y+th, x:x+tw] = img
        cv2.rectangle(canvas, (x, y), (x + tw, y + th), tpl["border_color"], 3)
        cv2.putText(canvas, f"Foto {i+1}", (x + 12, y + 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (255, 255, 255) if CURRENT_TEMPLATE == "dark" else (35, 35, 35), 2)
        y += th + gap

    line_y = top_space + (th * 3) + (gap * 2) + 18
    cv2.line(canvas, (margin_x, line_y), (canvas_w - margin_x, line_y), tpl["border_color"], 2)
    cv2.putText(canvas, "Terima kasih sudah berfoto", (margin_x, line_y + 42),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, tpl["footer_color"], 2)
    cv2.putText(canvas, "Photobooth sederhana dari laptop", (margin_x, line_y + 76),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, tpl["subtitle_color"], 2)
    return canvas

def show_countdown():
    win = tk.Toplevel(root)
    win.attributes("-fullscreen", True)
    win.configure(bg="#101010")
    win.grab_set()

    tk.Label(win, text="SIAP FOTO", bg="#101010", fg="white",
             font=("Arial", 24, "bold")).pack(pady=40)

    num_label = tk.Label(win, text="", bg="#101010", fg="white",
                         font=("Arial", 140, "bold"))
    num_label.pack(expand=True)

    tk.Label(win, text="Tetap diam dan lihat kamera", bg="#101010", fg="#bfbfbf",
             font=("Arial", 18)).pack(pady=40)

    win.update()
    for n in [3, 2, 1]:
        num_label.config(text=str(n))
        win.update()
        win.after(1000)
    win.destroy()

# =========================
# UI UPDATE
# =========================
def update_thumbnails():
    for i in range(3):
        thumb = make_thumb(shots[i])
        img = cv_to_tk(thumb)
        thumb_labels[i].configure(image=img)
        thumb_labels[i].image = img
        thumb_cards[i].configure(bg="#2a2a2a" if i == selected_slot else "#202020")

def show_strip_preview():
    if preview_strip is None:
        preview_canvas.delete("all")
        return

    display_w = 320
    h, w = preview_strip.shape[:2]
    display_h = int(h * display_w / w)
    disp = cv2.resize(preview_strip, (display_w, display_h))

    img = cv_to_tk(disp)
    preview_canvas.delete("all")
    preview_canvas.create_image(0, 0, anchor="nw", image=img)
    preview_canvas.image = img
    preview_canvas.configure(scrollregion=(0, 0, display_w, display_h))

def update_final_preview():
    global preview_strip
    if all(s is not None for s in shots):
        preview_strip = make_strip(shots)
        show_strip_preview()
    else:
        preview_strip = None
        preview_canvas.delete("all")
    update_thumbnails()

def refresh_template_label():
    template_label.config(text=f"Template aktif: {TEMPLATES[CURRENT_TEMPLATE]['name']}")

# =========================
# ACTIONS
# =========================
def set_slot(idx):
    global selected_slot
    selected_slot = idx
    slot_var.set(f"Slot aktif: {selected_slot + 1}")
    update_thumbnails()

def set_template(key):
    global CURRENT_TEMPLATE
    CURRENT_TEMPLATE = key
    refresh_template_label()
    update_final_preview()

def ask_event():
    global EVENT_NAME
    name = simpledialog.askstring("Nama Acara", "Masukkan nama acara:")
    if name and name.strip():
        EVENT_NAME = name.strip()
    event_label.config(text=f"Event: {EVENT_NAME}")
    update_final_preview()

def do_capture_session():
    global shots
    shots = [None, None, None]
    update_thumbnails()
    preview_canvas.delete("all")
    for i in range(3):
        show_countdown()
        frame = capture_frame()
        if frame is not None:
            shots[i] = add_frame(frame)
        update_thumbnails()
    update_final_preview()

def do_retake():
    if shots[selected_slot] is None:
        messagebox.showinfo("Info", "Slot ini belum ada foto. Silakan capture dulu.")
        return
    show_countdown()
    frame = capture_frame()
    if frame is not None:
        shots[selected_slot] = add_frame(frame)
    update_final_preview()

def do_save():
    global preview_strip
    if preview_strip is None:
        messagebox.showinfo("Info", "Belum ada strip untuk disimpan.")
        return
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
    cv2.imwrite(os.path.join("strip", filename), preview_strip)
    messagebox.showinfo("Sukses", f"Strip tersimpan:\n{filename}")

def do_quit():
    cap.release()
    cv2.destroyAllWindows()
    root.destroy()

def refresh_camera():
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        preview = cv2.resize(frame, (380, 285))

        cv2.putText(preview, "PHOTOBOOTH", (16, 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
        cv2.putText(preview, f"Slot aktif: {selected_slot + 1}", (16, 54),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 2)
        cv2.putText(preview, f"Template: {TEMPLATES[CURRENT_TEMPLATE]['name']}", (16, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 2)

        img = cv_to_tk(preview)
        camera_label.configure(image=img)
        camera_label.image = img

    root.after(30, refresh_camera)

# =========================
# LAYOUT
# =========================
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=2)

header = tk.Frame(root, bg="#0f0f0f", height=56)
header.grid(row=0, column=0, columnspan=2, sticky="nsew")
header.grid_propagate(False)
tk.Label(header, text="PHOTOBOOTH RUMAHAN", bg="#0f0f0f", fg="white",
         font=("Arial", 18, "bold")).pack(pady=10)

content = tk.Frame(root, bg="#1b1b1b")
content.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
content.grid_rowconfigure(0, weight=1)
content.grid_columnconfigure(0, weight=3)
content.grid_columnconfigure(1, weight=2)

left = tk.Frame(content, bg="#1b1b1b")
left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
left.grid_rowconfigure(0, weight=3)
left.grid_rowconfigure(1, weight=1)
left.grid_columnconfigure(0, weight=1)

right = tk.Frame(content, bg="#1b1b1b")
right.grid(row=0, column=1, sticky="nsew")
right.grid_rowconfigure(0, weight=0)
right.grid_rowconfigure(1, weight=0)
right.grid_rowconfigure(2, weight=1)
right.grid_columnconfigure(0, weight=1)

camera_card = tk.Frame(left, bg="#202020", bd=1, relief="solid")
camera_card.grid(row=0, column=0, sticky="nsew")
camera_card.grid_columnconfigure(0, weight=1)
camera_card.grid_rowconfigure(0, weight=1)

camera_label = tk.Label(camera_card, bg="#202020")
camera_label.grid(row=0, column=0, padx=10, pady=10)

bottom = tk.Frame(left, bg="#1b1b1b")
bottom.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
bottom.grid_columnconfigure(0, weight=1)

event_label = tk.Label(bottom, text=f"Event: {EVENT_NAME}", bg="#1b1b1b", fg="white",
                       font=("Arial", 11, "bold"))
event_label.grid(row=0, column=0, sticky="w", pady=(0, 4))

status_row = tk.Frame(bottom, bg="#1b1b1b")
status_row.grid(row=1, column=0, sticky="w", pady=(0, 6))
slot_var = tk.StringVar(value="Slot aktif: 1")
tk.Label(status_row, textvariable=slot_var, bg="#1b1b1b", fg="white",
         font=("Arial", 10)).pack(side="left", padx=6)

template_label = tk.Label(bottom, text="Template aktif: Clean", bg="#1b1b1b", fg="white",
                          font=("Arial", 10))
template_label.grid(row=2, column=0, sticky="w", pady=(0, 8))

tk.Label(bottom, text="Slot Kamera", bg="#1b1b1b", fg="white",
         font=("Arial", 11, "bold")).grid(row=3, column=0, sticky="w", pady=(0, 4))

slot_row = tk.Frame(bottom, bg="#1b1b1b")
slot_row.grid(row=4, column=0, sticky="w")

thumb_cards = []
thumb_labels = []

for i in range(3):
    card = tk.Frame(slot_row, bg="#202020", bd=1, relief="solid")
    card.pack(side="left", padx=6)
    thumb_cards.append(card)

    tk.Label(card, text=f"Slot {i+1}", bg="#202020", fg="white",
             font=("Arial", 10, "bold")).pack(pady=(4, 2))
    img_label = tk.Label(card, bg="#202020")
    img_label.pack(padx=6, pady=4)
    thumb_labels.append(img_label)

    btn_row = tk.Frame(card, bg="#202020")
    btn_row.pack(pady=(0, 5))
    tk.Button(btn_row, text="Select", command=lambda i=i: set_slot(i), width=7,
              bg="#2f2f2f", fg="white", relief="flat").pack(side="left", padx=2)
    tk.Button(btn_row, text="Retake", command=do_retake, width=7,
              bg="#2f2f2f", fg="white", relief="flat").pack(side="left", padx=2)

control_card = tk.Frame(right, bg="#202020", bd=1, relief="solid")
control_card.grid(row=0, column=0, sticky="new", pady=(0, 10))
tk.Label(control_card, text="Controls", bg="#202020", fg="white",
         font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 8))

for txt, cmd in [
    ("Set Event Name", ask_event),
    ("Capture Session", do_capture_session),
    ("Save Strip", do_save),
    ("Quit", do_quit),
]:
    tk.Button(control_card, text=txt, command=cmd, width=20, height=1,
              bg="#2f2f2f", fg="white", relief="flat").pack(pady=4, padx=10, fill="x")

template_card = tk.Frame(right, bg="#202020", bd=1, relief="solid")
template_card.grid(row=1, column=0, sticky="new", pady=(0, 10))
tk.Label(template_card, text="Template", bg="#202020", fg="white",
         font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(10, 8))

for key in ["clean", "dark", "warm"]:
    tk.Button(template_card, text=TEMPLATES[key]["name"],
              command=lambda k=key: set_template(k),
              width=20, bg="#2f2f2f", fg="white", relief="flat").pack(pady=4, padx=10, fill="x")

preview_card = tk.Frame(right, bg="#202020", bd=1, relief="solid")
preview_card.grid(row=2, column=0, sticky="nsew")
preview_card.grid_rowconfigure(1, weight=1)
preview_card.grid_columnconfigure(0, weight=1)

tk.Label(preview_card, text="Final Strip Preview", bg="#202020", fg="white",
         font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 6))

preview_box = tk.Frame(preview_card, bg="#202020")
preview_box.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
preview_box.grid_rowconfigure(0, weight=1)
preview_canvas = tk.Canvas(preview_box, bg="#202020", highlightthickness=0, width=340, height=430)
preview_scrollbar = tk.Scrollbar(preview_box, orient="vertical", command=preview_canvas.yview)
preview_canvas.configure(yscrollcommand=preview_scrollbar.set)
preview_canvas.grid(row=0, column=0, sticky="nsew")
preview_scrollbar.grid(row=0, column=1, sticky="ns")

preview_canvas.bind_all(
    "<MouseWheel>",
    lambda e: preview_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
)

update_thumbnails()
refresh_camera()
root.mainloop()