<img alt="Openframe ApS" src="https://openframe-public.s3.eu-west-1.amazonaws.com/assets/logo-text-google-admin.png" width="200" />

# Criteria Set Protocol

## Python library
This is a Python library with types and implementations of the Criteria Set Protocol. It is published
publicly on [PyPI](https://pypi.org/project/openframe-criteria-set-protocol/) as `openframe-criteria-set-protocol`.

### Installation
```bash
pip install openframe-criteria-set-protocol
```

### Contents
#### Protocol v1
The library contains the types defined in the protocol v1 specification.

##### Types
| Type                          | Remarks                                             |
|-------------------------------|-----------------------------------------------------|
| **Metadata types**            |                                                     |
| `Metadata`                    |                                                     |
| `Theme`                       |                                                     |
| `ThemeStyle`                  |                                                     |
| `Color`                       |                                                     |
| `RgbColor`                    |                                                     |
| **Task tree types**           |                                                     |
| `CriteriaTree`                |                                                     |
| `Criterion`                   |                                                     |
| `TaskGroup`                   |                                                     |
| `Task`                        |                                                     |
| `TaskItem`                    |                                                     |
| **TaskItem value types**      |                                                     |
| `SelectSingleType`            |                                                     |
| `SelectMultipleType`          |                                                     |
| `NumberType`                  |                                                     |
| `BooleanType`                 |                                                     |
| `PointOption`                 | Used by `SelectSingleType` and `SelectMultipleType` |
| `TaskItemValue`               | The raw value of a TaskItem, which can be an array  |
| `TaskItemScalarValue`         | The raw value of a TaskItem                         |
| **REST types**                |                                                     |
| `MetadataResponse`            | Metadata endpoint response body                     |
| `StreamCriteriaSetMatrixBody` | Request body for the matrix streaming endpoints     |
| `StreamMatrixResponse`        | Matrix streaming endpoints response body            |

##### Schemas
Validation schemas are provided for validating the endpoints of the protocol v1 specification.

| Schema                    | Remarks                                                                         |
|---------------------------|---------------------------------------------------------------------------------|
| `criteria_set_id`         | Regular expression for the criteria_set_id parameter for endpoints which use it |
| `version`                 | Regular expression for the version parameter for endpoints which use it         |
| **marshmallow schemas**   |                                                                                 |
| `TreeAndMatrixBodySchema` | Schema for validating the request body for tree and matrix endpoints            |

### Deployment
Deploy using the following commands:

```bash
python3 -m build
python3 -m twine upload dist/*
```

## License
<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/openframe-org/criteria-set-protocol">Openframe Criteria Set Protocol</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/andresangulo">Openframe ApS</a> is licensed under <a href="http://creativecommons.org/licenses/by-nd/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-ND 4.0<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nd.svg?ref=chooser-v1"></a></p>
