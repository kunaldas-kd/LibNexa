import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import cv2
from PIL import Image, ImageTk
from paddleocr import PaddleOCR, draw_ocr
import numpy as np
import os
import sys

# Initialize OCR once (can take time on first run)
# Change lang if needed, e.g., "en", "ch", "fr", etc.
ocr = PaddleOCR(use_angle_cls=True, lang="en")  # May download models on first run

def preprocess_image(img_bgr):
    # Basic preprocessing: grayscale, contrast/brightness adjust, denoise
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    gray = cv2.convertScaleAbs(gray, alpha=1.3, beta=10)
    den = cv2.fastNlMeansDenoising(gray, h=10)
    return img_bgr, den

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Handwriting OCR (Tkinter + PaddleOCR)")
        self.geometry("900x650")
        self.image_path = None
        self.orig_bgr = None
        self.preview_tk = None

        # Font path for draw_ocr overlays
        self.font_path = None

        # Top controls
        top = tk.Frame(self)
        top.pack(fill=tk.X, padx=8, pady=8)

        self.btn_open = tk.Button(top, text="Open Image...", command=self.open_image)
        self.btn_open.pack(side=tk.LEFT, padx=5)

        self.var_use_bin = tk.BooleanVar(value=False)
        tk.Checkbutton(top, text="Use binarized input", variable=self.var_use_bin).pack(side=tk.LEFT, padx=5)

        self.btn_run = tk.Button(top, text="Run OCR", command=self.run_ocr_thread, state=tk.DISABLED)
        self.btn_run.pack(side=tk.LEFT, padx=5)

        self.btn_save_vis = tk.Button(top, text="Save Visualization", command=self.save_vis, state=tk.DISABLED)
        self.btn_save_vis.pack(side=tk.LEFT, padx=5)

        self.btn_font = tk.Button(top, text="Set Font...", command=self.choose_font)
        self.btn_font.pack(side=tk.LEFT, padx=5)

        # Image preview
        self.preview_label = tk.Label(self, text="No image loaded", anchor="center")
        self.preview_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Text output
        tk.Label(self, text="Recognized text:").pack(anchor="w", padx=10)
        self.text_box = scrolledtext.ScrolledText(self, height=10, wrap=tk.WORD)
        self.text_box.pack(fill=tk.BOTH, expand=False, padx=10, pady=(0,10))

        self.last_boxes = None
        self.last_txts = None
        self.last_scores = None

    def choose_font(self):
        path = filedialog.askopenfilename(
            title="Select TTF/OTF font",
            filetypes=[("Font files", "*.ttf;*.otf")]
        )
        if path:
            self.font_path = path
            messagebox.showinfo("Font selected", f"Using font:\n{path}")

    def open_image(self):
        path = filedialog.askopenfilename(
            title="Select image",
            filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff")]
        )
        if not path:
            return
        img = cv2.imread(path)
        if img is None:
            messagebox.showerror("Error", f"Could not read image:\n{path}")
            return
        self.image_path = path
        self.orig_bgr = img
        self.show_preview(img)
        self.text_box.delete(1.0, tk.END)
        self.btn_run.config(state=tk.NORMAL)
        self.btn_save_vis.config(state=tk.DISABLED)
        self.last_boxes = self.last_txts = self.last_scores = None

    def show_preview(self, img_bgr):
        # Fit to area while keeping aspect ratio
        h, w = img_bgr.shape[:2]
        max_w, max_h = 800, 400
        scale = min(max_w / w, max_h / h, 1.0)
        resized = cv2.resize(img_bgr, (int(w*scale), int(h*scale)))
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        pil = Image.fromarray(rgb)
        self.preview_tk = ImageTk.PhotoImage(pil)
        self.preview_label.configure(image=self.preview_tk)

    def run_ocr_thread(self):
        self.btn_run.config(state=tk.DISABLED)
        self.text_box.delete(1.0, tk.END)
        threading.Thread(target=self.run_ocr, daemon=True).start()

    def run_ocr(self):
        try:
            if self.orig_bgr is None:
                raise RuntimeError("No image loaded")
            orig, binarized = preprocess_image(self.orig_bgr)
            input_img = binarized if self.var_use_bin.get() else orig

            # PaddleOCR accepts numpy arrays (BGR) directly
            result = ocr.ocr(input_img, cls=True)
            lines_out = []
            boxes, txts, scores = [], [], []

            for page in result or []:
                for det in page:
                    box, (text, conf) = det
                    boxes.append(box)
                    txts.append(text)
                    scores.append(conf)
                    lines_out.append(f"{text} (conf={conf:.3f})")

            if not lines_out:
                lines_out = ["No text detected. Try toggling 'Use binarized input' or try a clearer image."]

            self.last_boxes, self.last_txts, self.last_scores = boxes, txts, scores

            self.text_box.insert(tk.END, "\n".join(lines_out))
            self.btn_save_vis.config(state=tk.NORMAL if boxes else tk.DISABLED)
        except Exception as e:
            messagebox.showerror("OCR Error", str(e))
        finally:
            self.btn_run.config(state=tk.NORMAL)

    def _default_font(self):
        # Provide a sensible default OS font for draw_ocr if user hasn't chosen one
        if sys.platform.startswith("win"):
            candidates = [
                r"C:\Windows\Fonts\arial.ttf",
                r"C:\Windows\Fonts\segoeui.ttf",
                r"C:\Windows\Fonts\calibri.ttf",
            ]
        elif sys.platform == "darwin":
            candidates = [
                "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
                "/System/Library/Fonts/Supplemental/Arial.ttf",
                "/Library/Fonts/Arial.ttf",
            ]
        else:
            candidates = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
            ]
        for c in candidates:
            if os.path.exists(c):
                return c
        return None  # draw_ocr may still handle None but better to pick a font

    def save_vis(self):
        if self.orig_bgr is None or not self.last_boxes:
            messagebox.showinfo("Info", "Nothing to visualize yet.")
            return
        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")],
            title="Save visualization"
        )
        if not save_path:
            return
        try:
            # Convert base image to PIL for draw_ocr
            image = Image.fromarray(cv2.cvtColor(self.orig_bgr, cv2.COLOR_BGR2RGB))

            font = self.font_path or self._default_font()

            im_drawn = draw_ocr(
                image,
                self.last_boxes,
                self.last_txts,
                self.last_scores,
                font_path=font
            )
            # draw_ocr returns a numpy array (RGB)
            Image.fromarray(im_drawn).save(save_path)
            messagebox.showinfo("Saved", f"Visualization saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Visualization Error", f"Failed to save visualization:\n{e}")

if __name__ == "__main__":
    # Keep a reference so Tk image objects and the instance don't get GC'd
    app = App()
    app.mainloop()
