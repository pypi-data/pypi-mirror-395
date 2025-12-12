# torchfits v0.1.1 - First PyPI Release

**High-performance FITS I/O for PyTorch**

We're excited to announce the first public release of `torchfits` on PyPI! This library brings native PyTorch integration to astronomical FITS files, enabling zero-copy tensor operations and GPU acceleration for astronomy workflows.

## 🚀 Installation

```bash
pip install torchfits
```

**Requirements:**
- Python ≥ 3.11
- PyTorch ≥ 2.0.0
- System libraries: cfitsio, wcslib (installed automatically on most systems)

## ✨ Key Features

### High-Performance I/O
- **1.3-1.7× faster** than fitsio for images and tables
- Zero-copy tensor creation from FITS data
- Direct GPU loading (CUDA, MPS) without CPU intermediates
- Memory-mapped reading for files larger than RAM

### Native PyTorch Integration
- Read FITS → PyTorch tensors in one line
- Write tensors → FITS with full header support
- PyTorch Dataset/DataLoader integration
- Batch processing with automatic optimization

### PyTorch-Frame Support (NEW in v0.1.1)
- Convert FITS tables → TensorFrame for tabular deep learning
- Automatic semantic type inference (numerical/categorical)
- Round-trip FITS ↔ TensorFrame conversion
- See `examples/example_frame.py` for complete workflow

### Astronomy-Optimized
- WCS coordinate transformations (pixel ↔ world)
- Astronomy transforms: ZScale, AsinhStretch, LogStretch
- Multi-extension FITS (MEF) support
- Compressed FITS (Rice, gzip) reading
- Table operations: column selection, row ranges, streaming

## 📊 Performance

Benchmarked against astropy and fitsio on real astronomical data:

| Operation | torchfits | fitsio | astropy | Speedup |
|-----------|-----------|--------|---------|---------|
| 4k×4k image read | **0.012s** | 0.016s | 0.089s | 1.3-7.4× |
| 1M row table | **0.089s** | 0.152s | 0.341s | 1.7-3.8× |
| GPU transfer | **0.003s** | 0.156s | 0.158s | 52× |

*Methodology: Average of 100 runs on M1 Mac, data in page cache*

## 🎯 Quick Start

### Read FITS Image
```python
import torchfits

# Read to PyTorch tensor
data, header = torchfits.read("image.fits")
print(data.shape, data.dtype)  # torch.Size([2048, 2048]), torch.float32

# Read directly to GPU
data_gpu, _ = torchfits.read("image.fits", device='cuda')
```

### Read FITS Table
```python
# Read table as dictionary of tensors
table, header = torchfits.read("catalog.fits", hdu=1)
print(table.keys())  # ['RA', 'DEC', 'MAG', ...]

# Select specific columns
data, _ = torchfits.read("catalog.fits", hdu=1, 
                         columns=['RA', 'DEC'])
```

### PyTorch-Frame Integration
```python
# Convert FITS table to TensorFrame
tf = torchfits.read_tensor_frame("catalog.fits", hdu=1)

# Access features by semantic type
from torch_frame import stype
print(tf.feat_dict[stype.numerical])    # Numerical features
print(tf.feat_dict[stype.categorical])  # Categorical features
```

### Astronomy Transforms
```python
from torchfits.transforms import ZScale, AsinhStretch, Compose

transform = Compose([
    ZScale(),           # IRAF ZScale normalization
    AsinhStretch(),     # High dynamic range stretch
])

data, _ = torchfits.read("image.fits", device='cuda')
processed = transform(data)
```

## 📚 Documentation

- **README**: https://github.com/sfabbro/torchfits#readme
- **API Reference**: https://github.com/sfabbro/torchfits/blob/main/API.md
- **Examples**: https://github.com/sfabbro/torchfits/tree/main/examples

## 🆕 What's New in v0.1.1

### Added
- **PyTorch-Frame integration documentation** - Complete guide in README and API docs
- **New example**: `example_frame.py` - Comprehensive TensorFrame workflow
- **API documentation** for `read_tensor_frame()`, `to_tensor_frame()`, `write_tensor_frame()`

This patch release adds documentation for the existing PyTorch-Frame integration, making it easier to use FITS tables with tabular deep learning models.

## 🔧 System Requirements

**Supported Platforms:**
- Linux (Ubuntu 20.04+, RHEL 8+)
- macOS (11.0+, both Intel and Apple Silicon)

**Python Versions:**
- Python 3.11, 3.12, 3.13

**Dependencies:**
- PyTorch ≥ 2.0.0
- pytorch-frame ≥ 0.2.0 (optional, for TensorFrame support)
- NumPy ≥ 1.20.0
- psutil ≥ 5.0.0

**System Libraries** (auto-installed via conda/mamba):
- cfitsio ≥ 3.49
- wcslib ≥ 7.0

## 🤝 Contributing

We welcome contributions! Please see our [GitHub repository](https://github.com/sfabbro/torchfits) for:
- Bug reports and feature requests
- Code contributions
- Documentation improvements

## 📄 License

GNU General Public License v2.0 (GPL-2.0)

## 🙏 Acknowledgments

Built on top of:
- **cfitsio** - NASA's FITS I/O library
- **wcslib** - World Coordinate System library
- **PyTorch** - Deep learning framework
- **pytorch-frame** - Tabular deep learning

---

**Links:**
- PyPI: https://pypi.org/project/torchfits/
- GitHub: https://github.com/sfabbro/torchfits
- Issues: https://github.com/sfabbro/torchfits/issues
