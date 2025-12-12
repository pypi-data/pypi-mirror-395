import matplotlib.pyplot as plt
import numpy as np

# plt.rcParams['text.usetex']=True
plt.rcParams["font.size"] = 10
plt.rcParams["lines.linewidth"] = 2

# list(colormaps)

"""
['magma',
 'inferno',
 'plasma',
 'viridis',
 'cividis',
 'twilight',
 'twilight_shifted',
 'turbo',
 'Blues',
 'BrBG',
 'BuGn',
 'BuPu',
 'CMRmap',
 'GnBu',
 'Greens',
 'Greys',
 'OrRd',
 'Oranges',
 'PRGn',
 'PiYG',
 'PuBu',
 'PuBuGn',
 'PuOr',
 'PuRd',
 'Purples',
 'RdBu',
 'RdGy',
 'RdPu',
 'RdYlBu',
 'RdYlGn',
 'Reds',
 'Spectral',
 'Wistia',
 'YlGn',
 'YlGnBu',
 'YlOrBr',
 'YlOrRd',
 'afmhot',
 'autumn',
 'binary',
 'bone',
 'brg',
 'bwr',
 'cool',
 'coolwarm',
 'copper',
 'cubehelix',
 'flag',
 'gist_earth',
 'gist_gray',
 'gist_heat',
 'gist_ncar',
 'gist_rainbow',
 'gist_stern',
 'gist_yarg',
 'gnuplot',
 'gnuplot2',
 'gray',
 'hot',
 'hsv',
 'jet',
 'nipy_spectral',
 'ocean',
 'pink',
 'prism',
 'rainbow',
 'seismic',
 'spring',
 'summer',
 'terrain',
 'winter',
 'Accent',
 'Dark2',
 'Paired',
 'Pastel1',
 'Pastel2',
 'Set1',
 'Set2',
 'Set3',
 'tab10',
 'tab20',
 'tab20b',
 'tab20c',
 'grey',
 'gist_grey',
 'gist_yerg',
 'Grays',
 'magma_r',
 'inferno_r',
 'plasma_r',
 'viridis_r',
 'cividis_r',
 'twilight_r',
 'twilight_shifted_r',
 'turbo_r',
 'Blues_r',
 'BrBG_r',
 'BuGn_r',
 'BuPu_r',
 'CMRmap_r',
 'GnBu_r',
 'Greens_r',
 'Greys_r',
 'OrRd_r',
 'Oranges_r',
 'PRGn_r',
 'PiYG_r',
 'PuBu_r',
 'PuBuGn_r',
 'PuOr_r',
 'PuRd_r',
 'Purples_r',
 'RdBu_r',
 'RdGy_r',
 'RdPu_r',
 'RdYlBu_r',
 'RdYlGn_r',
 'Reds_r',
 'Spectral_r',
 'Wistia_r',
 'YlGn_r',
 'YlGnBu_r',
 'YlOrBr_r',
 'YlOrRd_r',
 'afmhot_r',
 'autumn_r',
 'binary_r',
 'bone_r',
 'brg_r',
 'bwr_r',
 'cool_r',
 'coolwarm_r',
 'copper_r',
 'cubehelix_r',
 'flag_r',
 'gist_earth_r',
 'gist_gray_r',
 'gist_heat_r',
 'gist_ncar_r',
 'gist_rainbow_r',
 'gist_stern_r',
 'gist_yarg_r',
 'gnuplot_r',
 'gnuplot2_r',
 'gray_r',
 'hot_r',
 'hsv_r',
 'jet_r',
 'nipy_spectral_r',
 'ocean_r',
 'pink_r',
 'prism_r',
 'rainbow_r',
 'seismic_r',
 'spring_r',
 'summer_r',
 'terrain_r',
 'winter_r',
 'Accent_r',
 'Dark2_r',
 'Paired_r',
 'Pastel1_r',
 'Pastel2_r',
 'Set1_r',
 'Set2_r',
 'Set3_r',
 'tab10_r',
 'tab20_r',
 'tab20b_r',
 'tab20c_r']

"""


def plot_water_values(time, X, Y, Z, name=""):
    fig, ax = plt.subplots()

    pmin = Z.min().min()
    pmax = Z.max().max()
    levels = np.linspace(pmin, pmax, 30)

    # TODO: Plot time

    # Creating plot
    cp = ax.contourf(
        Y,
        X,
        Z,
        cmap="ocean_r",
        levels=levels,
    )
    fig.colorbar(cp)
    ax.set_title(f"Water values: {name}")
    ax.set_xlabel("Week")
    ax.set_ylabel("Filling")
    fig.autofmt_xdate()
    plt.show()


def plot_price_series(time, data, name=""):
    """Plots price series as a function of time for all scenarios"""

    fig, ax = plt.subplots()

    time_np = np.array(time, dtype="datetime64[ms]")
    prices_np = np.array(data, copy=False)

    scenarios = prices_np.shape[0]
    ax.set_title('Price series "{}"'.format(name))

    for i in range(scenarios):
        ax.plot(
            time_np,
            prices_np[i, :],
        )

    ax.set_xlabel("Time (h)")
    ax.set_ylabel(f"Price ({data.unit})")

    plt.gcf().autofmt_xdate()
    plt.show()


def generic_plot(time, data, name="Generic plot"):
    time_np = np.array(time, dtype="datetime64[ms]")
    data_np = np.array(data, copy=False)

    fig, ax = plt.subplots()
    scenarios = data_np.shape[0]

    labels = []

    for i in range(scenarios):
        ax.plot(time_np, data_np[i, :])
        labels.append(f"Scenario {i}")

    ax.legend(labels)
    ax.set_title(f"{name} ({data.unit})")

    plt.gcf().autofmt_xdate()
    plt.show()


def make_generic_plot(ndarray: tuple, name):
    if ndarray is None:
        return

    time, values = ndarray

    if time is None or values is None:
        return

    generic_plot(time, values, name)


def continuous_generic_plot(time, data, name="Stacked Generic plot"):
    time_np = np.array(time, dtype="datetime64[ms]")
    data_np = np.array(data, copy=False)

    scenarios = data_np.shape[0]
    fig, ax = plt.subplots(figsize=(1.5 * scenarios, 4))

    labels = []

    # fiftytwo_weeks = np.timedelta64(52, "W")
    fiftytwo_weeks = time_np[-1] - time_np[0]

    for i in range(scenarios):
        x = time_np + fiftytwo_weeks * i
        ax.plot(x, data_np[i, :])
        labels.append(f"Scenario {i}")

    ax.legend(labels)
    ax.set_title(f"{name} ({data.unit})")

    plt.gcf().autofmt_xdate()
    plt.show()


def make_continuous_generic_plot(ndarray: tuple, name):
    if ndarray is None:
        return

    time, values = ndarray

    if time is None or values is None:
        return

    continuous_generic_plot(time, values, name)


def make_water_value_plot(wv_results: tuple, name: str):
    if wv_results is None:
        return

    time, values = wv_results

    if time is None or values is None:
        return

    time_np = np.array(time, dtype="datetime64[ms]")
    water_values = np.array(values, copy=False)

    # print(water_values.shape)
    if water_values.shape != ():
        wv_for_plotting = water_values[:, 0, 0, :]
        max_reservoir_level = 100
        filling = np.linspace(max_reservoir_level, 0, wv_for_plotting.shape[1])
        week = np.arange(wv_for_plotting.shape[0])

        X, Y = np.meshgrid(filling, week)
        plot_water_values(time_np, X, Y, wv_for_plotting, name=name)

    pass


def make_market_results_plot(market_results: tuple, name: str):
    if market_results is None:
        return

    time, prices = market_results

    if time is None or prices is None:
        return

    plot_price_series(time, prices, name)

    pass
