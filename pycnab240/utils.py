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


def get_forma_de_lancamento(bank_name, code):
    try:
        value = FORMA_DE_LANCAMENTO[bank_name][code]
    except KeyError:
        message = 'Code'
        if not FORMA_DE_LANCAMENTO.get(bank_name):
            message = 'Bank'
        raise KeyError("{} not found!".format(message))
    return value
