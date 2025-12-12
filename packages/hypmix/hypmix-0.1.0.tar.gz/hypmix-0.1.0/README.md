# hypmix
Hyperspectral Unmixing Library for Python

## Installation

```bash
pip install hypmix
```

## Usage
```python
import hypmix

em_list = []
for data, wvl in zip(spectrum_list, wvl_list):
    spec=hypmix.Spectrum(data, wvl)
    em_list.append(hypmix.EndMember("endmember1", spec))

model = hypmix.MixtureModel(em_list, data_cube)
model.add_virtual_shade()

res = model.run("save/path/results.hdf5", "model_name")
hypmix.save_model_result(res)
```
