""" Versatile collection of routines & tools for common development tasks """

__author__ = 'Dr. Marcus Zeller (dsp4444@gmail.com)'
__version__ = '0.1.5'
__all__ = [ "core", "plot" ]


def demo():
    import numpy as np
    from zdev.plot import qplot, plt

    print("Welcome to the zdev package!")

    tmp = input("Please enter some numbers (separated by ','): ") 
    x = np.array(str(tmp).split(','), dtype=np.float64)

    qplot(x, info='what-u-just-entered', bold=True)
    plt.show()

    print("See how quickly things can be plotted? (> 'qplot()')")
    print("Therefore... have phun! ;)")

    return

