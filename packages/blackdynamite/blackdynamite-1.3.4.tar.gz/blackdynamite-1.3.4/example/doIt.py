#!/bin/env python3
# This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import numpy as np

import BlackDynamite as BD

myrun, myjob = BD.getRunFromScript()

print(myjob)

myrun.start()

for step in range(0, 10):
    _quantity = myrun.id * step
    myrun.pushQuantity(_quantity, step, "ekin")
    myrun.pushQuantity(_quantity * 2, step, "epot")
    myrun.pushQuantity(np.random.random(10), step, "random_vect")

myrun.finish()
