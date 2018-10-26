from pycnab240 import bancos
FORMA_DE_LANCAMENTO = {
    'santander': {
        '01': '03',  # Transferências para outros bancos (DOC, TED)
        '02': '03',  # Transferências para outros bancos (DOC, TED)
        '03': '11',  # Pagamento de Títulos
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
    'itau': {
        '01': '41',  # 'Transferência (TED - outro titular)'
        '02': '07',  # 'Transferência (DOC "D" - outro titular)'
        '97': '03',  # 'Transferência (DOC "C" - mesmo titular)'
        '98': '17',  # 'Transferência (TED - mesmo titular)'
        '99': '01',  # 'Credito em CC do itau')'
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
            '01': 'Itau_Unibanco',
            '03': 'outros_bancos',
            '07': 'outros_bancos',
            '17': 'outros_bancos',
            '41': 'outros_bancos'
        }
    }
}


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


def parse_keyerror_servico(dic, bank_name, code):
    message, value = 'Code', code
    raise KeyError("{} {} not found to {}!".format(message, value, bank_name))


def get_subsegments_from_line(segment_name, line):
    if segment_name == 'SegmentoN':
        return get_subsegments(line[0:3], segment_name, line[132:134])


def get_subsegments(bank_code, segment_name, code):
    return SUBSEGMENTS.get(bank_code, {}).get(segment_name, {}).get(code)
