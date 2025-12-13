from _typeshed import Incomplete
from plotly import graph_objects
from predict_backend.validation.type_validation import validate_types
from virtualitics_sdk.elements.element import Element as Element

PREDICT_PLOT_DEFAULT_COLORWAY: Incomplete
PREDICT_PLOT_DIVERGING_COLORSCALE: Incomplete
PREDICT_PLOT_SEQUENTIAL_COLORSCALE: Incomplete
PREDICT_PLOT_SEQUENTIAL_MINUS_COLORSCALE: Incomplete

class PlotlyPlot(Element):
    '''Create a plot using the Plotly package. On creation, the Plotly plot title will be remove and made into a VAIP title. 
    To use the  Virtualitics color scheme in Plotly plots simply add ``template="predict_default"`` to the Plotly layout object
    and have the imported virtualitics_sdk plotly_plot module.
    
    NOTE: Plotly plot title will be removed and made into a VAIP title
    
    More on Plotly documentation can be found here: https://plotly.com/python/

    :param fig: A Plotly figure object
    :param title: The title of the PlotlyPlot, if not specified, the title of object Plotly is used.
    :param show_title: Whether to show the title on the page when rendered, defaults to True.
    :param description: The element\'s description, defaults to \'\'.
    :param show_description: Whether to show the description to the page when rendered, defaults to True.
    :param reference_id: A user-defined reference ID for the unique identification of PlotlyPlot element within the
                        Page, defaults to \'\'.
    :param info_content: Description to be displayed within the element\'s info button. Use RichText/Markdown for 
                         advanced formatting.

    **EXAMPLE:**

       .. code-block:: python
           
           # Imports 
           from virtualitics_sdk import PlotlyPlot
           . . .
           # Example usage
           class ExampleStep(Step):
             def run(self, flow_metadata):
               . . .
               fig_1 = px.scatter(ex_df,
                                  x="gdpPercap", 
                                  y="lifeExp", 
                                  size="pop", 
                                  color="continent",
                                  log_x=True, size_max=60,
                                  template="predict_default", 
                                  title="Gapminder 2007 - Predict")
               fig_2 = px.scatter(ex_df,
                                  x="gdpPercap", 
                                  y="lifeExp", 
                                  size="pop", 
                                  color="continent",
                                  log_x=True, 
                                  size_max=60, 
                                  title="Gapminder 2007 - Default")
               pplot_1 = PlotlyPlot(fig_1)
               pplot_2 = PlotlyPlot(fig_2)

    The above PlotlyPlot will be displayed as:      

       .. image:: ../images/plotly_plot_ex.png
          :align: center
    '''
    fig: Incomplete
    id: Incomplete
    type: str
    title: Incomplete
    reference_id: Incomplete
    show_title: Incomplete
    description: Incomplete
    show_description: Incomplete
    info_content: Incomplete
    @validate_types
    def __init__(self, fig: graph_objects.Figure, title: str | None = None, show_title: bool = True, description: str = '', show_description: bool = True, reference_id: str | None = '', info_content: str | None = None) -> None: ...
    def to_json(self): ...
