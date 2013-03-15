'''
Created on 04/23/2012

@author: zubietaroberto
'''

from cx_Freeze import setup, Executable

exe = Executable("main.py")


setup(
        name = "Hashtag Counter",
        version = "0.1",
        description = "Cuenta tweets",
		author = "Roberto E. Zubieta P.",
        executables = [exe]
        )