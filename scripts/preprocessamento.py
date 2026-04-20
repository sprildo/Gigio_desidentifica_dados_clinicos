import re

def tratar_texto(texto):
    """
    PT: Função para limpar e padronizar textos médicos para treinamento de LLMs.
    EN: Function to clean and standardize medical texts for LLM training.
    """
    
    # 1. PT: Garantir que o texto seja uma string e converter para minúsculas, pois os registros são misturados.
    #    EN: Ensure the text is a string and convert to lowercase since records are sometimes mixed.
    texto = str(texto).lower()
    
    # 2. PT: Tratamento de Registros (7 dígitos + opcionalmente 1 espaço + exatamente 1 letra)
    #    EN: Record Treatment (7 digits + optional 1 space + exactly 1 letter)
    # 
    # PT: \b      -> Fronteira de palavra (garante que não haja números antes, ex: 8 dígitos)
    # EN: \b      -> Word boundary (ensures there are no numbers before, e.g., 8 digits)
    # PT: \d{7}   -> Exatamente 7 dígitos numéricos
    # EN: \d{7}   -> Exactly 7 numeric digits
    # PT: \s?     -> Zero ou um espaço em branco (permite "1234567a" e "1234567 a")
    # EN: \s?     -> Zero or one whitespace (allows "1234567a" and "1234567 a")
    # PT: [a-z]   -> Exatamente 1 letra (como o texto já está em lower(), não precisamos de A-Z)
    # EN: [a-z]   -> Exactly 1 letter (since the text is already in lower(), we don't need A-Z)
    # PT: \b      -> Fronteira de palavra (garante que não há outras letras depois, ex: "1234567anos")
    # EN: \b      -> Word boundary (ensures there are no other letters after, e.g., "1234567anos")
    texto = re.sub(r'\b\d{7}\s?[a-z]\b', ' [REGISTRO] ', texto)
    
    # 3. PT: Limpeza de formatação e caracteres desnecessários
    #    EN: Cleaning formatting and unnecessary characters
    texto = re.sub(r'#', '', texto)        # PT: Remove as hashtags / EN: Removes hashtags
    texto = re.sub(r'"', '', texto)        # PT: Remove aspas / EN: Removes quotes
    texto = re.sub(r'[\(\)]', ' ', texto)  # PT: Substitui parênteses por espaços / EN: Replaces parentheses with spaces
    texto = re.sub(r'_+', ' ', texto)      # PT: Substitui um ou múltiplos sublinhados seguidos por um espaço / EN: Replaces one or multiple consecutive underscores with a space
    texto = re.sub(r'¿', '', texto)        # PT: Remove o ponto de interrogação invertido / EN: Removes inverted question mark
    
    # 4. PT: Tratamento de repetições (Preserva símbolos únicos que dão contexto)
    #    EN: Repetition treatment (Preserves unique symbols that provide context)
    # PT: Remove apenas quando há 2 ou mais repetições de símbolos como -, =, >, *, ~, /, . ou x
    # EN: Removes only when there are 2 or more repetitions of symbols like -, =, >, *, ~, /, . or x
    texto = re.sub(r'[-=>*~/\.x]{2,}', ' ', texto) 
    
    # 5. PT: Normalização de Espaços
    #    EN: Whitespace Normalization
    # PT: Substitui múltiplos espaços em branco e tabulações por um único espaço
    # EN: Replaces multiple whitespaces and tabs with a single space
    texto = re.sub(r'[ \t]+', ' ', texto)
    
    # 6. PT: Reduz excesso de quebras de linha
    #    EN: Reduces excessive line breaks
    texto = re.sub(r'\n{2,}', '\n', texto)
    texto = re.sub(r'[\r\n]+', '\n', str(texto))
    
    # 7. PT: Remove espaços vazios no início e no final do texto
    #    EN: Removes leading and trailing whitespaces from the text
    texto = texto.strip()
    
    return texto