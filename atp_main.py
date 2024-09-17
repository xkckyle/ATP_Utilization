import atp_etl,atp_plot_util
import os

if __name__ == '__main__':
    #
    #
    fnd,mind,maxd = atp_etl.grab_dr()
    atp_plot_util.plot_util(fnd,mind,maxd)