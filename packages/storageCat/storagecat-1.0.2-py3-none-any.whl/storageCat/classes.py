import json
from dataclasses import asdict, dataclass, field
from typing import Optional


@dataclass
class ScientificMetadata:
    sample: dict = field(default_factory=dict)
    dataCollection: dict = field(default_factory=dict)
    otherParameters: Optional[dict] = field(default_factory=dict)

    def collect(self):
        if "name" not in self.sample:
            raise ValueError("Sample name has not been provided in `sample`")
        if "date" not in self.dataCollection:
            raise ValueError("Sample collection date has not been provided in `dataCollection`")

        result = {"sample": self.sample, "dataCollection": self.dataCollection}

        if self.otherParameters:
            result.update(self.otherParameters)

        return result


@dataclass
class SciCat:
    dataFormat: str = field(default=None)
    sourceFolder: str = field(default=None)
    datasetName: str = field(default=None)
    description: str = field(default=None)
    owner: str = field(default=None)
    ownerEmail: str = field(default=None)
    isPublished: str = field(default=None)
    type: str = field(default=None)
    principleInvestigator: str = field(default=None)
    creationLocation: str = field(default=None)
    ownerGroup: str = field(default=None)
    scientificMetadata: ScientificMetadata = field(default=None)
    otherFields: Optional[dict] = field(default=None)

    def __post_init__(self):
        if self.scientificMetadata is None:
            raise ValueError("Scientific Metadata cannot be None")

    def collect(self):
        result = {}

        for k, v in asdict(self).items():
            if v is not None and k not in ["otherFields", "scientificMetadata"]:
                result[k] = str(v)

        if self.scientificMetadata is not None:
            result["scientificMetadata"] = self.scientificMetadata.collect()

        if self.otherFields is not None:
            result.update({k: str(v) for k, v in self.otherFields.items()})

        return result

    def to_json(self, filepath=None, indent=4):
        data = self.collect()
        if filepath:
            with open(filepath, "w") as f:
                json.dump(data, f, indent=indent)
        else:
            return json.dumps(data, indent=indent)
