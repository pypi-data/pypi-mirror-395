import numpy as np
import matplotlib.pyplot as plt
from functools import wraps

from MPSPlots.styles import mps as plot_style


def post_mpl_plot(function):
    extra_doc = """
    Extra Parameters
    ----------------
    show : bool
        Whether to display the plot after creation.
    save_as : str, optional
        If provided, save the figure to this path.
    figure_size : tuple, optional
        Size of the figure in inches.
    tight_layout : bool, default=True
        Whether to use tight layout for the figure.
    axes : matplotlib.axes.Axes, optional
        Axes to draw on. If None, a new figure+axes are created.
    xscale : str, optional
        X-axis scale type (e.g., 'linear', 'log').
    yscale : str, optional
        Y-axis scale type (e.g., 'linear', 'log').
    xlim : tuple, optional
        X-axis limits as (min, max).
    ylim : tuple, optional
        Y-axis limits as (min, max).
    style : str, default=plot_style
        Matplotlib style to use for the plot.
    **kwargs
        Additional keyword arguments to pass to the plotting function.

    Returns
    -------
    Figure : matplotlib.figure.Figure
        The figure with the market prices plot.
    """
    @wraps(function)
    def wrapper(
        *args,
        tight_layout: bool = True,
        save_as: str = None,
        show: bool = True,
        xscale: str = None,
        yscale: str = None,
        xlim: tuple = None,
        ylim: tuple = None,
        figure_size: tuple = None,
        style: str = plot_style,
        **kwargs):


        with plt.style.context(style):
            figure = function(*args, **kwargs)

            # Apply axis customizations
            axes = np.ravel(figure.axes)

            all_axes = axes if isinstance(axes, np.ndarray) else [axes]
            for ax in all_axes:
                if xscale:
                    ax.set_xscale(xscale)
                if yscale:
                    ax.set_yscale(yscale)
                if xlim:
                    ax.set_xlim(*xlim)
                if ylim:
                    ax.set_ylim(*ylim)

            if figure_size is not None:
                figure.set_figwidth(figure_size[0])
                figure.set_figheight(figure_size[1])

            if tight_layout:
                figure.tight_layout()

            if save_as is not None:
                figure.savefig(save_as, dpi=300)

            if show:
                plt.show()

            return figure

    # merge docstrings (original + extra)
    if function.__doc__:
        wrapper.__doc__ = f"{function.__doc__}\n{extra_doc}"
    else:
        wrapper.__doc__ = extra_doc
    return wrapper


def pre_plot(nrows: int = 1, ncols: int = 1, subplot_kw: dict = {}, gridspec_kw: dict = {}, sharex: bool = False, sharey: bool = False):
    """
    Decorator factory that creates a matplotlib figure with subplots
    before calling the decorated plotting function.

    Parameters
    ----------
    nrows : int
        Number of subplot rows.
    ncols : int
        Number of subplot columns.
    """
    def decorator(function):
        extra_doc = """
        Extra Parameters
        ----------------
        show : bool
            Whether to display the plot after creation.
        save_as : str, optional
            If provided, save the figure to this path.
        figure_size : tuple, optional
            Size of the figure in inches.
        tight_layout : bool, default=True
            Whether to use tight layout for the figure.
        axes : matplotlib.axes.Axes, optional
            Axes to draw on. If None, a new figure+axes are created.
        xscale : str, optional
            X-axis scale type (e.g., 'linear', 'log').
        yscale : str, optional
            Y-axis scale type (e.g., 'linear', 'log').
        xlim : tuple, optional
            X-axis limits as (min, max).
        ylim : tuple, optional
            Y-axis limits as (min, max).
        style : str, default=plot_style
            Matplotlib style to use for the plot.
        **kwargs
            Additional keyword arguments to pass to the plotting function.

        Returns
        -------
        axes : matplotlib.axes.Axes
            The axes with the market prices plot.
        """

        @wraps(function)
        def wrapper(*args,
                    show: bool = True,
                    save_as: str = None,
                    figure_size: tuple = None,
                    tight_layout: bool = True,
                    axes: plt.Axes = None,
                    xscale: str = None,
                    yscale: str = None,
                    xlim: tuple = None,
                    ylim: tuple = None,
                    style: str = plot_style,
                    **kwargs):

            with plt.style.context(style):
                if axes is None:
                    figure, axes = plt.subplots(
                        nrows=nrows,
                        ncols=ncols,
                        figsize=figure_size,
                        squeeze=False,
                        subplot_kw=subplot_kw,
                        gridspec_kw=gridspec_kw,
                        sharex=sharex,
                        sharey=sharey
                    )
                else:
                    figure = axes.get_figure()

                axes = np.array(axes).flatten()
                if nrows * ncols == 1:
                    axes = axes[0]

                # Call the decorated function
                if args and hasattr(args[0], "__class__"):
                    function(args[0], axes=axes, *args[1:], **kwargs)
                else:
                    function(*args, axes=axes, **kwargs)

                # Apply axis customizations
                all_axes = axes if isinstance(axes, np.ndarray) else [axes]
                for ax in all_axes:
                    if xscale:
                        ax.set_xscale(xscale)
                    if yscale:
                        ax.set_yscale(yscale)
                    if xlim:
                        ax.set_xlim(*xlim)
                    if ylim:
                        ax.set_ylim(*ylim)

                if tight_layout:
                    figure.tight_layout()

                if save_as is not None:
                    figure.savefig(save_as, dpi=300)

                if show:
                    plt.show()

                return figure

        # merge docstrings (original + extra)
        if function.__doc__:
            wrapper.__doc__ = f"{function.__doc__}\n{extra_doc}"
        else:
            wrapper.__doc__ = extra_doc
        return wrapper


    return decorator


def pre_figure_plot():
    """
    Decorator factory that creates a matplotlib figure with subplots
    before calling the decorated plotting function.

    Parameters
    ----------
    nrows : int
        Number of subplot rows.
    ncols : int
        Number of subplot columns.
    """
    def decorator(function):
        extra_doc = """
        Extra Parameters
        ----------------
        show : bool
            Whether to display the plot after creation.
        save_as : str, optional
            If provided, save the figure to this path.
        figure_size : tuple, optional
            Size of the figure in inches.
        tight_layout : bool, default=True
            Whether to use tight layout for the figure.
        axes : matplotlib.axes.Axes, optional
            Axes to draw on. If None, a new figure+axes are created.
        xscale : str, optional
            X-axis scale type (e.g., 'linear', 'log').
        yscale : str, optional
            Y-axis scale type (e.g., 'linear', 'log').
        xlim : tuple, optional
            X-axis limits as (min, max).
        ylim : tuple, optional
            Y-axis limits as (min, max).
        style : str, default=plot_style
            Matplotlib style to use for the plot.
        **kwargs
            Additional keyword arguments to pass to the plotting function.

        Returns
        -------
        axes : matplotlib.axes.Axes
            The axes with the market prices plot.
        """

        @wraps(function)
        def wrapper(*args,
                    show: bool = True,
                    save_as: str = None,
                    figure_size: tuple = None,
                    tight_layout: bool = True,
                    axes: plt.Axes = None,
                    xscale: str = None,
                    yscale: str = None,
                    xlim: tuple = None,
                    ylim: tuple = None,
                    style: str = plot_style,
                    **kwargs):

            with plt.style.context(style):


                # Call the decorated function
                if args and hasattr(args[0], "__class__"):
                    figure = function(args[0], *args[1:], **kwargs)
                else:
                    figure = function(*args, **kwargs)

                # Apply axis customizations
                all_axes = axes if isinstance(axes, np.ndarray) else [axes]
                for ax in all_axes:
                    if xscale:
                        ax.set_xscale(xscale)
                    if yscale:
                        ax.set_yscale(yscale)
                    if xlim:
                        ax.set_xlim(*xlim)
                    if ylim:
                        ax.set_ylim(*ylim)

                if tight_layout:
                    figure.tight_layout()

                if save_as is not None:
                    figure.savefig(save_as, dpi=300)

                if show:
                    plt.show()

                return figure

        # merge docstrings (original + extra)
        if function.__doc__:
            wrapper.__doc__ = f"{function.__doc__}\n{extra_doc}"
        else:
            wrapper.__doc__ = extra_doc
        return wrapper


    return decorator


def add_inset(ax: plt.Axes, x_lim: tuple = None, y_lim: tuple = None, zoom: float = 2., loc: str = "upper center"):

    from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset

    axins = zoomed_inset_axes(ax, zoom=zoom, loc=loc)

    axins.set_xticks([])
    axins.set_yticks([])

    for line in ax.lines:
        axins.plot(
            *line.get_data(),
            color=line.get_color(),
            marker=line.get_marker(),
            label=line.get_label(),
            linestyle=line.get_linestyle(),
            linewidth=line.get_linewidth(),
        )

    for collection in ax.collections:
        verts = collection.get_paths()[0].vertices
        x_fill, y_fill = verts[:, 0], verts[:, 1]

        axins.fill_between(
            x_fill,
            0,
            y_fill,
            alpha=collection.get_alpha(),
            color=collection.get_facecolor(),
            label=collection.get_label()
        )

    mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")

    if x_lim is not None:
        axins.set_xlim(x_lim)

    if y_lim is not None:
        axins.set_ylim(y_lim)

    return axins