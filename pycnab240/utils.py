# -*- encoding: utf8 -*-

import re
from datetime import date, timedelta
from decimal import Decimal
from pycnab240 import bancos

BANK = {
    '756': bancos.sicoob,
    '033': bancos.santander,
    '341': bancos.itau,
    '237': bancos.bradesco
}


OPERATION_NAME = {
    'OTHER': {
        '01': 'TED_OTHER_BANK',
        '02': 'DOC_OTHER_BANK',
        '03': 'TITULOS',
        '04': 'BARCODE',
        '05': 'GPS',
        '06': 'DARF_NORMAL',
        '07': 'DARF_SIMPLES',
        '08': 'FGTS',
        '09': 'ICMS'
        },
    'SAME_BANK': {
        '01': 'CC_OTHER_TITUL',
        '02': 'CC_OTHER_TITUL',
        '03': 'TITULOS_SAME_BANK'
    },
    'SAME_TIT': {
        '01': 'TED_SAME_TITUL',
        '02': 'DOC_SAME_TITUL'
    },
    'SAME_BOTH': {
        '01': 'CC_SAME_TITUL',
        '02': 'CC_SAME_TITUL'
    }
}

FORMA_DE_LANCAMENTO = {
    # Usar os códigos do Santander como base
    '033': {
        'TED_OTHER_BANK': '03',  # Transferências para outros bancos (DOC, TED)
        'DOC_OTHER_BANK': '03',  # Transferências para outros bancos (DOC, TED)
        'TITULOS': '31',  # Pagamento de Títulos
        'TITULOS_SAME_BANK': '30',
        'BARCODE': '11',  # Tributos com código de barras
        'GPS': '17',  # GPS - Guia de previdencia Social
        'DARF_NORMAL': '16',  # DARF Normal
        'DARF_SIMPLES': '18',  # DARF Simples
        'FGTS': '11',  # FGTS
        # 'ICMS': '',  # ICMS
        'DOC_SAME_TITUL': '03',  # 'Transferência (DOC "C" - mesmo titular)'
        'TED_SAME_TITUL': '03',  # 'Transferência (TED - mesmo titular)'
        'CC_OTHER_TITUL': '01',  # 'Credito em CC)'
        'CC_SAME_TITUL': '01'
    },
    '756': {
        'TED_OTHER_BANK': '41',  # Transferências para outros bancos (TED)
        'DOC_OTHER_BANK': '03',  # Transferências para outros bancos (DOC)
        'DOC_SAME_TITUL': '03',  # 'Transferência (DOC "C" - mesmo titular)'
        'TED_SAME_TITUL': '43',  # 'Transferência (TED - mesmo titular)'
        'TITULOS': '31',  # Pagamento de Títulos
        'TITULOS_SAME_BANK': '30',  # Pagamento de Títulos - Sicoob
        'BARCODE': '11',  # Tributos com código de barras
        'GPS': '17',  # GPS - Guia de previdencia Social
        'DARF_NORMAL': '16',  # DARF Normal
        'DARF_SIMPLES': '18',  # DARF Simples
        'FGTS': '11',  # FGTS
        'CC_OTHER_TITUL': '01',  # 'Credito em CC)'
        'CC_SAME_TITUL': '01'
        #  'ICMS': , #
    },
    '341': {
        'TED_OTHER_BANK': '41',  # 'Transferência (TED - outro titular)'
        'DOC_OTHER_BANK': '03',  # 'Transferência (DOC "D" - outro titular)'
        'TITULOS': '31',  # 'Pagamento de Títulos - Outros bancos'
        'BARCODE': '91',  # Tributos com código de barras e GNRE
        'GPS': '17',  # GPS - Guia de previdencia Social
        'DARF_NORMAL': '16',  # DARF Normal
        'DARF_SIMPLES': '18',  # DARF Simples
        'FGTS': '35',  # FGTS
        'ICMS': '22',  # ICMS
        'TITULOS_SAME_BANK': '30',  # 'Pagamento de Títulos - Itaú'
        'CC_SAME_TITUL': '06',  # 'Credito em CC do Itaú - mesmo titular
        'DOC_SAME_TITUL': '07',  # 'Transferência (DOC "C" - mesmo titular)'
        'TED_SAME_TITUL': '43',  # 'Transferência (TED - mesmo titular)'
        'CC_OTHER_TITUL': '01',  # 'Credito em CC do itau')'
    },
    '237': {
        'TED_OTHER_BANK': '41',  # Transferências para outros bancos (TED)
        'DOC_OTHER_BANK': '03',  # Transferências para outros bancos (DOC)
        'DOC_SAME_TITUL': '03',  # 'Transferência (DOC "C" - mesmo titular)'
        'TED_SAME_TITUL': '43',  # 'Transferência (TED - mesmo titular)'
        'TITULOS': '31',  # Pagamento de Títulos
        'TITULOS_SAME_BANK': '30',  # Pagamento de Títulos - Sicoob
        'BARCODE': '11',  # Tributos com código de barras
        'GPS': '17',  # GPS - Guia de previdencia Social
        'DARF_NORMAL': '16',  # DARF Normal
        'DARF_SIMPLES': '18',  # DARF Simples
        #  'FGTS': '11',  # FGTS
        'CC_OTHER_TITUL': '01',  # 'Credito em CC)'
        'CC_SAME_TITUL': '01',  # 'Credito em CC - mesma titularidade)'
        'ICMS': '22',  # GARE-SP
    }
}

TIPO_DE_SERVICO = {
    'santander': {
        '03': '03',  # Bloqueto Eletronico
        '10': '10',  # Pagamento Dividendos
        '14': '14',  # Consulta de Tributos a Pagar DETRAN com RENAVAM
        '20': '20',  # Pagamento Fornecedor
        '22': '22',  # Pagamento de Contas, Tributos e Impostos
        '29': '29',  # Alegacao do Sacado
        '50': '50',  # Pagamento Sinistros Segurados
        '60': '60',  # Pagamento Despesas Viajante em Transito
        '70': '70',  # Pagamento Autorizado
        '75': '75',  # Pagamento Credenciados
        '80': '80',  # Pagamento Representantes / Vendedores Autorizados
        '90': '90',  # Pagamento Beneficios
        '98': '98',  # Pagamentos Diversos
    },
    'itau': {
        '10': '10',  # Pagamento Dividendos
        '14': '14',  # Consulta de Tributos a Pagar DETRAN com RENAVAM
        '20': '20',  # Pagamento Fornecedor
        '22': '22',  # Pagamento de Contas, Tributos e Impostos
        '29': '29',  # Alegacao do Sacado
        '50': '50',  # Pagamento Sinistros Segurados
        '60': '60',  # Pagamento Despesas Viajante em Transito
        '80': '80',  # Pagamento Representantes / Vendedores Autorizados
        '90': '90',  # Pagamento Beneficios
        '98': '98',  # Pagamentos Diversos
    },
    'bradesco': {
        '10': '10',  # Pagamento Dividendos
        '14': '14',  # Consulta de Tributos a Pagar DETRAN com RENAVAM
        '20': '20',  # Pagamento Fornecedor
        '22': '22',  # Pagamento de Contas, Tributos e Impostos
        '29': '29',  # Alegacao do Sacado
        '50': '50',  # Pagamento Sinistros Segurados
        '60': '60',  # Pagamento Despesas Viajante em Transito
        '80': '80',  # Pagamento Representantes / Vendedores Autorizados
        '90': '90',  # Pagamento Beneficios
        '98': '98',  # Pagamentos Diversos
        }
}


DOC_TED_FINALITY = {
    'itau': {
        '02': {  # DOC
            '01': '01',  # Crédito em Conta Corrente
            '02': '02',  # Pagamento de Aluguel / Condomínio
            '03': '03',  # Pagamento de Duplicatas e Títulos
            '04': '04',  # Pagamento de Dividendos
            '05': '05',  # Pagamento de Mensalidades Escolares
            '06': '06',  # Pagamento de Salários
            '07': '07',  # Pagamento a Fornecedor / Honorários
            '08': '08',  # Pagamento de Câmbio/Fundos/Bolsas
            '09': '09',  # Repasse de Arrecadação / Pagamento de Tributos
            '11': '11',  # DOC para Poupança'
            '12': '12',  # DOC para Depósito Judicial
            '13': '13',  # Pensão Alimentícia
            '99': '99',  # Outros
        },
        '01': {  # TED
            '01': '010',  # Crédito em Conta Corrente
            '02': '007',  # Pagamento de Aluguel / Condomínio
            '03': '008',  # Pagamento de Duplicatas e Títulos
            '04': '003',  # Pagamento de Dividendos
            '06': '004',  # Pagamento de Salários
            '07': '005',  # Pagamento a Fornecedor / Honorários
            '08': '204',  # Pagamento de Câmbio/Fundos/Bolsas
            '09': '001',  # Repasse de Arrecadação / Pagamento de Tributos
            '12': '100',  # DOC para Depósito Judicial
            '13': '101',  # Pensão Alimentícia
        }
    },
    'sicoob': {
        '02': {  # DOC
            '01': '01',  # credito em conta
            '02': '02',  # pagto de aluguel/cond
            '03': '03',  # pagto de duplicata/titulos
            '04': '04',  # pagto de dividendos
            '05': '05',  # pagto mensalidade escolar
            '06': '06',  # pagto salarios
            '07': '07',  # pagto fornecedores
            '08': '08',  # op cambio/fundos/bolsa
            '09': '09',  # arrecadação/pagto de tributos
            '11': '11',  # DOC para poupança
            '12': '12',  # DOC para Depósito Judicial
            '13': '13',  # Pensão Alimentícia
            '14': '14',  # Restituição de Imposto de Renda
            '99': '13',  # Outros
        },
        '01': {  # TED
            '01': '10',  # credito em conta
            '02': '7',  # pagto de aluguel/cond
            '03': '8',  # pagto de duplicata/titulos
            '04': '3',  # pagto de dividendos
            '05': '9',  # pagto mensalidade escolar
            '06': '4',  # pagto salarios
            '07': '5',  # pagto fornecedores
            '08': '204',  # op cambio/fundos/bolsa
            '09': '1',  # arrecadação/pagto de tributos
            '11': '10',  # DOC para poupança
            '12': '10',  # DOC para Depósito Judicial
            '13': '101',  # Pensão Alimentícia
            '14': '300',  # Restituição de Imposto de Renda
            '99': '10',  # Outros
        }
    },
    'bradesco': {
        '02': {  # DOC
            '01': '01',  # credito em conta
            '02': '02',  # pagto de aluguel/cond
            '03': '03',  # pagto de duplicata/titulos
            '04': '04',  # pagto de dividendos
            '05': '05',  # pagto mensalidade escolar
            '06': '06',  # pagto salarios
            '07': '07',  # pagto fornecedores
            '08': '08',  # op cambio/fundos/bolsa
            '09': '09',  # arrecadação/pagto de tributos
            '11': '11',  # DOC para poupança
            '12': '12',  # DOC para Depósito Judicial
            '13': '13',  # Pensão Alimentícia
            '14': '13',  # Restituição de Imposto de Renda
            '99': '13',  # Outros
        },
        '01': {  # TED
            '01': '01',  # credito em conta
            '02': '02',  # pagto de aluguel/cond
            '03': '03',  # pagto de duplicata/titulos
            '04': '04',  # pagto de dividendos
            '05': '05',  # pagto mensalidade escolar
            '06': '06',  # pagto salarios
            '07': '07',  # pagto fornecedores
            '08': '08',  # op cambio/fundos/bolsa
            '09': '09',  # arrecadação/pagto de tributos
            '11': '11',  # DOC para poupança
            '12': '12',  # DOC para Depósito Judicial
            '13': '13',  # Pensão Alimentícia
            '14': '13',  # Restituição de Imposto de Renda
            '99': '13',  # Outros
        }
    }
}


SUBSEGMENTS = {
    '033': {
        'SegmentoN': {
            '16': 'SegmentoN_DarfNormal',
            '17': 'SegmentoN_GPS',
            '18': 'SegmentoN_DarfSimples',
            '22': 'SegmentoN_GareSP',
            '23': 'SegmentoN_GareSP',
            '24': 'SegmentoN_GareSP',
        }
    },
    '756': {
        'SegmentoN': {
            '16': 'SegmentoN_DarfNormal',
            '17': 'SegmentoN_GPS',
            '18': 'SegmentoN_DarfSimples',
        }
    },
    '341': {
        'SegmentoA': {
            '341': 'SegmentoA_Itau_Unibanco',
            '409': 'SegmentoA_Itau_Unibanco',
        },
        'SegmentoN': {
            '01': 'SegmentoN_GPS',
            '02': 'SegmentoN_DarfNormal',
            '03': 'SegmentoN_DarfSimples',
            '04': 'SegmentoN_DARJ',
            '05': 'SegmentoN_GareSP',
            '07': 'SegmentoN_IPVA_DPVAT',
            '08': 'SegmentoN_IPVA_DPVAT',
            '11': 'SegmentoN_FGTS',
        }
    },
    '237': {
        'SegmentoN': {
            '16': 'SegmentoN_DarfNormal',
            '17': 'SegmentoN_GPS',
            '18': 'SegmentoN_DarfSimples',
            '22': 'SegmentoN_GareSP',
        }
    },
}


CODIGOS_RETORNO = {
    '033': {
        '00': 'Crédito ou Débito Efetivado',
        '01': 'Insuficiência de Fundos - Débito Não Efetuado',
        '02': 'Crédito ou Débito Cancelado pelo Pagador/Credor',
        '03': 'Débito Autorizado pela Agência - Efetuado',
        'AA': 'Controle Inválido',
        'AB': 'Tipo de Operação Inválido',
        'AC': 'Tipo de Serviço Inválido',
        'AD': 'Forma de Lançamento Inválida',
        'AE': 'Tipo/Número de Inscrição Inválido',
        'AF': 'Código de Convênio Inválido',
        'AG': 'Agência/Conta Corrente/DV Inválido',
        'AH': 'Número Seqüencial do Registro no Lote Inválido',
        'AI': 'Código de Segmento de Detalhe Inválido',
        'AJ': 'Tipo de Movimento Inválido',
        'AK': 'Código da Câmara de Compensação do Banco do Favorecido/Depositário Inválido',  # noqa
        'AL': 'Código do Banco do Favorecido ou Depositário Inválido',
        'AM': 'Agência Mantenedora da Conta Corrente do Favorecido Inválida',
        'AN': 'Conta Corrente/DV do Favorecido Inválido',
        'AO': 'Nome do Favorecido não Informado',
        'AP': 'Data Lançamento Inválida/Vencimento Inválido',
        'AQ': 'Tipo/Quantidade da Moeda Inválido',
        'AR': 'Valor do Lançamento Inválido',
        'AS': 'Aviso ao Favorecido - Identificação Inválida',
        'AT': 'Tipo/Número de Inscrição do Favorecido/Contribuinte Inválido',
        'AU': 'Logradouro do Favorecido não Informado',
        'AV': 'Número do Local do Favorecido não Informado',
        'AW': 'Cidade do Favorecido não Informada',
        'AX': 'CEP/Complemento do Favorecido Inválido',
        'AY': 'Sigla do Estado do Favorecido Inválido',
        'AZ': 'Código/Nome do Banco Depositário Inválido',
        'BA': 'Código/Nome da Agência Depositário não Informado',
        'BB': 'Número do Documento Inválido(Seu Número)',
        'BC': 'Nosso Número Invalido',
        'BD': 'Inclusão Efetuada com Sucesso',
        'BE': 'Alteração Efetuada com Sucesso',
        'BF': 'Exclusão Efetuada com Sucesso',
        'BG': 'Agência/Conta Impedida Legalmente',
        'B1': 'Bloqueado Pendente de Autorização',
        'B3': 'Bloqueado pelo cliente',
        'B4': 'Bloqueado pela captura de titulo da cobrança',
        'B8': 'Bloqueado pela Validação de Tributos',
        'CA': 'Código de barras - Código do Banco Inválido',
        'CB': 'Código de barras - Código da Moeda Inválido',
        'CC': 'Código de barras - Dígito Verificador Geral Inválido',
        'CD': 'Código de barras - Valor do Título Inválido',
        'CE': 'Código de barras - Campo Livre Inválido',
        'CF': 'Valor do Documento/Principal/menor que o minimo Inválido',
        'CH': 'Valor do Desconto Inválido',
        'CI': 'Valor de Mora Inválido',
        'CJ': 'Valor da Multa Inválido',
        'CK': 'Valor do IR Inválido',
        'CL': 'Valor do ISS Inválido',
        'CM': 'Valor do IOF Inválido',
        'CN': 'Valor de Outras Deduções Inválido',
        'CO': 'Valor de Outros Acréscimos Inválido',
        'HA': 'Lote Não Aceito',
        'HB': 'Inscrição da Empresa Inválida para o Contrato',
        'HC': 'Convênio com a Empresa Inexistente/Inválido para o Contrato',
        'HD': 'Agência/Conta Corrente da Empresa Inexistente/Inválida para o Contrato',  # noqa
        'HE': 'Tipo de Serviço Inválido para o Contrato',
        'HF': 'Conta Corrente da Empresa com Saldo Insuficiente',
        'HG': 'Lote de Serviço fora de Seqüência',
        'HH': 'Lote de Serviço Inválido',
        'HI': 'Arquivo não aceito',
        'HJ': 'Tipo de Registro Inválido',
        'HL': 'Versão de Layout Inválida',
        'HU': 'Hora de Envio Inválida',
        'IJ': 'Competência ou Período de Referencia ou Numero da Parcela inválido',  # noqa
        'IL': 'Código de pagamento/Empresa/Receita inválido',
        'IM': 'Município Invalido',
        'IN': 'Numero Declaração Invalido',
        'IO': 'Numero Etiqueta invalido',
        'IP': 'Numero Notificação invalido',
        'IQ': 'Inscrição Estadual invalida',
        'IR': 'Divida Ativa Invalida',
        'IS': 'Valor Honorários ou Outros Acréscimos invalido',
        'IT': 'Período Apuração invalido',
        'IU': 'Valor ou Percentual da Receita invalido',
        'IV': 'Numero Referencia invalido',
        'TA': 'Lote não Aceito - Totais do Lote com Diferença',
        'XB': 'Número de Inscrição do Contribuinte Inválido',
        'XC': 'Código do Pagamento ou Competência ou Número de Inscrição Inválido',  # noqa
        'XF': 'Código do Pagamento ou Competência não Numérico ou igual á zeros',  # noqa
        'YA': 'Título não Encontrado',
        'YB': 'Identificação Registro Opcional Inválido',
        'YC': 'Código Padrão Inválido',
        'YD': 'Código de Ocorrência Inválido',
        'YE': 'Complemento de Ocorrência Inválido',
        'YF': 'Alegação já Informada',
        'ZA': 'Transferencia Devolvida',
        'ZB': 'Transferencia mesma titularidade não permitida',
        'ZC': 'Código pagamento Tributo inválido',
        'ZD': 'Competência Inválida',
        'ZE': 'Valor outras entidades inválido',
        'ZF': 'Sistema Origem Inválido',
        'ZG': 'Banco Destino não recebe DOC',
        'ZH': 'Banco Destino inoperante para DOC',
        'ZI': 'Código do Histórico de Credito Invalido',
        'ZK': 'Autorização iniciada no Internet Banking',
        'Z0': 'Conta com bloqueio*',
        'Z1': 'Conta fechada. É necessário ativar a conta*',
        'Z2': 'Conta com movimento controlado*',
        'Z3': 'Conta cancelada*',
        'Z4': 'Registro inconsistente (Título)*',
        'Z5': 'Apresentação indevida (Título)*',
        'Z6': 'Dados do destinatário inválidos*',
        'Z7': 'Agência ou conta destinatária do crédito inválida*',
        'Z8': 'Divergência na titularidade*',
        'Z9': 'Conta destinatária do crédito encerrada*',
        'C1': 'COMPROR – Devolvido por outros bancos**',
        'C2': 'COMPROR – Recusado**',
        'C3': 'COMPROR – Rejeitado por sistema**',
        'C4': 'COMPROR – Rejeitado por horário**',
        'C6': 'COMPROR – Aprovado**',
        'C7': 'COMPROR – Compromisso Inválido**',
    },
    '237': {
        '00': 'Crédito ou Débito Efetuado',
        '01': 'Insuficiência de fundos',
        '02': 'Crédito ou Débito Cancelado pelo Pagador/Credor',
        '03': 'Débito Autorizado pela Agência - Efetuado',
        'AA': 'Controle Inválido',
        'AB': 'Tipo de Operação Inválido',
        'AC': 'Tipo de Serviço inválido',
        'AD': 'Forma de Lançamento Inválida',
        'AE': 'Tipo/número de inscrição Inválido',
        'AF': 'Código de Convênio Inválido',
        'AG': 'Agência/Conta Corrente/DV Inválido',
        'AH': 'Nr Sequencial de Registro no Lote Inválido',
        'AI': 'Código de Segmento de Detalho Inválido',
        'AJ': 'Tipo de Movimento Inválido',
        'AK': 'Código da câmara de compensação do Banco Favorecido Inválido',
        'AL': 'Código do Banco Favorecido ou Depositário Inválido',
        'AM': 'Agência Mantenedora da Conta Corrente do Favorecido Inválida',
        'AN': 'Conta Corrente/DV do Favorecido Inválido',
        'AO': 'Nome do Favorecido não Informado',
        'AP': 'Data de Lançamento Inválida',
        'AQ': 'Tipo/Quantidade da Moeda Inválido',
        'AR': 'Valor do Lançamento Inválido',
        'AS': 'Aviso ao Favorecido - Identificação Inválida',
        'AT': 'Tipo/Número de Inscrição do Favorecido Inválido',
        'AU': 'Logradouro do Favorecido Não Informado',
        'AV': 'Nr do Local do Favorecido Não Informado',
        'AW': 'Cidade do Favorecido não Informada',
        'AX': 'CEP/Complemento do Favorecido Inválido',
        'AY': 'Sigla do Estado do favorecido Inválida',
        'AZ': 'Código/Nome do Banco depositário Inválido',
        'BA': 'Código/Nome da Agência depositária não Informado',
        'BB': 'Seu Número Inválido',
        'BC': 'Nosso Número Inválido',
        'BD': 'Inclusão Efetuada com Sucesso',
        'BE': 'Alteração Efetuada com Sucesso',
        'BF': 'Exclusão Efetuada com Sucesso',
        'BG': 'Agência/Conta Impedida Legalmente',
        'BH': 'Empresa não Pagou Salário',
        'BI': 'Falecimento do Mutuário',
        'BJ': 'Empresa não Enviou Remessa do Mutuário',
        'BK': 'Empresa não enviou remessa do vencimento',
        'BL': 'Valor da Parcela Inválida',
        'BM': 'Identificação do Contrato Inválida',
        'BN': 'Operação de Consignação Incluída com Sucesso',
        'BO': 'Operação de Consignação Alterada com Sucesso',
        'BP': 'Operação de Consignação Excluída com Sucesso',
        'BQ': 'Operação de Consignação Liquidada com Sucesso',
        'CA': 'Código de Barras - Código do Banco Inválido',
        'CB': 'Código de Barras - Código da Moeda Inválido',
        'CC': 'Código de Barras - DV Geral Inválido',
        'CD': 'Código de Barras - Valor do Título Divergente/Inválido',
        'CE': 'Código de Barras - Campo Livre Inválido',
        'CF': 'Valor do Documento Inválido',
        'CG': 'Valor do Abatimento Inválido',
        'CH': 'Valor do Desconto Inválido',
        'CI': 'Valor de Mora Inválido',
        'CJ': 'Valor de Multa Inválido',
        'CK': 'Valor do IR Inválido',
        'CL': 'Valor do ISS Inválido',
        'CM': 'Valor do IOF Inválido',
        'CN': 'Valor de Outras Deduções Inválido',
        'CO': 'Valor de Outros Acrescimos Inválido',
        'CP': 'Valor do INSS Inválido',
        'HA': 'Lote não Aceito',
        'HB': 'Inscrição da Empresa Inválida para o Contrato',
        'HC': 'Convênio com a Empresa Inexistente/Inválido para o Contrato',
        'HD': 'Agência/CC da Empresa Inexistente/Inválida para o Contrato',
        'HE': 'Tipo de Serviço Inválido para o Contrato',
        'HF': 'Conta Corrente da Empresa com Saldo Insuficiente',
        'HG': 'Lote de Serviço Fora da Sequência',
        'HH': 'Lote de Serviço Inválido',
        'HI': 'Arquivo não Aceito',
        'HJ': 'Tipo de Registro Inválido',
        'HK': 'Código Remessa/Retorno Inválido',
        'HL': 'Versão de Layout Inválida',
        'HM': 'Mutuário não Identificado',
        'HN': 'Tipo do Benefício não Permite Empréstimo',
        'HO': 'Benefício Cessado/Suspenso',
        'HP': 'Benefício Possui Representante Legal',
        'HQ': 'Benefício é do tipo Pensão Alimentícia',
        'HR': 'Quantidade de Contratos Permitida Excedida',
        'HS': 'Benefício não pertence ao Banco Informado',
        'HT': 'Início do desconto Informado já Ultrapassado',
        'HU': 'Número da Parcela Inválida',
        'HV': 'Quantidade de Parcela Inválida',
        'HW': 'Margem Consignável Excedida p/ o Mutuário no Prazo do Contrato',
        'HX': 'Empréstimo Já Cadastrado',
        'HY': 'Empréstimo Inexistente',
        'HZ': 'Empréstimo Já Encerrado',
        'H1': 'Arquivo sem Trailer',
        'H2': 'Mutuário Sem Crédito na Competência',
        'H3': 'Não Descontado - Outros Motivos',
        'H4': 'Retorno de Crédito não Pago',
        'H5': 'Cancelamento de Empréstimo Retroativo',
        'H6': 'Outros Motivos de Glosa',
        'H7': 'Margem Consignável Excedida p/ o Mutuário Acima\
    do Prazo do Contrato',
        'H8': 'Mutuário Desligado do Empregador',
        'H9': 'Mutuário Afastado por Licença',
        'IA': 'Primeiro nome do Mutuário Diferente do Primeiro nome do\
    Movimento do Censo/da Base do Titular do Benefício',
        'TA': 'Lote não Aceito - Totais do Lote com Diferença',
        'YA': 'Título não Encontrado',
        'YB': 'Identificador Registro Opcional Inválido',
        'YC': 'Código Padrão Inválido',
        'YD': 'Código de Ococrrência Inválido',
        'YE': 'Complemento de Ococrrência Inválido',
        'YF': 'Alegação Já Informada',
        'ZA': 'Agência/Conta do Favorecido Substituída',
        'ZB': 'Divergência no Nome do Beneficiário comparado à Receita Fed.',
        'ZC': 'Confirmação de Antecipação de Valor',
        'ZD': 'Antecipação Parcial de Valor',
        '5A': 'Agendado sob Lista de débito',
        '5B': 'Pagamento não Autoriza sob lista de débito',
        '5C': 'Lista com Mais de Uma Modalidade',
        '5D': 'Lista com Mais de Uma Data de Pagamento',
        '5E': 'Número de Lista Duplicado',
        '5F': 'Lista de Débito Vencida e Não Autorizada',
        '5M': 'Número de Lista de Débito Inválida',
        'ZE': 'Título Bloqueado na Base',
        'ZF': 'Sistema em contingência - Título Valor Maior que Referência',
        'ZG': 'Sistema em contingência - Título Vencido',
        'ZH': 'Sistema em contingência - Título Indexado',
        'ZI': 'Beneficiário Divergente',
        'ZJ': 'Limite de Pagamentos Parciais Excedidos',
        'ZK': 'Boleto Já Liquidado'
    },
     '341': {
        '00': 'Pagamento Efetuado',
        'AE': 'Data de Pagamento Alterada',
        'AG': 'Número do Lote Inválido',
        'AH': 'Número Seqüencial do Registro no Lote Inválido',
        'AI': 'Produto Demonstrativo de Pagamento não contratado',
        'AJ': 'Tipo de Movimento Inválido',
        'AL': 'Código do Banco do Favorecido Inválido',
        'AM': 'Agência do Favorecido Inválida',
        'AN': 'Conta Corrente do Favorecido Inválida/Conta de \
    Investimento extinta em 30/04/2011',
        'AO': 'Nome do Favorecido Inválido',
        'AP': 'Data de Pagamento/Validade/Arrecadação/Apuração/Hora de \
    Lançamento Inválida',
        'AQ': 'Quantidade de registros maior que 999999',
        'AR': 'Valor Arrecadado / Lançamento Inválido',
        'BC': 'Nosso Número Invalido',
        'BD': 'Pagamento Agendado',
        'BE': 'Pagamento Agendado com forma alterada para OP',
        'BI': 'CNPJ/CPF do favorecido no segmentoJ-52 ou B inválido',
        'BL': 'Valor da Parcela Inválido',
        'CD': 'CNPJ/CPF Informado Divergente do Cadastrado',
        'CE': 'Pagamento Cancelado',
        'CF': 'Valor do Documento Inválido',
        'CG': 'Valor do Abatimento Inválido',
        'CH': 'Valor do Desconto Inválido',
        'CI': 'CNPJ/CPF/Identificador/IE/Inscrição no CAD/ICMS Inválido',
        'CJ': 'Valor da multa Inválido',
        'CK': 'Tipo de Inscrição Inválida',
        'CL': 'Valor do INSS Inválido',
        'CM': 'Valor do COFINS Inválido',
        'CN': 'Conta não Cadastrada',
        'CO': 'Valor de Outras Entidades Inválido',
        'CP': 'Confirmação de OP Cumprida',
        'CQ': 'Soma das Faturas Difere do Pagamento',
        'CR': 'Valor do CSLL Inválido',
        'CS': 'Data de Vencimento da Fatura Inválida',
        'DA': 'Número de Depend. Salário Familia Inválido',
        'DB': 'Número de Horas Semanais Inválido',
        'DC': 'Salário de Contribuição INSS Inválido',
        'DD': 'Salário de Contribuição FGTS Inválido',
        'DE': 'Valor Total dos Proventos Inválido',
        'DF': 'Valor Total dos Descontos Inválido',
        'DG': 'Valor Líquido não Numérico',
        'DH': 'Valor Líquido Informado difere do Calculado',
        'DI': 'Valor do salário-base inválido',
        'DJ': 'Base de cálculo IRRF inválida',
        'DK': 'Base de cálculo FGTS inválida',
        'DL': 'Forma de pagamento Incompatível com Holerite',
        'DM': 'E-mail do Favorecido Inválido',
        'DV': 'DOC/TED Devolvido pelo banco favorecido',
        'D0': 'Finalidade do Holerite Inválida',
        'D1': 'Mês de Competência do Holerite Inválido',
        'D2': 'Dia da Competência do Holerite Inválido',
        'D3': 'Centro de Custo Inválido',
        'D4': 'Campo Numérico da Funcional Inválido',
        'D5': 'Data Início de Férias não numérica',
        'D6': 'Data Início de Férias Inconsistente',
        'D7': 'Data Fim de Férias não numérica',
        'D8': 'Data Fim de Férias Inconsistente',
        'D9': 'Número de dependentes IR inválido',
        'EM': 'Confirmação de OP emitida',
        'EX': 'Devolução de OP não sacada pelo Favorecido',
        'E0': 'Tipo de Movimento Holerite Inválido',
        'E1': 'Valor 01 do Holerite / Informe inválido',
        'E2': 'Valor 02 do Holerite / Informe inválido',
        'E3': 'Valor 03 do Holerite / Informe inválido',
        'E4': 'Valor 04 do Holerite / Informe inválido',
        'FC': 'Pagamento efetuado através de financiamento Compror',
        'FD': 'Pagamento efetuado através de financiamento Descompror',
        'HA': 'Erro no Header de Arquivo',
        'HM': 'Erro no Header de Lote',
        'IB': 'Valor e/ou Data do documento Inválido',
        'IC': 'Valor do Abatimento Inválido',
        'ID': 'Valor do Desconto Inválido',
        'IE': 'Valor da Mora Inválido',
        'IF': 'Valor da Dulta inválido',
        'IG': 'Valor da Dedução inválido',
        'IH': 'Valor do Acréscimo inválido',
        'II': 'Data de vencimento inválida',
        'IJ': 'Competência/Período referência/Parcela inválida',
        'IK': 'Tributo não liquidável via sispag ou não conveniado com Itaú',
        'IL': 'Código de pagamento/Empresa/Receita inválido',
        'IM': 'Tipo X Forma não compatível',
        'IN': 'Banco/Agência não cadastrados',
        'IO': 'DAC/Valor/Competência/Identificador do Lacre inválido',
        'IP': 'DAC do código de barras inválido',
        'IQ': 'Dívida ativa ou número de etiqueta inválido',
        'IR': 'Pagamento Alterado',
        'IS': 'Concessionária não conveniada com Itaú',
        'IT': 'Valor do tributo inválido',
        'IU': 'Valor da Receita Bruta Acumulada inválido',
        'IV': 'Número do documento origem/referência inválido',
        'IX': 'Código do produto inválido',
        'LA': 'Data de pagamentos de um Lote alterada',
        'LC': 'Lote de pagamentos cancelado',
        'NA': 'Pagamento Cancelado por falta de Autorização',
        'NB': 'Identificação do Tributo inválida',
        'NC': 'Execício (ano base) inválido',
        'ND': 'Código RENAVAM não encontrado/inválido',
        'NE': 'UF inválida',
        'NF': 'Código do município inválido',
        'NG': 'Placa Inválida',
        'NH': 'Opção/parcela de pagamento inválida',
        'NI': 'Tributo já foi pago ou está vencido',
        'NR': 'Operação não Realizada',
        'PD': 'Aquisição Confirmada (Equivale à ocorrência 02 \
    no Layout de Risco Sacado)',
        'RJ': 'Registro Rejeitado',
        'RS': 'Pagamento disponível para antecipação no risco sacado - \
    modalidade Risco Sacado pós Autorizado',
        'SS': 'Pagamento Cancelado por insuficiência de saldo/\
        Limite diário de pagamento',
        'TA': 'Lote não aceito - Totais do Lote com Diferença',
        'TI': 'Titularidade Inválida',
        'X1': 'Forma incompatível com Layout 010',
        'X2': 'Número da Nota Fiscal Inválido',
        'X3': 'Identificador de NF/CNPJ Inválido',
        'X4': 'Forma 32 Inválida'
    },
    '756': {
        '00': 'Crédito ou Débito Efetivado',
        'AJ': 'Tipo de Movimento Inválido / Erro CNAB',
        'BD': 'Inclusão Efetuada com Sucesso',
        'PD': 'Transação Pendente de Assinatura',
        'BF': 'Transação Rejeitada',
    }
}


def get_return_message(bank_code, return_code):
    try:
        return CODIGOS_RETORNO[bank_code][return_code]
    except KeyError:
        parse_keyerror(CODIGOS_RETORNO, bank_code, return_code)


def get_forma_de_lancamento(bank_name, code):
    try:
        value = FORMA_DE_LANCAMENTO[bank_name][code]
    except KeyError:
        parse_keyerror(FORMA_DE_LANCAMENTO, bank_name, code)
    return value


def get_ted_doc_finality(bank, mov_type, code, ignore=False):
    try:
        value = DOC_TED_FINALITY[bank][mov_type][code]
    except KeyError:
        if ignore:
            return ''
        parse_keyerror_finality(bank, code, finality=mov_type)
    return value


def get_tipo_de_servico(bank_name, code):
    try:
        value = TIPO_DE_SERVICO[bank_name][code]
    except KeyError:
        parse_keyerror_servico(TIPO_DE_SERVICO, bank_name, code)
    return value


def get_bank(bank_code):
    try:
        value = BANK[bank_code]
    except KeyError:
        parse_keyerror(BANK, bank_code)
    return value


def parse_keyerror(dic, bank_name, code):
    message, value = 'Code', code
    if not dic.get(bank_name):
        message, value = 'Bank', bank_name
    raise KeyError("{} {} not found!".format(message, value))


def parse_keyerror_servico(bank_name, code):
    raise KeyError("Code {} not found to {}!".format(code, bank_name))


def parse_keyerror_finality(bank_name, code, finality=False, same=False):
    if same:
        raise KeyError("Code {} not found to operation {} in {}!".format(
            code, same, bank_name))
    else:
        raise KeyError("Code {} not found to operation {} in {}!".format(
            code, finality, bank_name))


def get_subsegments_from_line(segment_name, line):
    if line[0:3] != '341':
        return get_subsegments(line[0:3], segment_name, line[132:134])
    else:
        if segment_name == 'SegmentoN':
            return get_subsegments('341', segment_name, line[17:19])
        else:
            try:
                return get_subsegments('341', segment_name, line[20:23])
            except KeyError as e:
                if 'segment code' in e.args[0]:
                    return 'SegmentoA_outros_bancos'
                else:
                    raise


def get_subsegments(bank_code, segment_name, code):
    if not SUBSEGMENTS.get(bank_code):
        raise KeyError("{}: bank code not found!".format(bank_code))
    if not SUBSEGMENTS[bank_code].get(segment_name):
        raise KeyError("{}: segment not found!".format(segment_name))
    if not SUBSEGMENTS[bank_code][segment_name].get(code):
        raise KeyError("{}: segment code not found!".format(code))
    return SUBSEGMENTS[bank_code][segment_name][code]


def pretty_format_line(digitable_line):
    line = re.sub('[^0-9]', '', digitable_line or '')
    if len(line) == 47:
        return "{}.{} {}.{} {}.{} {} {}".format(
            line[0:5], line[5:10], line[10:15], line[15:21],
            line[21:26], line[26:32], line[32:33], line[33:47])
    elif len(line) == 48:
        return "{} {} {} {}".format(
            line[0:12],
            line[12:24],
            line[24:36],
            line[36:48])
    else:
        raise Exception('Linha digitável com tamanho inválido!')


def decode_digitable_line(digitable_line):
    """
        Posição  #   Conteúdo para 47 digitos
        01 a 03  03  Número do banco
        04       01  Código da Moeda - 9 para Real
        05       01  Digito verificador do Código de Barras
        06 a 09  04  Data de vencimento em dias partis de 07/10/1997
        10 a 19  10  Valor do boleto (8 inteiros e 2 decimais)
        20 a 44  25  Campo Livre definido por cada banco
        Total    44
        ====================================================
        Posição  #   Conteúdo para 48 digitos
        01       01  Número do banco
        02       01  Identificação do Segmento
        03       01  Identificação do valor real ou referência
        04       01  Dígito verificador geral
        05 a 15  10  Valor do boleto (8 inteiros e 2 decimais)
        16 a 19  05  Identificação da Empresa/Órgão
        20 a 44  25  Campo Livre definido por cada orgão
        Total    44
    """
    digitable_line = digitable_line or ''
    barcode = ''
    DATA_BASE = date(1997, 10, 7)
    if len(digitable_line) == 47:
        test_dv_47(digitable_line)
        barcode = "{}{}{}{}{}{}".format(
            digitable_line[0:4],
            digitable_line[32],
            digitable_line[-14:],
            digitable_line[4:9],
            digitable_line[10:20],
            digitable_line[21:31])
        return {
            'barcode': barcode,
            'banco': barcode[:3],
            'vencimento': DATA_BASE + timedelta(days=int(barcode[5:9])),
            'valor': Decimal("{:.2f}".format(int(barcode[9:19]) / 100.0)),
        }
    elif len(digitable_line) == 48:
        test_dv_48(digitable_line)
        barcode = "{}{}{}{}".format(
            digitable_line[0:11],
            digitable_line[12:23],
            digitable_line[24:35],
            digitable_line[36:47],
        )
        return {
            'barcode': barcode,
            'banco': barcode[:3],
            'valor': Decimal("{:.2f}".format(int(barcode[4:15]) / 100.0)),
        }
    else:
        raise Exception('Código de barras com tamanho inválido!')


def test_dv_47(line):
    dv1 = calc_verif_dig_10(line[:10])
    dv2 = calc_verif_dig_10(line[11:21])
    dv3 = calc_verif_dig_10(line[22:32])
    if dv1 != line[10] or dv2 != line[21] or dv3 != line[32]:
        raise Exception('Informações inconsistentes! DV não confere,\
 digite a linha novamente.')


def test_dv_48(line):
    dv = calc_verif_dig_11(line)
    if dv != line[4]:
        raise Exception('Informações inconsistentes! DV não confere,\
 digite a linha novamente.')


def calc_verif_dig_10(self, strfield):
    seq = [2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    i, total = 0, ''
    for dig in reversed(strfield):
        mult = str(int(dig)*seq[i])
        total += mult
        i += 1
    total_num = sum([int(algarism) for algarism in total])
    dv = 10 - (total_num % 10)
    return 0 if dv == 10 else dv


def calc_verif_dig_11(self, strfield):
    seq = [2, 3, 4, 5, 6, 7, 8, 9]
    i, total = 0, ''
    for dig in reversed(strfield):
        mult = str(int(dig)*seq[i])
        total += mult
        i = i + 1 if i < 7 else 0
    res_div = sum([int(algarism) for algarism in total]) % 11
    dv = 0 if (res_div < 2) else (11 - res_div)
    return dv


def get_operation(bank_origin, bank_dest, titular_origin, titular_dest, op):
        same_titularity = titular_origin == titular_dest
        same_bank = bank_origin == bank_dest
        try:
            if (int(op) < 4):
                if same_titularity and not same_bank:
                    return get_forma_de_lancamento(
                        bank_origin, OPERATION_NAME['SAME_TIT'][op])
                if same_bank and not same_titularity:
                    return get_forma_de_lancamento(
                        bank_origin, OPERATION_NAME['SAME_BANK'][op])
                if same_titularity and same_bank:
                    return get_forma_de_lancamento(
                        bank_origin, OPERATION_NAME['SAME_BOTH'][op])
            return get_forma_de_lancamento(
                bank_origin, OPERATION_NAME['OTHER'][op])
        except KeyError:
            same_info = 'same bank' if same_bank else\
                'same titularity' if same_titularity else ''
            parse_keyerror_finality(bank_origin, op, same=same_info)
