#!/usr/bin/env python3
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
################################################################

import BlackDynamite as BD

################################################################


def validate(question, params):
    validated = BD.bdparser.validate_question(question, params)

    return validated


################################################################


def main(argv=None):
    parser = BD.BDParser(description="reset")

    params = parser.parseBDParameters(argv)
    # print(params)
    validated = validate("Reset completely the study (irreversible)", params)
    if validated:
        import subprocess

        subprocess.run("rm -rf BD-*-runs .bd", shell=True)


if __name__ == "__main__":
    main()
