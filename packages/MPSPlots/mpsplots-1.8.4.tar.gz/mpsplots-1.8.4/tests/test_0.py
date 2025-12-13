import pytest
import numpy
import matplotlib.pyplot as plt

from MPSPlots import helper


def test_dummy():
    @helper.post_mpl_plot
    def _plot():
        figure, axes = plt.subplots(1, 1)
        x = numpy.arange(0, 100)
        y = 2 * x**2
        axes.plot(x, y)

        return figure

    _plot(show=True, yscale='log')


if __name__ == "__main__":
    pytest.main(["-W error", "-s", __file__])