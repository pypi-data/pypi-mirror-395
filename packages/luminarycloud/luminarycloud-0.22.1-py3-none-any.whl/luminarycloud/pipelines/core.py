# Copyright 2025 Luminary Cloud, Inc. All Rights Reserved.
from abc import ABC, abstractmethod
from dataclasses import is_dataclass, fields
from typing import Any, Type, TypeVar, Generic
from typing_extensions import Self
import re
import yaml

from ..pipeline_util.yaml import ensure_yamlizable


class PipelineParameterRegistry:
    def __init__(self):
        self.parameters = {}

    def register(self, parameter_class: Type["PipelineParameter"]) -> None:
        self.parameters[parameter_class._type_name()] = parameter_class

    def get(self, type_name: str) -> Type["PipelineParameter"]:
        if type_name not in self.parameters:
            raise ValueError(f"Unknown parameter type: {type_name}")
        return self.parameters[type_name]


class PipelineParameter(ABC):
    """
    Base class for all concrete PipelineParameters.
    """

    def __init__(self, name: str):
        self.name = name
        self._validate()

    @property
    def type(self) -> str:
        return self.__class__._type_name()

    @classmethod
    @abstractmethod
    def _represented_type(cls) -> Type:
        pass

    @classmethod
    @abstractmethod
    def _type_name(cls) -> str:
        pass

    def _validate(self) -> None:
        if not re.match(r"^[a-zA-Z0-9_-]+$", self.name):
            raise ValueError(
                "name must only contain alphanumeric characters, underscores and hyphens"
            )

    def _add_to_params(self, params: dict) -> None:
        if self.name in params and params[self.name]["type"] != self.type:
            raise ValueError(
                f"Parameter name {self.name} used with multiple types: {params[self.name]['type']} != {self.type}"
            )
        params[self.name] = {"type": self.type}

    def _to_pipeline_dict(self) -> tuple[dict, list["PipelineParameter"]]:
        return {"$pipeline_param": self.name}, [self]

    def __str__(self) -> str:
        return f'{self.__class__.__name__}(name="{self.name}")'

    _registry = PipelineParameterRegistry()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        PipelineParameter._registry.register(cls)

    @classmethod
    def _get_subclass(cls, parameter_type: str) -> Type["PipelineParameter"]:
        return cls._registry.get(parameter_type)

    def _is_valid_value(self, value: Any) -> bool:
        return isinstance(value, self._represented_type())

    def __hash__(self) -> int:
        return hash((self.type, self.name))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PipelineParameter):
            return False
        return self.__hash__() == other.__hash__()


class PipelineInput:
    """
    A named input for a Stage. Explicitly connected to a PipelineOutput.
    """

    def __init__(self, upstream_output: "PipelineOutput", owner: "Stage", name: str):
        self.upstream_output = upstream_output
        self.owner = owner
        self.name = name

    def _to_dict(self, id_for_stage: dict) -> dict:
        if self.upstream_output.owner not in id_for_stage:
            raise ValueError(
                f"Stage {self.owner} depends on a stage, {self.upstream_output.owner}, that isn't in the Pipeline. Did you forget to add it?"
            )
        upstream_stage_id = id_for_stage[self.upstream_output.owner]
        upstream_output_name = self.upstream_output.name
        return {self.name: f"{upstream_stage_id}.{upstream_output_name}"}


class PipelineOutput(ABC):
    """
    A named output for a Stage. Can be used to spawn any number of connected PipelineInputs.
    """

    def __init__(self, owner: "Stage", name: str):
        self.owner = owner
        self.name = name
        self.downstream_inputs: list[PipelineInput] = []

    def _spawn_input(self, owner: "Stage", name: str) -> PipelineInput:
        input = PipelineInput(self, owner, name)
        self.downstream_inputs.append(input)
        return input


class StageInputs:
    """
    A collection of all PipelineInputs for a Stage.
    """

    def __init__(
        self, owner: "Stage", **input_descriptors: tuple[Type[PipelineOutput], PipelineOutput]
    ):
        """
        input_descriptors is a dict of input name -> (required_upstream_output_type, upstream_output)
        We have that required_upstream_output_type so we can do runtime validation that each given
        output is of the correct type for the input it's hooked up to.
        """
        self.inputs: set[PipelineInput] = set()
        for name, (required_upstream_output_type, upstream_output) in input_descriptors.items():
            if not isinstance(upstream_output, required_upstream_output_type):
                raise ValueError(
                    f"Input {name} must be a {required_upstream_output_type.__name__}, got {upstream_output.__class__.__name__}"
                )
            self.inputs.add(upstream_output._spawn_input(owner, name))

    def _to_dict(self, id_for_stage: dict) -> dict[str, str]:
        d: dict[str, str] = {}
        for input in self.inputs:
            d |= input._to_dict(id_for_stage)
        return d


T = TypeVar("T", bound="StageOutputs")


class StageOutputs(ABC):
    """
    A collection of all PipelineOutputs for a Stage. Must be subclassed, and the subclass must also
    be a dataclass whose fields are all PipelineOutput subclasses. Then that subclass should be
    instantiated with `_instantiate_for`. Sounds a little complicated, perhaps, but it's not bad.
    See the existing subclasses in `./stages.py` for examples.
    """

    @classmethod
    def _instantiate_for(cls: type[T], owner: "Stage") -> T:
        # create an instance with all fields instantiated with the given owner, and named by the
        # field name.
        # Also validate here that we are a dataclass, and all our fields are PipelineOutput types.
        # Would love to get this done in the type system, but I think it's impossible, so this is
        # the next best thing.
        if not is_dataclass(cls):
            raise TypeError(f"'{cls.__name__}' must be a dataclass")
        outputs = {}
        for field in fields(cls):
            assert not isinstance(field.type, str)
            if not issubclass(field.type, PipelineOutput):
                raise TypeError(
                    f"Field '{field.name}' in '{cls.__name__}' must be a subclass of PipelineOutput"
                )
            outputs[field.name] = field.type(owner, field.name)
        return cls(**outputs)

    def downstream_inputs(self) -> list[PipelineInput]:
        inputs = []
        for field in fields(self):
            inputs.extend(getattr(self, field.name).downstream_inputs)
        return inputs


class StageRegistry:
    def __init__(self):
        self.stages = {}

    def register(self, stage_class: Type["Stage"]) -> None:
        self.stages[stage_class.__name__] = stage_class

    def get(self, stage_type_name: str) -> Type["Stage"]:
        if stage_type_name not in self.stages:
            raise ValueError(f"Unknown stage type: {stage_type_name}")
        return self.stages[stage_type_name]


TOutputs = TypeVar("TOutputs", bound=StageOutputs)


class Stage(Generic[TOutputs], ABC):
    def __init__(
        self,
        stage_name: str | None,
        params: dict,
        inputs: StageInputs,
        outputs: TOutputs,
    ):
        self._stage_type_name = self.__class__.__name__
        self._name = stage_name if stage_name is not None else self._stage_type_name
        self._params = params
        self._inputs = inputs
        self.outputs = outputs
        ensure_yamlizable(self._params_dict()[0], "Stage parameters")

    def is_source(self) -> bool:
        return len(self._inputs.inputs) == 0

    def inputs_dict(self) -> dict[str, tuple["Stage", str]]:
        inputs = {}
        for pipeline_input in self._inputs.inputs:
            inputs[pipeline_input.name] = (
                pipeline_input.upstream_output.owner,
                pipeline_input.upstream_output.name,
            )
        return inputs

    def downstream_stages(self) -> list["Stage"]:
        return [input.owner for input in self.outputs.downstream_inputs()]

    def _to_dict(self, id_for_stage: dict) -> tuple[dict, set[PipelineParameter]]:
        params, pipeline_params_set = self._params_dict()
        d = {
            "name": self._name,
            "operator": self._stage_type_name,  # TODO: change key to "stage_type" when we're ready to bump the yaml schema version
            "params": params,
            "inputs": self._inputs._to_dict(id_for_stage),
        }
        return d, pipeline_params_set

    def _params_dict(self) -> tuple[dict, set[PipelineParameter]]:
        d = {}
        pipeline_params = set()
        for name, value in self._params.items():
            if hasattr(value, "_to_pipeline_dict"):
                d[name], downstream_params = value._to_pipeline_dict()
                for param in downstream_params:
                    if not isinstance(param, PipelineParameter):
                        raise ValueError(
                            f"Expected `_to_pipeline_dict()` to only return PipelineParameters, but got a {type(param)}: {param}"
                        )
                pipeline_params.update(downstream_params)
            else:
                d[name] = value
        # Strip None values. We treat absence of a param value in the YAML the same as a present null value.
        d = {k: v for k, v in d.items() if v is not None}
        return d, pipeline_params

    def __str__(self) -> str:
        return f'{self._stage_type_name}(name="{self._name}")'

    _registry = StageRegistry()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Stage._registry.register(cls)

    @classmethod
    def _get_subclass(cls, stage_type_name: str) -> Type["Stage"]:
        return cls._registry.get(stage_type_name)

    @classmethod
    def _parse_params(cls, params: dict) -> dict:
        # Stages with params that are just primitives or PipelineParams have no parsing to do.
        # Stages with more complicated params should override this method.
        return params


class Pipeline:
    def __init__(self, stages: list[Stage]):
        self.stages = stages
        self._stage_ids = self._assign_ids_to_stages()

    def to_yaml(self) -> str:
        return yaml.safe_dump(self._to_dict())

    def pipeline_params(self) -> set[PipelineParameter]:
        return self._stages_dict_and_params()[1]

    def get_stage_id(self, stage: Stage) -> str:
        return self._stage_ids[stage]

    def _stages_dict_and_params(self) -> tuple[dict, set[PipelineParameter]]:
        id_for_stage = self._stage_ids
        stages = {}
        params = set()
        for stage in id_for_stage.keys():
            stage_dict, referenced_params = stage._to_dict(id_for_stage)
            stages[id_for_stage[stage]] = stage_dict
            params.update(referenced_params)
        return stages, params

    def _to_dict(self) -> dict:
        stages, params = self._stages_dict_and_params()

        d = {
            "lc_pipeline": {
                "schema_version": 1,
                "params": self._pipeline_params_dict(params),
                "tasks": stages,  # TODO: change key to "stages" when we're ready to bump the yaml schema version
            }
        }
        ensure_yamlizable(d, "Pipeline")
        return d

    def _assign_ids_to_stages(self) -> dict[Stage, str]:
        return {stage: f"s{i + 1}-{stage._stage_type_name}" for i, stage in enumerate(self.stages)}

    def _pipeline_params_dict(self, params: set[PipelineParameter]) -> dict:
        d: dict[str, dict] = {}
        for p in params:
            if p.name in d and d[p.name]["type"] != p.type:
                raise ValueError(
                    f'PipelineParameter "{p.name}" used with multiple types: {d[p.name]["type"]} != {p.type}'
                )
            d[p.name] = {"type": p.type}
        return d

    @classmethod
    def _from_yaml(cls, yaml_str: str) -> Self:
        d = yaml.safe_load(yaml_str)
        if "lc_pipeline" not in d:
            raise ValueError("Invalid pipeline YAML: missing 'lc_pipeline' key")

        d = d["lc_pipeline"]
        if "schema_version" not in d:
            raise ValueError("Invalid pipeline YAML: missing 'schema_version' key")
        if (
            "tasks" not in d
        ):  # TODO: change key to "stages" when we're ready to bump the yaml schema version
            raise ValueError("Invalid pipeline YAML: missing 'tasks' key")

        if d["schema_version"] != 1:
            raise ValueError(f"Unsupported schema version: {d['schema_version']}")

        # first, parse the pipeline parameters...
        parsed_params = {}
        for param_name, param_metadata in d.get("params", {}).items():
            parsed_params[param_name] = PipelineParameter._get_subclass(param_metadata["type"])(
                param_name
            )

        # ...and use them as replacements for any references in the stages' parameters
        for stage_dict in d[
            "tasks"
        ].values():  # TODO: change key to "stages" when we're ready to bump the yaml schema version
            stage_dict["params"] = _recursive_replace_pipeline_params(
                stage_dict["params"], parsed_params
            )

        # then, finish parsing the stages
        parsed_stages = {}
        for stage_id in d["tasks"]:
            _parse_stage(d, stage_id, parsed_stages)

        pipe = cls(list(parsed_stages.values()))
        # Preserve the stage IDs from the YAML definition by overwriting the auto-assigned ones
        pipe._stage_ids = {stage: stage_id for stage_id, stage in parsed_stages.items()}
        return pipe


def _recursive_replace_pipeline_params(d: Any, parsed_params: dict) -> Any:
    if isinstance(d, dict):
        if "$pipeline_param" in d:
            # d is a dict representation of a PipelineParameter, so return the actual PipelineParameter
            pp_name = d["$pipeline_param"]
            if pp_name not in parsed_params:
                raise ValueError(
                    f'Pipeline parameter "{pp_name}" referenced in a pipeline stage, but not found in pipeline\'s declared parameters'
                )
            return parsed_params[pp_name]
        else:
            return {
                key: _recursive_replace_pipeline_params(value, parsed_params)
                for key, value in d.items()
            }
    elif isinstance(d, list):
        return [_recursive_replace_pipeline_params(item, parsed_params) for item in d]
    else:
        return d


def _parse_stage(pipeline_dict: dict, stage_id: str, all_stages: dict[str, Stage]) -> Stage:
    all_stages_dict = pipeline_dict[
        "tasks"
    ]  # TODO: change key to "stages" when we're ready to bump the yaml schema version
    if stage_id in all_stages:
        return all_stages[stage_id]
    stage_dict = all_stages_dict[stage_id]
    stage_type_name = stage_dict[
        "operator"
    ]  # TODO: change key to "stage_type" when we're ready to bump the yaml schema version
    stage_class = Stage._get_subclass(stage_type_name)

    parsed_inputs = {}
    for input_name, input_value in stage_dict["inputs"].items():
        source_stage_id, source_output_name = input_value.split(".")
        source_stage = _parse_stage(pipeline_dict, source_stage_id, all_stages)
        source_output = getattr(source_stage.outputs, source_output_name)
        parsed_inputs[input_name] = source_output

    parsed_params = stage_class._parse_params(stage_dict["params"])

    stage_params = {
        "stage_name": stage_dict["name"],
        **parsed_params,
        **parsed_inputs,
    }
    stage = stage_class(**stage_params)
    all_stages[stage_id] = stage
    return stage
