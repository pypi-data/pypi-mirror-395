"""
Common search strings for regular expressions in Python
"""

# EXPORTED DATA

# alphabetical
S_WORD                  = r'[a-zA-Z_]+'         # e.g.: 'nomen' or 'is_juicy_peach'
S_WORD_W_DOT            = r'[a-zA-Z_.]+'        # e.g.: 'n.men' or 'is_juicy.peach'
S_WORD_W_DOT_HYP        = r'[a-zA-Z_.-]+'       # e.g.: 'my-n.men' or 'is_ju.cy.pea-ch'
S_WORD_W_DOT_HYP_CLN    = r'[a-zA-Z_.-:]+'      # e.g.: 'my-n.men:t' or 'is_ju.cy:t'

# alpha-numerical
S_IDENT                 = r'[a-zA-Z0-9_]+'      # e.g.: 'nomen1' or 'is_4juicy_peach'
S_IDENT_W_DOT           = r'[a-zA-Z0-9_.]+'     # e.g.: 'n.men1' or 'is_4juicy.peach'
S_IDENT_W_DOT_HYP       = r'[a-zA-Z0-9_.\-]+'   # e.g.: 'my-n.men1' or 'is_4ju.cy_pea-ch'
S_IDENT_W_DOT_HYP_CLN   = r'[a-zA-Z0-9_.\-:]+'  # e.g.: 'my-n.men:1' or 'is_4ju.cy:77'

# numerical
S_HEX_DIGIT     = r'[0-9a-fA-F]'                # e.g. '4', 'A'
S_INTEGER       = r'[+-]?[0-9]+'                # e.g.: '123' or '-4096'
S_FLOAT_INT     = r'[+-]?[0-9]+[.]?[0-9]*'      # e.g.: '+32.' or '444.'
S_FLOAT_FRAC    = r'[+-]?[0-9]*[.]{1}[0-9]+'    # e.g.: '.9995' or '+3.14159'
S_EXPONENT      = r'[eE]?[+-]?[0-9]*'           # e.g.: 'e-2', '+E23' (if at all, else '')
S_NUMBER        = S_FLOAT_FRAC+S_EXPONENT + r'|' + S_FLOAT_INT+S_EXPONENT

# specials
S_SEP       = r'[,;]+\s*'           # separators w/ add. whitespace, e.g.: ';' or ',   '
S_SEP_W_DOT = r'[.,;]+\s*'          # separators or dot w/ add. whitespace
S_BRACKETS  = r'[\(\)\[\]\{\}]+'    # opening & closing brackets '()[]{}'
S_SPECIAL   = r'[\+\-\!§$%&<>°]+'   # special chars ('+','-','!','§','$','%','&','<','>','°')
S_DOC_STR_QUOTES = r'"""'           # opening/closing quotes for doc-strings
