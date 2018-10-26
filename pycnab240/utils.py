# -*- encoding: utf8 -*-

from pycnab240 import bancos
FORMA_DE_LANCAMENTO = {
    'santander': {
        '01': '03',  # Transferências para outros bancos (DOC, TED)
        '02': '03',  # Transferências para outros bancos (DOC, TED)
        '03': '31',  # Pagamento de Títulos
        '04': '11',  # Tributos com código de barras
        '05': '17',  # GPS - Guia de previdencia Social
        '06': '16',  # DARF Normal
        '07': '18',  # DARF Simples
        '08': '11',  # FGTS
    },
    'sicoob': {  # TODO: add esquema para quando doc e ted são
                # para a mesma titularidade e tributos são do mesmo banco
                '01': '41',  # Transferências para outros bancos (TED)
                '02': '03',  # Transferências para outros bancos (DOC)
                '03': '31',  # Pagamento de Títulos
                '04': '11',  # Tributos com código de barras
                '05': '17',  # GPS - Guia de previdencia Social
                '06': '16',  # DARF Normal
                '07': '18',  # DARF Simples
                '08': '11',  # FGTS
    },
}
BANK = {
    '756': bancos.sicoob,
    '033': bancos.santander,
    '341': bancos.itau,
    '237': bancos.bradesco
}
TIPO_DE_SERVICO = {
    'santander': {
        0: '03',  # Bloqueto Eletronico
        1: '10',  # Pagamento Dividendos
        2: '14',  # Consulta de Tributos a Pagar DETRAN com RENAVAM
        3: '20',  # Pagamento Fornecedor
        4: '22',  # Pagamento de Contas, Tributos e Impostos
        5: '29',  # Alegacao do Sacado
        6: '50',  # Pagamento Sinistros Segurados
        7: '60',  # Pagamento Despesas Viajante em Transito
        8: '70',  # Pagamento Autorizado
        9: '75',  # Pagamento Credenciados
        10: '80',  # Pagamento Representantes / Vendedores Autorizados
        11: '90',  # Pagamento Beneficios
        12: '98',  # Pagamentos Diversos
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
    }
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
        'AK': 'Código da Câmara de Compensação do Banco do Favorecido/Depositário Inválido',  #noqa
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


def get_tipo_de_servico(bank_name, code):
    try:
        value = TIPO_DE_SERVICO[bank_name][code]
    except KeyError:
        parse_keyerror(TIPO_DE_SERVICO, bank_name, code)
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


def get_subsegments_from_line(segment_name, line):
    return get_subsegments(line[0:3], segment_name, line[132:134])


def get_subsegments(bank_code, segment_name, code):
    if not SUBSEGMENTS.get(bank_code):
        raise KeyError("{}: bank code not found!".format(bank_code))
    if not SUBSEGMENTS[bank_code].get(segment_name):
        raise KeyError("{}: segment not found!".format(segment_name))
    if not SUBSEGMENTS[bank_code][segment_name].get(code):
        raise KeyError("{}: segment code not found!".format(code))
    return SUBSEGMENTS[bank_code][segment_name][code]
