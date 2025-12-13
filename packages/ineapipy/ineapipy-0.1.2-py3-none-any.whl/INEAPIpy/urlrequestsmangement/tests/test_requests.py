#
# Set shebang if needed
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 17:21:46 2025

@author: mano
"""


from src import RequestsManagement as RM


A1 = RM.RequestsManager()
A2 = RM.RequestsManager(0.30, True)

print(A1 is A2)
