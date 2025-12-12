# SeisPlotPy Desktop

**SeisPlotPy** is a high-performance seismic visualization and analysis tool designed for geophysicists and researchers. Built with **Python 3**, **PyQt6**, and **PyQtGraph**, it offers a fast, interactive environment for viewing and processing 2D SEG-Y data.

---

## Key Features

### 🚀 High-Performance Visualization
- **Zero-Lag Rendering**: Visualizes thousands of traces instantly using hardware-accelerated rendering.
- **Interactive Navigation**: Smooth zooming, panning, and gain control.
- **Header Inspection**: View text headers (EBCDIC/ASCII) and binary headers.

### 🛠️ Seismic Processing
- **AGC (Automatic Gain Control)**: Dynamic amplitude balancing.
- **Bandpass Filter**: Zero-phase filtering with adjustable corner frequencies.
- **Attribute Analysis**:
  - Instantaneous Amplitude (Envelope)
  - Instantaneous Phase & Cosine Phase
  - Instantaneous Frequency
  - RMS Amplitude

### 📉 Analysis Tools
- **Horizon Management**: Pick, edit, and export horizons to CSV.
- **Spectral Analysis**: View frequency spectrum of selected traces.
- **Quality Control**: Plot trace headers for geometry QC.

### 📤 Export
- **Publication Ready**: Export plots as high-resolution PDF or PNG.

---

## Installation

### For Users (Windows Executable)
No Python installation is required.
1. Go to the [Releases Page](https://github.com/arjun-vh/SeisPlotPy-Desktop/releases).
2. Download the latest `SeisPlotPy.exe`.
3. Run the executable directly.

### For Developers (Python)
Requirements: Python 3.10+

1. **Clone the repository:**
   ```bash
   git clone https://github.com/arjun-vh/SeisPlotPy-Desktop.git
   cd SeisPlotPy-Desktop
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

---

## Building from Source

To create the standalone `.exe` yourself:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Run the build command using the included spec file:
   ```bash
   python -m PyInstaller --noconfirm --clean SeisPlotPy.spec
   ```

3. The executable will be generated in the `dist/` directory.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any bugs or feature enhancements.

## License

This project is licensed under the **GPL License**. See the [LICENSE](LICENSE) file for details.

## Author

**Arjun V H**  
📧 arjunvelliyidathu@gmail.com
