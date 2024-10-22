def validate_gtin(gtin: str) -> bool:
    """Valida se o GTIN fornecido é válido (suporta GTIN-8, GTIN-12, GTIN-13 e GTIN-14).
    
    Parâmetro:
    gtin (str): O número GTIN a ser validado.
    
    Retorna:
    bool: True se o GTIN for válido, False caso contrário.
    """
    # Remover espaços em branco
    gtin = gtin.strip()
    
    if len(gtin) not in [8, 12, 13, 14] or not gtin.isdigit():
        return False
    
    # Cálculo do dígito verificador (algoritmo de Luhn)
    def calculate_check_digit(gtin_without_check_digit):
        total = 0
        reverse_digits = gtin_without_check_digit[::-1]
        for i, char in enumerate(reverse_digits):
            digit = int(char)
            if i % 2 == 0:
                total += digit * 3
            else:
                total += digit
        check_digit = (10 - (total % 10)) % 10
        return check_digit
    
    # Extrair o dígito verificador do GTIN fornecido
    provided_check_digit = int(gtin[-1])
    gtin_without_check_digit = gtin[:-1]
    
    # Calcular o dígito verificador esperado
    calculated_check_digit = calculate_check_digit(gtin_without_check_digit)
    
    # Comparar o dígito verificador calculado com o fornecido
    return provided_check_digit == calculated_check_digit