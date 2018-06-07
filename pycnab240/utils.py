FORMA_DE_LANCAMENTO = {
    'santander': {
        0: '01',  # Credito em conta corrente
        1: '03',  # Transferencias para outros bancos
        2: '05',  # Credito em conta poupanca
        3: '10',  # Ordem de pagamento / recibo
        4: '11',  # Pagamento de contas com codigo de barras
        5: '16',  # DARF Normal
        6: '17',  # GPS - Guia de previdencia social
        7: '18',  # DARF Simples
        8: '20',  # Caixa "Autenticacao"
        9: '22',  # GARE SP ICMS
        10: '23',  # GARE SP DR
        11: '24',  # GARE SP ITCMD
        12: '25',  # IPVA SP
        13: '26',  # LICENCIAMENTO SP
        14: '27',  # DPVAT SP
        15: '30',  # Liquidacao de titulos em carteira de cobranca proprio
                   # Santander Banespa
        16: '31',  # Liquidacao de titulos outros Bancos
    },
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


def parse_keyerror(dic, bank_name, code):
    message, value = 'Code', code
    if not dic.get(bank_name):
        message, value = 'Bank', bank_name
    raise KeyError("{} {} not found!".format(message, value))
