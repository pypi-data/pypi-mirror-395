#coding=utf8

################################################################################
###                                                                          ###
### Created by Martin Genet, 2012-2025                                       ###
###                                                                          ###
### University of California at San Francisco (UCSF), USA                    ###
### Swiss Federal Institute of Technology (ETH), Zurich, Switzerland         ###
### École Polytechnique, Palaiseau, France                                   ###
###                                                                          ###
################################################################################

import os
import sys

################################################################################

class Printer():

    def __init__(self,
            tab=" |  ",
            max_level=float("+Inf"),
            filename=None,
            silent=False):

        self.tab = tab
        self.cur_level = 0
        self.loc_level = 0
        self.max_level = max_level

        if (silent):
            self.must_close = False
            if (sys.version_info.major >= 3):
                self.output = open(os.devnull, "w", encoding='utf-8')
            else:
                self.output = open(os.devnull, "w")
        else:
            if (filename is None):
                self.must_close = False
                self.output = sys.stdout
            else:
                self.must_close = True
                if (sys.version_info.major >= 3):
                    self.output = open(filename, "w", encoding='utf-8')
                else:
                    self.output = open(filename, "w")

    def close(self):

        if (self.must_close):
            self.output.close()

    def inc(self):
        self.cur_level += 1

    def dec(self):
        self.cur_level -= 1

    def print_str(self,
            string,
            var_level=0,
            tab=True,
            newline=True,
            flush=True):

        self.loc_level = self.cur_level + var_level
        if (self.loc_level <= self.max_level):
            if (tab):
                self.output.write(self.loc_level*self.tab)
            self.output.write(string)
            if (newline):
                self.output.write("\n")
            if (flush):
                self.output.flush()

    def print_var(self,
            name,
            val,
            var_level=0,
            tab=True,
            newline=True,
            flush=True):

        self.print_str(
            string=name+" = "+str(val),
            var_level=var_level,
            tab=tab,
            newline=newline,
            flush=flush)

    def print_sci(self,
            name,
            val,
            var_level=0,
            tab=True,
            newline=True,
            flush=True):

        self.print_str(
            string=name.ljust(13) + " = " + format(val,".4e"),
            var_level=var_level,
            tab=tab,
            newline=newline,
            flush=flush)

################################################################################

class TablePrinter():

    def __init__(self,
            titles,
            width=None,
            filename=None,
            silent=False):

        if (silent):
            self.must_close = False
            self.output = open(os.devnull, "w")
        else:
            if (filename is None):
                self.must_close = False
                self.output = sys.stdout
            else:
                self.must_close = True
                if (sys.version_info.major >= 3):
                    self.output = open(filename, "w", encoding='utf-8')
                else:
                    self.output = open(filename, "w")

        self.titles = titles

        if (width is None):
            self.width = max([len(title) for title in self.titles])+2
        else:
            self.width = width

        self.output.write("-"+"-".join(["-"*self.width for title in self.titles])+"-\n")
        self.output.write("|"+"|".join([title.center(self.width) for title in self.titles])+"|\n")
        self.output.write("-"+"-".join(["-"*self.width for title in self.titles])+"-\n")
        self.output.flush()

    def close(self):

        self.output.write("-"+"-".join(["-"*self.width for title in self.titles])+"-\n")
        self.output.flush()

        if (self.must_close):
            self.output.close()

    def write_line(self,
            values):

        strings = []
        for value in values:
            if (len(str(value)) <= self.width):
                strings += [str(value)]
            else:
                strings += [format(value, ".2e")]
        self.output.write("|"+"|".join([string.center(self.width) for string in strings])+"|\n")
        self.output.flush()

################################################################################

class DataPrinter():

    def __init__(self,
            names,
            filename,
            limited_precision=False,
            width=None,
            sep=" ",
            comment="#"):

        self.names = names
        self.filename = filename
        if (limited_precision):
            min_width = 6
            self.write_line = self.write_line_limited_precision
        else:
            min_width = 23
            self.write_line = self.write_line_full_precision
        if (width is None):
            self.width = max(min_width, max([len(name) for name in self.names]))
        else:
            self.width = width
        self.sep = sep
        self.comment = comment

        if (sys.version_info.major >= 3):
            self.file = open(self.filename, "w", encoding='utf-8')
        else:
            self.file = open(self.filename, "w")
        self.file.write(self.comment+self.sep.join([name.center(self.width) for name in self.names])+"\n")
        self.file.flush()

    def close(self):

        self.file.close()

    def write_comment(self,
            comment : str):

        self.file.write(self.comment+comment+"\n")
        self.file.flush()

    def write_line_full_precision(self,
            values : list = []):

        self.file.write(" "+self.sep.join([str(value).center(self.width) for value in values])+"\n")
        self.file.flush()

    def write_line_limited_precision(self,
            values : list = []):

        self.file.write(" "+self.sep.join([str(value).center(self.width) if (type(value) is int) else format(value, "+1.3f").center(self.width) for value in values])+"\n")
        self.file.flush()
