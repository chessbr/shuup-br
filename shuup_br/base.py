# -*- coding: utf-8 -*-
# This file is part of Shuup BR.
#
# Copyright (c) 2016, Rockho Team. All rights reserved.
# Author: Christian Hess
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.


class CPF(object):
    @classmethod
    def validate(cls, cpf):
        """
        Valida o CPF recebido
            @param cpf: string - CPF a ser validado
            @return: bool - se o CPF é válido ou não
        """

        if not cpf:
            return False

        # obtém os digitos do CPF (apenas os numeros)
        cpf_digits = "".join([d for d in str(cpf) if d.isdigit()])

        # deve haver 11 digitos
        if len(cpf_digits) != 11:
            return False

        invalid_cpfs = [11 * str(i) for i in range(10)]

        # não pode ser um número com todos os
        # digitos iguais, ex: 11111111111, 222222222, 33333333, etc
        if cpf_digits in invalid_cpfs:
            return False

        # transforma a string em uma lista de inteiros
        cpf_number = [int(x) for x in cpf_digits]

        weights_dv1 = range(10, 1, -1)
        dv1 = 0

        # calcula o primeiro digito verificador utilizando os 9 numeros
        for ix in range(9):
            dv1 = dv1 + (weights_dv1[ix] * cpf_number[ix])

        dv1 = 11 - (dv1 % 11)
        if dv1 > 9:
            dv1 = 0

        weights_dv2 = range(11, 1, -1)
        # calcula o segundo dv utilizando 10 numeros
        dv2 = 0
        for ix in range(10):
            dv2 = dv2 + (weights_dv2[ix] * cpf_number[ix])
        dv2 = 11 - (dv2 % 11)
        if dv2 > 9:
            dv2 = 0

        if [dv1, dv2] != cpf_number[-2:]:
            return False

        return True


class CNPJ(object):
    @classmethod
    def _get_dv1(cls, cnpj_digits):
        """
        Obtém o primeiro dígito verificador do CNPJ informado
            @param cnpj_digits: lista de inteiros contendo os 12 números do CNPJ (sem os dv)
            @return: int - primeiro DV
        """
        weights_dv1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

        # calcula o DV1
        dv1_sum = 0
        dv1 = 0

        for ix in range(12):
            dv1_sum = dv1_sum + (weights_dv1[ix] * cnpj_digits[ix])

        rdv1 = dv1_sum % 11

        if rdv1 < 2:
            dv1 = 0
        else:
            dv1 = 11 - rdv1

        return dv1

    @classmethod
    def _get_dv2(cls, cnpj_digits):
        """
        Obtém o segundo dígito verificador do CNPJ informado
            @param cnpj_digits: lista de inteiros contendo os 13 números do CNPJ (sem o ultimo dv)
            @return: int - segundo DV
        """
        weights_dv2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

        # calcula o DV2
        dv2_sum = 0
        dv2 = 0

        for ix in range(13):
            dv2_sum = dv2_sum + (weights_dv2[ix] * cnpj_digits[ix])

        rdv2 = dv2_sum % 11

        if rdv2 < 2:
            dv2 = 0
        else:
            dv2 = 11 - rdv2

        return dv2

    @classmethod
    def validate(cls, cnpj):
        """
        Valida o CNPJ recebido
            @param cnpj: string - CNPJ a ser validado
            @return: bool - se o CNPJ é válido ou não
        """

        if not cnpj:
            return False

        # obtém os digitos do CNPJ (apenas os numeros)
        cnpj_digits = "".join([d for d in str(cnpj) if d.isdigit()])

        # deve haver 14 digitos
        if len(cnpj_digits) != 14:
            return False

        invalid_cnpjs = [14 * str(i) for i in range(10)]

        # não pode ser um número com todos os
        # digitos iguais, ex: 11111111111, 222222222, 33333333, etc
        if cnpj_digits in invalid_cnpjs:
            return False

        # transforma a string em uma lista de inteiros
        cnpj_number = [int(x) for x in cnpj_digits]

        dv1 = CNPJ._get_dv1(cnpj_number)
        dv2 = CNPJ._get_dv2(cnpj_number)

        if [dv1, dv2] != cnpj_number[-2:]:
            return False

        return True
