import io
import random

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import BetaController


def draw_beta_chart_with_baseline(beta_list, base_line, security_name):
    """
    The main driver for working with matplot lib
    :param beta_list:
    :param base_line:
    :param security_name:
    :return:
    """
    print("Debug: Going to create a chart with the following values", "beta list: ", beta_list, "base_line: ",
          base_line, "Security Name:", security_name, sep='\n')
    fig = plt.figure()

    # The below sets the lists to the same size
    if len(beta_list) > len(base_line):
        for x in range(len(beta_list) - 1):
            base_line.append(base_line[0])

    # Sets the x values
    x_axis_values = range(len(beta_list))
    plt.plot(x_axis_values, base_line, label="Total Period Beta")

    ###############################################
    # Add a plot to plt. simply add the list of chunked betas
    plt.plot(x_axis_values, beta_list, label="Sub-Period Beta")
    ###############################################

    plt.title(security_name + " Beta over time period")
    ###########################################
    # uncomment below and correctly set matplot lib x and y labels
    plt.xlabel("xlabel")
    plt.ylabel("ylabel")

    plt.legend()

    # comment out next line when running from web
    # plt.show()  <--- needed to turn this off
    # end
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return output


'''
Stub to create a random graph. 
You should use draw_beta_chart_with_baseline
'''


def create_figure(name):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    axis.set_title("Your name: " + name)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return output


"""
I like to have simple test functions in each module while developing
"""
if __name__ == '__main__':
    base_betas, chunked_betas = BetaController.do_calculations("AAPL", 10)
    draw_beta_chart_with_baseline(chunked_betas, base_betas, 'AAPL')
