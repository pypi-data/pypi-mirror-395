
  
# d3c-polyskel  
  
A packaged and maintained version of polyskel for use in D3Companion projects.  
  
## Credits  
  
d3c-polyskel is a redistributed and repackaged version of the [polyskel library by Ármin Scipiades (@Bottfy)](https://github.com/Botffy/polyskel), which is a Python implementation of the straight skeleton algorithm as described by Felkel and Obdržálek in their 1998 conference paper "Straight skeleton implementation."  
  
### Key differences from the original: 
- Packaged for PyPI distribution with modern Python packaging (pyproject.toml)  
- Removed test files and development artifacts    
- Added proper dependency management  
- Maintained for compatibility with D3Companion toolchain  
  
## Installation  
  
```bash  
pip install d3c-polyskel
```

## Quick start  
  
  ### Basic Example

```python  
from d3c_polyskel import skeletonize

rectangle = [(40, 40), (40, 310), (520, 310), (520, 40)]
skeleton = skeletonize(polygon=rectangle)
```
 ### Polygon with holes

```python  
from d3c_polyskel import skeletonize

rectangle = [(40, 40), (40, 310), (520, 310), (520, 40)]
holes = [[(100, 100), (200, 100), (200, 150), (100, 150)]]
skeleton = skeletonize(polygon=rectangle, holes=holes)
```

## Support

For issues related to this package, please open an issue on this repository.
For questions about the original polyskel implementation, please refer to the [original repository](https://github.com/Botffy/polyskel?tab=readme-ov-file).

## License

This package contains code from the original polyskel library by Ármin Scipiades, licensed under **LGPL v3**.
Since we are redistributing the original LGPL source code, this entire package is licensed under **LGPL v3** (see LICENSE file).
Packaging and maintenance by D3Companion GmbH.