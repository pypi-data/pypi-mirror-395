"""Simple sampling GUI based on OpenCV and a Tk file dialog.

Usage:
    python -m sampler.gui
or
    from sampler.gui import run_gui; run_gui()
"""
from __future__ import annotations

import json
import os
from typing import List, Optional

import argparse
import sys

import cv2
import numpy as np
from glob import glob


class LineSample:
    """Container for sampled points and optional midscreen crossing."""

    def __init__(self) -> None:
        self.midscreen_x: Optional[int] = None
        self.points: List[List[int]] = []


class SamplerApp:
    """Runs an image sampling session.

    The GUI uses OpenCV windows. Use the file dialog to select image files.
    Controls:
      - Click left: add point to current sample
      - Enter: add current crosshair as point
      - N: start a new line sample
      - Backspace/Delete: remove last point from current sample
      - Q/E: prev/next image
      - Arrow keys / WASD: move crosshair
      - ESC: quit and save samples
    """

    def __init__(self, image_paths: List[str], save_path: str = "samples.json"):
        self.save_path = save_path
        self.image_paths = list(image_paths)
        images = []
        for p in self.image_paths:
            im = cv2.imread(p)
            if im is None:
                print(f"Warning: failed to read image: {p}")
                continue
            images.append(im)
        if not images:
            raise ValueError("No readable images provided to sampler")
        self.images = images
        self.img_h, self.img_w = self.images[0].shape[:2]
        self.midscreen_y = self.img_h // 2
        self.curr_idx = 0
        self.samples: List[LineSample] = []
        self.curr_x = self.img_w // 2
        self.curr_y = self.img_h // 2
        self.window = "Sampler"
        self.dot_radius = 5

    def new_line(self) -> None:
        self.samples.append(LineSample())

    def _draw(self, img: np.ndarray) -> np.ndarray:
        out = img.copy()
        cv2.line(out, (0, self.midscreen_y), (self.img_w - 1, self.midscreen_y), (0, 0, 255), 1)
        cv2.line(out, (self.curr_x, 0), (self.curr_x, self.img_h - 1), (0, 255, 0), 1)
        for s in self.samples:
            for pt in s.points:
                cv2.circle(out, (int(pt[0]), int(pt[1])), 3, (255, 0, 0), -1)
            if s.midscreen_x is not None:
                cv2.circle(out, (int(s.midscreen_x), self.midscreen_y), 5, (0, 255, 255), 1)
        cv2.circle(out, (int(self.curr_x), int(self.curr_y)), self.dot_radius, (0, 255, 255), -1)
        cv2.putText(out, 'Q/E: prev/next  N: new line  Enter/Click: add  Del: remove', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        return out

    def _mouse_cb(self, event, x, y, flags, param) -> None:
        if event == cv2.EVENT_MOUSEMOVE:
            self.curr_x = int(x)
            self.curr_y = int(y)
        elif event == cv2.EVENT_LBUTTONDOWN:
            if len(self.samples) == 0:
                self.new_line()
            self.samples[-1].points.append([int(x), int(y)])
            if abs(int(y) - self.midscreen_y) <= 2:
                self.samples[-1].midscreen_x = int(x)

    def _save(self) -> None:
        out = []
        for s in self.samples:
            out.append({"midscreen_x": s.midscreen_x, "points": s.points})
        with open(self.save_path, "w") as f:
            json.dump(out, f, indent=2)

    def run(self) -> None:
        cv2.namedWindow(self.window, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(self.window, lambda e, x, y, f, p: self._mouse_cb(e, x, y, f, p))
        if len(self.samples) == 0:
            self.new_line()
        running = True
        while running:
            img = self.images[self.curr_idx].copy()
            out = self._draw(img)
            cv2.imshow(self.window, out)
            key = cv2.waitKey(30)
            if key == -1 or key == 255:
                continue
            k = key & 0xFF
            if k in (ord('q'), ord('Q')):
                self.curr_idx = (self.curr_idx - 1) % len(self.images)
            elif k in (ord('e'), ord('E')):
                self.curr_idx = (self.curr_idx + 1) % len(self.images)
            elif k in (ord('n'), ord('N')):
                self.new_line()
            elif k in (8, 127):  # backspace/delete
                if self.samples and self.samples[-1].points:
                    self.samples[-1].points.pop()
            elif k in (13, 10):
                if len(self.samples) == 0:
                    self.new_line()
                self.samples[-1].points.append([int(self.curr_x), int(self.curr_y)])
                if abs(int(self.curr_y) - self.midscreen_y) <= 2:
                    self.samples[-1].midscreen_x = int(self.curr_x)
            elif k == 27:
                running = False
            elif k in (ord('a'), ord('A')):
                self.curr_x = max(0, self.curr_x - 1)
            elif k in (ord('d'), ord('D')):
                self.curr_x = min(self.img_w - 1, self.curr_x + 1)
            elif k in (ord('w'), ord('W')):
                self.curr_y = max(0, self.curr_y - 1)
            elif k in (ord('s'), ord('S')):
                self.curr_y = min(self.img_h - 1, self.curr_y + 1)

        cv2.destroyWindow(self.window)
        try:
            os.makedirs(os.path.dirname(self.save_path) or '.', exist_ok=True)
            self._save()
            print(f"Saved samples to {self.save_path}")
        except Exception as e:
            print("Failed to save samples:", e)


def _select_files_with_dialog() -> List[str]:
    try:
        import tkinter as tk  # type: ignore
        from tkinter import filedialog  # type: ignore
    except Exception:
        # Tk not available on this Python build (common on macOS/Homebrew).
        # Fallback: search common image files in workspace or prompt user.
        candidates = []
        for pat in ("*.png", "*.jpg", "*.jpeg", "*.JPG", "*.PNG"):
            candidates.extend(glob(pat))
        if candidates:
            print("tkinter not available — found images in current directory; using those.")
            return sorted(candidates)
        print("tkinter not available and no images found. Enter image paths separated by spaces, or leave empty to cancel:")
        line = input("Images> ")
        if not line.strip():
            return []
        return [p for p in line.split() if p]

    root = tk.Tk()
    root.withdraw()
    paths = filedialog.askopenfilenames(title="Select images for sampling", filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.JPG;*.PNG")])
    root.destroy()
    return list(paths)


def run_gui(image_paths: Optional[List[str]] = None, save_path: str = "samples.json") -> None:
    """Launch sampler GUI. If image_paths is None, a file dialog will open."""
    if image_paths is None or len(image_paths) == 0:
        image_paths = _select_files_with_dialog()
    if not image_paths:
        print("No images selected. Exiting.")
        return
    app = SamplerApp(list(image_paths), save_path=save_path)
    app.run()


def _main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Sampler GUI for collecting line samples from images")
    parser.add_argument("-i", "--images", nargs="*", help="Paths to image files to sample from")
    parser.add_argument("-s", "--save", default="samples.json", help="Output JSON path for samples")
    args = parser.parse_args(argv)
    run_gui(image_paths=list(args.images) if args.images else None, save_path=args.save)
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
