import plotly.graph_objects as go


class Figure(object):
    """
    A simple class to make plotting easier.
    Uses plotly under the hood.
    """
    def __init__(self, title='',
                 x_label='time (micro seconds)',
                 y_label='Counts (per micro second)'):
        """
        Creates a figure for plotting.
        :param title: the title for the plot.
        :param x_label: the x label for the plot.
        :param y_label: the y label for the plot.
        """

        self._fig = go.Figure()
        self._fig.update_layout(title=title,
                                xaxis_title=x_label,
                                yaxis_title=y_label)

    def plot(self, bin_centres, y_values, label):
        """
        Adds data to the plot as point data.
        :param bin_centres: the bin centres
        :param y_values: the y values for the histogram
        :param label:  the label for the line
        """
        self._fig.add_trace(go.Scatter(x=bin_centres,
                                       y=y_values,
                                       mode='lines+markers',
                                       name=label))

    def show(self):
        """
        Shows the figure (opens in browser)
        """
        self._fig.show()

    def plot_peak_property_histogram(self,
                                     hist,
                                     bins,
                                     label=''):
        """
        Plots the histogram of a peak property
        :param hist: the histogram
        :param bins: the histogram bins.
        """
        bin_centres = (bins[:-1] + bins[1:])/2.
        self.plot(bin_centres, hist,
                  label)

    def plot_from_histogram(self,
                            bins,
                            hist,
                            det_list,
                            label='',
                            period=1):
        """
        Plots the data from an instrument
        :param bins: the histogram bins.
        :param hist: the histogram matrix
        :param det_list: list of the detectors to plot
        :param period: the period to plot (start at 1)
        """
        bin_centres = (bins[:-1] + bins[1:])/2.
        for det in det_list:
            self.plot(bin_centres, hist[period-1][det],
                      label + f'Detector {det}')

    def plot_sample_log(self, muon_data, log_name):
        """
        Plots the current and original sample log data
        :param muon_data: the muon_data object with sample log
        :param log_name: the name of the sample log to plot
        """
        log = muon_data._get_sample_log(log_name)
        x0, y0 = log.get_original_values()
        self.plot(x0, y0, 'original data')
        x_filter, y_filter = log.get_values()
        self.plot(x_filter, y_filter, 'filtered values')
