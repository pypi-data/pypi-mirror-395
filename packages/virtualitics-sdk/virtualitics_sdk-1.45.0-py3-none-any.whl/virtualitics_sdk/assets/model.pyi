from predict_backend.validation.type_validation import validate_types
from typing import Any
from virtualitics_sdk.assets.asset import Asset as Asset, AssetType as AssetType

class Model(Asset):
    '''The model asset is a wrapper for machine learning models. Accessing attributes and member functions of
    the model asset also passes through access to the underlying machine learning model. 
    
    :param model: The machine learning model that this asset keeps track of.
    :param label: Label of :class:`~virtualitics_sdk.assets.asset.Asset`, see its documentation for more details.
    :param metadata: Metadata of :class:`~virtualitics_sdk.assets.asset.Asset`, see its documentation for more details. Defaults to None.
    :param name: Name of :class:`~virtualitics_sdk.assets.asset.Asset`, see its documentation for more details. Defaults to None.
    :param description: Description of :class:`~virtualitics_sdk.assets.asset.Asset`, see its documentation for more details. Defaults to None.
    :param version: Version of :class:`~virtualitics_sdk.assets.asset.Asset`, see its documentation for more details. Defaults to 0.

    **EXAMPLE:**

       .. code-block:: python

           # Imports 
           from virtualitics_sdk import Model
           from sklearn.linear_model import LogisticRegression
           . . .
           # Example usage
           X = np.random.rand(10).reshape(-1, 1)
           Y = np.random.randint(0, 2, size=(10, 1))
           model = Model(LogisticRegression(), label="test", name="model")
           model.fit(X, Y)


    Additionally, for specific packages the model asset stores hyperparameter information and the time it took 
    to run certain model functions. Currently supported packages are xgboost and sklearn.
    '''
    @validate_types
    def __init__(self, model: Any, label: str, metadata: dict | None = None, name: str | None = None, description: str | None = None, version: int | None = None, **kwargs: Any) -> None: ...
    def update_model_notes(self) -> None:
        """This function updates the asset's stored metadata about the model.
        """
    def get_all_metainfo(self) -> dict:
        """Returns the dictionary containing the model metadata.

        :return: Model metadata, including hyperparameters and times taken for last function calls.
        """
    def get_time(self, attr: str) -> str | None:
        """Returns the last time taken to run the function named attr. The function needs to have been
        called on the model asset rather than the underlying ML model in order for the time to be recorded.
        Returns None if no time was found.

        :param attr: The name of the function to find the time taken.
        :return: The time taken in seconds as a float. If no time is found, returns None instead.
        """
    def get_recent_time(self):
        """Returns the time taken for the most recent function which had its time recorded.
        
        :return: The time taken in seconds as a float. If no time is found, returns None instead.
        """
    def __getattr__(self, attr): ...
    def __setattr__(self, name: str, value): ...
