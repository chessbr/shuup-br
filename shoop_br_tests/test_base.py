# -*- coding: utf-8 -*-
# This file is part of Shoop BR.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from shoop_br.base import CPF, CNPJ

def test_cpf():
    assert CPF.validate('0123456789') == False
    assert CPF.validate('012345678901') == False

    assert CPF.validate('00000000000') == False
    assert CPF.validate('11111111111') == False
    assert CPF.validate('22222222222') == False
    assert CPF.validate('33333333333') == False
    assert CPF.validate('44444444444') == False
    assert CPF.validate('55555555555') == False
    assert CPF.validate('66666666666') == False
    assert CPF.validate('77777777777') == False
    assert CPF.validate('88888888888') == False
    assert CPF.validate('99999999999') == False

    assert CPF.validate('01234567890') == True
    assert CPF.validate('12541245351') == True
    assert CPF.validate('65928332700') == True
    assert CPF.validate('15868685270') == True
    assert CPF.validate('47322445805') == True
    assert CPF.validate('75788318602') == True
    assert CPF.validate('11578781647') == True
    assert CPF.validate('58686793770') == True
    assert CPF.validate('66348751112') == True
    assert CPF.validate('24753561208') == True
    assert CPF.validate('40088614832') == True
    assert CPF.validate('14477542208') == True
    assert CPF.validate('40817847600') == True

def test_cnpj():
    assert CNPJ.validate('0123456789') == False
    assert CNPJ.validate('012345678901') == False

    assert CNPJ.validate('00000000000') == False
    assert CNPJ.validate('11111111111') == False
    assert CNPJ.validate('22222222222') == False
    assert CNPJ.validate('33333333333') == False
    assert CNPJ.validate('44444444444') == False
    assert CNPJ.validate('55555555555') == False
    assert CNPJ.validate('66666666666') == False
    assert CNPJ.validate('77777777777') == False
    assert CNPJ.validate('88888888888') == False
    assert CNPJ.validate('99999999999') == False

    assert CNPJ.validate('00000000000000') == False
    assert CNPJ.validate('11111111111111') == False
    assert CNPJ.validate('22222222222222') == False
    assert CNPJ.validate('33333333333333') == False
    assert CNPJ.validate('44444444444444') == False
    assert CNPJ.validate('55555555555555') == False
    assert CNPJ.validate('66666666666666') == False
    assert CNPJ.validate('77777777777777') == False
    assert CNPJ.validate('88888888888888') == False
    assert CNPJ.validate('99999999999999') == False

    assert CNPJ.validate('33659232000105') == True
    assert CNPJ.validate('68171878000123') == True
    assert CNPJ.validate('86894898000104') == True
    assert CNPJ.validate('85571364000184') == True
    assert CNPJ.validate('29283665000131') == True
    assert CNPJ.validate('36869856000145') == True
    assert CNPJ.validate('97214039000143') == True
    assert CNPJ.validate('59550422000183') == True
    assert CNPJ.validate('84554458000182') == True
    assert CNPJ.validate('01234567000195') == True
    assert CNPJ.validate('01234567000276') == True
    assert CNPJ.validate('01234567000357') == True
    assert CNPJ.validate('01234567000438') == True
    assert CNPJ.validate('01234567005073') == True
    assert CNPJ.validate('01234567068407') == True
    assert CNPJ.validate('01234567954199') == True

