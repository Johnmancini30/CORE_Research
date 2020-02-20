import matplotlib.pyplot as plt
import re

"""
analysis.py: runs analysis on the data that was parsed
"""
class Analysis:

    """
    :param string file_name: file that will be parsed for doing analysis
    """
    def __init__(self, file_name):
        self.fn = file_name
        self.data = self.extract_data()


    """
    To analyze the mean of the data. In the context of received data it makes sense to calculate the average bytes 
    that arrived per second

    :param string: data_type this is to specify which string to use in data dictionary
    :return: None
    """
    def calculate_average(self, data_type):
        cache = {}

        curr_key = 1
        cache[curr_key] = 0
        data = self.data[data_type]
        curr = int(data[0])

        for time in data:
            if curr == int(time):
                cache[curr_key] += 1
            else:
                curr = int(time)
                curr_key += 1
                cache[curr_key] = 1

        num_seconds = len(cache.keys())-2
        tot = 0
        for key in list(cache.keys())[1:-1]:
            tot += cache[key]*125*8

        print("Calculating average on the <" + data_type + "> parameter.\n")
        print("Average bits generated per second:")
        print(tot/num_seconds)
        print("")
        print("Actual packets generated per second, 125 bytes per packet:")
        print(cache)


    """
    For looking at data with matplotlib
    
    :param dict: data Conains parameters
    :return: None
    """
    def display_data(self, data):
        x = None
        y = None
        x_label = None
        y_label = None

        try:
            x = data["x"]
            y = data["y"]
        except:
            print("Missing x or y data")

        if "x_label" in data:
            x_label = data["x_label"]
        if "y_label" in data:
            y_label = data["y_label"]

        plt.scatter(x, y)
        if x_label:
            plt.xlabel(x_label)
        if y_label:
            plt.ylabel(y_label)

        plt.show()


    """
    Parses file for data, stores each parameter as key with corresponding list of values
    
    :param None:
    :return: dict of lists
    """
    def extract_data(self):
        to_ret = {}

        with open(self.fn, "r") as f:

            lines = f.read().split("\n")
            curr = lines[0]
            i = 1
            while (i < len(lines)):
                if all([c == " " for c in lines[i]]):
                    i+=1
                    continue
                elif bool(re.search(r'\d', lines[i])):
                    if curr not in to_ret:
                        to_ret[curr] = []

                    to_ret[curr].append(self.convert_timestamp(lines[i]))
                else:
                    curr = lines[i]

                i += 1

        return to_ret


    """
    Converts a timestamp to seconds
    
    :param float: time
    :return float:
    """
    @staticmethod
    def convert_timestamp(time):
        to_add = 0.0
        fact = 60*60
        tmp = time.split(":")

        for num in tmp[:-1]:
            to_add += int(num)*fact
            fact/=60

        tmp = tmp[-1].split(".")
        to_add += float(tmp[0]) + float("." + tmp[-1])

        return to_add


if __name__=='__main__':
    a = Analysis("30Second_10kbps_Poisson.txt")

    #a.calculate_average("sent")
    #a.calculate_average("recv")
    #data = {"x" : a.data["sent"], "y" : a.data["recv"], "x_label" : "Sent", "y_label" : "Recevied"}
    #a.display_data(data)