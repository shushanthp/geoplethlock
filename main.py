import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import geopandas as gpd
import matplotlib.pyplot as plt
from geoplethlock_core import *

class GeoPlethLockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GeoPlethLock GUI Tool")

        self.raster_path = ""
        self.choropleth_path = ""
        self.key = None

        ttk.Button(root, text="Load Raster", command=self.load_raster).pack(pady=5)
        ttk.Button(root, text="Load Choropleth", command=self.load_choropleth).pack(pady=5)
        ttk.Button(root, text="Generate Key", command=self.make_key).pack(pady=5)
        ttk.Button(root, text="Encrypt and Overlay", command=self.encrypt_overlay).pack(pady=5)
        ttk.Button(root, text="Decrypt", command=self.decrypt).pack(pady=5)

    def load_raster(self):
        self.raster_path = filedialog.askopenfilename()
        messagebox.showinfo("Raster Loaded", f"Raster loaded: {self.raster_path}")

    def load_choropleth(self):
        self.choropleth_path = filedialog.askopenfilename()
        messagebox.showinfo("Choropleth Loaded", f"Choropleth loaded: {self.choropleth_path}")

    def make_key(self):
        self.key = generate_key()
        save_key(self.key, "keys/secret.key")
        messagebox.showinfo("Key Generated", "Key saved to keys/secret.key")

    def encrypt_overlay(self):
        if not self.raster_path or not self.choropleth_path or not self.key:
            messagebox.showerror("Missing Info", "Load raster, choropleth, and key first!")
            return
        gdf = load_choropleth(self.choropleth_path)
        enc_gdf = encrypt_coordinates(gdf, self.key)
        enc_gdf.plot()
        plt.title("Encrypted Choropleth Overlay")
        plt.show()

    def decrypt(self):
        key_path = filedialog.askopenfilename()
        key = load_key(key_path)
        gdf = load_choropleth(self.choropleth_path)
        decrypted = decrypt_coordinates(gdf, key)
        for d in decrypted[:5]: print("Decrypted:", d)
        messagebox.showinfo("Decryption", "Decryption successful! Check console.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GeoPlethLockApp(root)
    root.mainloop()
