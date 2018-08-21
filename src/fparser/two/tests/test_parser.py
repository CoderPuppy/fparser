# Copyright (c) 2018 Science and Technology Facilities Council
# All rights reserved.
#
# Modifications made as part of the fparser project are distributed
# under the following license:
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

''' Module containing tests for the parser file '''

import pytest
from fparser.two.parser import ParserFactory
from fparser.common.readfortran import FortranStringReader
from fparser.two.utils import NoMatchError


def test_parserfactory_std():
    '''Test ParserFactory std argument options [none, f2003, f2008 and
    invalid]. Also test that previous calls to the create method in
    the ParserFactory class do not affect current calls.

    '''
    fstring = (
        "submodule (x) y\n"
        "end\n")
    parser = ParserFactory().create()
    reader = FortranStringReader(fstring)
    with pytest.raises(NoMatchError) as excinfo:
        _ = parser(reader)
    assert "at line 1\n>>>submodule (x) y\n" in str(excinfo.value)

    parser = ParserFactory().create(std="f2003")
    reader = FortranStringReader(fstring)
    with pytest.raises(NoMatchError) as excinfo:
        _ = parser(reader)
    assert "at line 1\n>>>submodule (x) y\n" in str(excinfo.value)

    parser = ParserFactory().create(std="f2008")
    reader = FortranStringReader(fstring)
    ast = parser(reader)
    code = str(ast)
    assert "SUBMODULE (x) y\nEND SUBMODULE y" in code

    # Repeat f2003 example to make sure that a previously valid (f2008)
    # match does not affect the current (f2003) invalid match.
    parser = ParserFactory().create(std="f2003")
    reader = FortranStringReader(fstring)
    with pytest.raises(NoMatchError) as excinfo:
        _ = parser(reader)
    assert "at line 1\n>>>submodule (x) y\n" in str(excinfo.value)

    # TODO: raise exception here, see issue #52
    with pytest.raises(SystemExit):
        parser = ParserFactory().create(std="invalid")
