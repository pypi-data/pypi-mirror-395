import numpy as np
import pandas as pd
from _typeshed import Incomplete
from predict_backend.validation.type_validation import validate_types
from virtualitics_sdk.assets.asset import Asset as Asset, AssetType as AssetType

class Schema(Asset):
    '''
        A schema asset allows validation of a DataFrame according to a pre-specified schema. A schema is specified using
        a pd.Series object with indices names as expected columns in the dataframe and values as their expected dtypes.
        There are 2 levels of validation that can be performed. The first "level 1" validation ensures that the dataframe
        contains all the expected columns specified in the schema, and optionally ensures that no additional columns are
        present. It also ensures that each column\'s dtype matches the schema. The optional "level 2" validation performs additional checks,
        ensuring that numerical columns are within a specified range of values and that categorical columns take on a value
        from a specified list. In the event that a check fails, an exception is raised. Otherwise the validation function
        returns true.

        :param schema: A schema object. Indices should be expected column names and values should be expected dtypes.
        :param exact_match: If true, the dataframe must not have any additional columns not expected in the schema or else an
                                    exception will be raised. If performing level 2 validation, the \'valid_inputs\' variable must have
                                    key/value entries for each column in the schema. If false, these checks will be ignored.
        :param valid_inputs: A dictionary mapping column names (str) to lists describing their valid inputs.
                                    For columns with a numerical dtype, the value is expected to be [min, max] where min and max
                                    is the minimum and maximum possible values in the column respectively. For columns with a "object"
                                    dtype (i.e. string/categorical columns) the value is expected to be a list of all possible
                                    values in the column. If valid_inputs is None, this level 2 validation will not be performed.
        :param label: Label for :class:`~virtualitics_sdk.assets.asset.Asset`, see its documentation for more details.
        :param metadata: Metadata for :class:`~virtualitics_sdk.assets.asset.Asset`, see its documentation for more details.
        :param name: Name for :class:`~virtualitics_sdk.assets.asset.Asset`, see its documentation for more details.
        :param description: Description of :class:`~virtualitics_sdk.assets.asset.Asset`, see its documentation for more details.
        :param version: Version for :class:`~virtualitics_sdk.assets.asset.Asset`, see its documentation for more details.
    '''
    exact_match: Incomplete
    do_level_2: Incomplete
    valid_inputs: Incomplete
    col_to_dtype: Incomplete
    @validate_types
    def __init__(self, schema: pd.Series | None = None, exact_match: bool = False, valid_inputs: dict[str, list] | None = None, label: str | None = None, metadata: dict | None = None, name: str | None = None, description: str | None = None, version: int | None = None, **kwargs) -> None: ...
    def validate(self, df: pd.DataFrame) -> bool: ...
    def validate_level_1(self, df: pd.DataFrame) -> bool: ...
    def validate_level_2(self, df: pd.DataFrame) -> bool: ...
    def convert_strings_to_dtype(self, arr: np.array): ...
