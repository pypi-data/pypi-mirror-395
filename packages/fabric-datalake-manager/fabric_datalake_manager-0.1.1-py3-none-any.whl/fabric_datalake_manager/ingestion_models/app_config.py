from typing import List

from fabric_datalake_manager.interfaces.log_interface import ILog
from fabric_datalake_manager.interfaces.validate_interface import IValidate
from fabric_datalake_manager.interfaces.config_interface import ILakeConfig
from fabric_datalake_manager.interfaces.transform_interface import ITransform


class LayerConfiguration:
    def __init__(
        self,
        config: ILakeConfig,
        validators: List[IValidate] = None,
        transformers: List[ITransform] = None
    ):
        self.config: ILakeConfig = config
        self.validators: List[IValidate] = validators
        self.transformers: List[ITransform] = transformers


class Configuration:
    bronze: LayerConfiguration = None
    silver: LayerConfiguration = None
    gold: LayerConfiguration = None

    wh_name: str = None

    loggers: List[ILog] = None
