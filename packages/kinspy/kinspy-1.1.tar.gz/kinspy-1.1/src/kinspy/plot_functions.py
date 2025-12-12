from importlib import import_module

def generate_image_setting():
    plt = import_module("matplotlib.pyplot")
    plt.rcParams["font.family"] = "Helvetica"
    plt.rcParams["figure.dpi"] = 300
    plt.rcParams["figure.figsize"] = [6.4,4.8]
    plt.rcParams["font.size"] = 12
