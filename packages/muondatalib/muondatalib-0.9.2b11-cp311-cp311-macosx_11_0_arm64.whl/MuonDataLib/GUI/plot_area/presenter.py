from MuonDataLib.GUI.presenter_template import PresenterTemplate
from MuonDataLib.GUI.plot_area.view import PlotAreaView
import plotly
from plotly.subplots import make_subplots


class PlotAreaPresenter(PresenterTemplate):
    """
    A class for the plotting widget's presenter.
    This follows the MVP pattern.
    """

    def __init__(self):
        """
        Creates a Plot Area Presenter.
        """
        self._view = PlotAreaView(self)

    def plot(self, x1, y1, x2, y2):
        """
        Creates a plot with 2 subplots.
        :param x1: the x values for the first subplot
        :param y1: the y values for the first subplot
        :param x2: the x values for the second subplot
        :param y2: the y values for the second subplot
        :returns: the updated figure object
        """
        # for now lets fix it to 2 subplots
        self.n_rows = 2
        self.n_cols = 1

        x = [x1, x2]
        y = [y1, y2]

        y_labels = ["Field (filtered)", "Temp (unfiltered)"]

        # create the subplots with a shared x axis.
        fig = make_subplots(rows=self.n_rows,
                            cols=self.n_cols,
                            x_title='time',
                            shared_xaxes=True,
                            vertical_spacing=0.02,
                            start_cell='top-left')

        self._height = 900
        fig.update_layout(height=self._height)

        # add data to the subplots
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                # plot lines as this is much faster than points
                fig.add_trace(plotly.graph_objects.Scatter(
                        x=x[i],
                        y=y[i],
                        name=f'Example plot: {y_labels[i]}',
                        mode='lines'
                        ),
                              i + 1, j + 1)
                fig.update_yaxes(title_text=y_labels[i], row=i+1, col=j+1)
        return fig
