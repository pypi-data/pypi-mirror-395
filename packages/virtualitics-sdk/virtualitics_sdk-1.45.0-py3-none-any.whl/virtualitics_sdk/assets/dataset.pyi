import pandas as pd
from _typeshed import Incomplete
from predict_backend.validation.type_validation import validate_types
from typing import Iterable
from virtualitics_sdk.assets.asset import Asset as Asset, AssetType as AssetType
from virtualitics_sdk.utils.types import ExtendedEnum as ExtendedEnum, object_t as object_t

logger: Incomplete

class DataEncoding(ExtendedEnum):
    ORDINAL: str
    ONE_HOT: str
    VERBOSE: str

class Dataset(Asset):
    '''
    The dataset asset allows for easy conversion between data formats when it is provided with additional inputs to
    convert between formats.
    
    :param dataset: A dataset containing numerical and categorical columns. Should be given as a pandas DataFrame.
    :param label: Label for Asset. See Asset documentation for more details.
    :param metadata: Asset metadata. See asset documentation for more details.
    :param name: Name for Asset. See Asset documentation for more details.
    :param encoding: DataEncoding enum to specify the data type of the given dataset. Possible values are `ordinal`,`one_hot`, or `verbose`. These types refer to the format of categorical features. `ordinal` means that categories are contained only in a single column and encoded  with integers. `verbose` is the same format, but encoded with strings instead of integers. `one_hot` means categorical features are split up into columns for each possible value using a one-hot-encoding methodology.
    :param one_hot_dict: Allows conversion to and from \'one_hot\' encoding. This is a dictionary mapping from names of categorical features to a list of strings of the columns in the dataset which correspond to the given feature. If not provided and the dataset is given in a one hot encoding, attempts to create one_hot_dict assuming that the columns were created using pd.get_dummies.
    :param cat_to_vals: This is a dictionary mapping from names of categorical features to a list of strings representing their possible values. Even if not provided, one is inferred from the given dataset.
    :param categorical_cols: A list of strings representing the feature names of the category features. For an ordinal or verbose encoded dataset, it would just be the name of the column of the categorical feature. For a one_hot encoded dataset, it would be the corresponding name of the feature.
    :param predict_cols: Names of columns in the dataset that will be used by a model. This allows filtering of the dataframe when passing to a model even if the dataset contains extraneous columns. These columns are expected to match the provided encoding of the dataset.
    :param description: Description of :class:`~virtualitics_sdk.assets.asset.Asset`, see its documentation for more details.
    :param version: Version of :class:`~virtualitics_sdk.assets.asset.Asset`, see its documentation for more details.

    **EXAMPLE:**

       .. code-block:: python
       
           # Imports 
           from virtualitics_sdk import Dataset
           . . .
           # Example usage 
           df = store_interface.get_element_value(data_upload_step.name, "Upload data here!")
           vaip_dataset = Dataset(df, "ExampleDatasetLabel", name="ExampleData")
    '''
    one_hot_dict: Incomplete
    cat_to_vals: Incomplete
    categorical_cols: Incomplete
    predict_cols: Incomplete
    encoding: Incomplete
    @validate_types
    def __init__(self, dataset: pd.DataFrame, label: str, metadata: dict | None = None, name: str | None = None, encoding: str | DataEncoding = 'ordinal', one_hot_dict: dict[str, list[str]] | None = None, cat_to_vals: dict[str, list[object_t]] | None = None, categorical_cols: list[str] | None = None, predict_cols: list[str] | None = None, description: str | None = None, version: int | None = None, **kwargs) -> None: ...
    one_hot_conversion_allowed: Incomplete
    default_encoding: Incomplete
    categorical_names: Incomplete
    verbose_conversion_allowed: Incomplete
    def initialize_encodings(self, encoding: str | DataEncoding, one_hot_dict: dict[str, list[str]] | None = None, cat_to_vals: dict[str, list[object_t]] | None = None, categorical_cols: list[str] | None = None) -> None: ...
    filtering_allowed: bool
    predict_cols_ordinal: Incomplete
    predict_cols_verbose: Incomplete
    predict_cols_one_hot: Incomplete
    def initialize_filters(self, predict_cols: Iterable[str] | None): ...
    def filter_data(self, X: pd.DataFrame, encoding: str | DataEncoding | None = None):
        """Filters columns of the provided dataframe so that they contain only columns used for model prediction. This filtering
        is only possible when this Dataset object was initialized with the `predict_cols` parameter.

        :param X: The dataframe which will be filtered. This dataframe should contain every column specified in the intialization
                  of the `predict_cols` parameter.
        :param encoding: The encoding of the provided dataframe. If None, it assumes the dataframe is in the same encoding as the
                         original provided dataframe. Can also be provided as a string version of the encoding. Defaults to None.
        :return: The filtered dataset.
        """
    def convert_dtypes(self, X: pd.DataFrame):
        """Converts the dtypes of the columns in X to match the dtypes of this asset's dataset object.

        :param X: The dataframe whose dtypes will be converted.
        :return: The same dataframe with converted dtypes.
        """
    def convert_encoding(self, X: pd.DataFrame, from_: str | DataEncoding | None = None, to_: str | DataEncoding | None = None, filter: bool = False) -> pd.DataFrame:
        """Converts the dataframe from and to the specified encodings. The dataframe should be in the encoding specified in `from_`.
        The dataframe can also be concurrently filtered to only contain prediction columns.

        :param X: The dataframe to be converted. Should be in the encoding specified in `from_`. 
        :param from_: The encoding of the provided dataframe. If None, it assumes the dataframe is in the same encoding as the
                      original provided dataframe. Can also be provided as a string version of the encoding. Defaults to None.
        :param to_: The encoding to convert the dataframe to. If None, it assumes the dataframe is in the same encoding as the
                    original provided dataframe. Can also be provided as a string version of the encoding. Defaults to None.
        :param filter: Whether to filter the provided data to only contain prediction columns. Defaults to False.
        :raises ValueError: When either the `from_` or `to_` encodings are not supported for conversion.
        :return: The converted dataframe.
        """
    def check_valid_encoding(self, encoding: str | DataEncoding | None = None) -> DataEncoding:
        """Converts provided encoding to a :class:`~virtualitics_sdk.assets.dataset.DataEncoding` enum. If no encoding
        is provided, defaults to the original encoding of the provided dataframe in initialization.

        :param encoding: The encoding to be validated If None, the functions returns the default encoding provided in initialization.
                         Can also be provided string versions of the encodings. Valid strings are `ordinal`, `one_hot`, and `verbose`. Defaults to None.
        :raises ValueError: If the provided string does not match a valid DataEncoding.
        :return: The corresponding :class:`~virtualitics_sdk.assets.dataset.DataEncoding` enum.
        """
    def get_as_encoding(self, encoding: str | DataEncoding | None = None, filter: bool = False) -> pd.DataFrame:
        """Returns this asset's dataset as the specified encoding. 

        :param encoding: The encoding to convert the dataframe to. If None, it assumes the dataframe is in the same encoding as the
                         original provided dataframe. Can also be provided as a string version of the encoding. Defaults to None.
        :param filter: Whether to filter the provided data to only contain prediction columns. Defaults to False.
        :return: The dataset in the specified encoding, with additional filtering if specified.
        """
    def get_categorical_names(self, predict_cols: bool = False) -> list[str]:
        """Returns the names of the categorical columns of this dataset. Can also optionally return only categorical columns
        which are also prediction columns.

        :param predict_cols: Whether to reduce the set of categorical columns returned to just prediction columns. Defaults to False.
        :return: The list of categorical columns.
        """
