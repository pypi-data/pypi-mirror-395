# iconetto  
*A demo application for the Python package 👉 [iconipy](https://pypi.org/project/iconipy/)*

iconetto is a fully functional demonstration tool showcasing the capabilities of **iconipy**, a Python package for generating clean, scalable, and customizable icons on the fly.  
All UI elements—buttons, hover effects, and dynamic icon rendering—are implemented in **Tkinter** using **FreeSimpleGUI**, with every icon generated at runtime through iconipy.

Although originally created as a simple test script for iconipy, iconetto has grown into a practical utility that I now use regularly to design lightweight program icons for my own Python scripts, especially when preparing executables with PyInstaller.

---

## ✨ Features

- **Dynamic icon generation** using iconipy  
- **Interactive GUI** built with FreeSimpleGUI  
- **Live customization** of icon appearance (colors, shapes, outlines, effects, etc.)  
- **Real‑time preview**  
- **Export single icons** in multiple formats:  
  - PNG  
  - ICO  
  - WEBP  
  - GIF  
- **Bulk export** of entire icon sets with your chosen settings  
- **Automatic project file saving**  
  - Every export stores your configuration in a project file  
  - Project files can be reloaded at any time  
- **Practical tool for developers**  
  - Quickly create simple icons (program icons, favicons, website buttons, etc.)  

---

## 🚀 Installation

```bash
pip install iconetto
```

---

## 🖥️ Usage

After installation, simply run:

```bash
python -m iconetto
```
or
```bash
iconetto
```

This opens the graphical interface where you can:

- Adjust icon / button parameters  
- Preview icon / button styles  
- Export icons or full icon sets  
- Save and reload project configurations  

No additional setup is required.

---

## 📁 Project Files

Whenever you export an icon or icon set, iconetto automatically saves a project file containing all current settings.  
This allows you to:

- Recreate icons / buttons later  
- Continue working on a previous design  
- Maintain consistent styling across multiple icons / buttons  

---

## 🎯 Purpose

iconetto started as a small internal test tool for iconipy.  
Over time, it evolved into a surprisingly useful everyday helper for generating quick, clean icons for Python applications.

If you need simple, customizable icons without relying on external graphics tools, iconetto might be exactly what you’re looking for.

---

## 📜 License

This project is released under the MIT License.
