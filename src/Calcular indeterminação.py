import sympy
from sympy import sympify, limit, oo, S, sqrt

def encontrar_indeterminacao(expressao_str, ponto_str):
    """
    Calcula o tipo de indeterminação de uma função em um determinado ponto.

    Args:
        expressao_str: A função como uma string.
        ponto_str: O ponto para o qual o limite tende, como uma string.

    Returns:
        Uma string representando o tipo de indeterminação ou uma mensagem.
    """
    try:
        x = sympy.Symbol('x')
        ponto = sympify(ponto_str)
        # Substitui 'sqrt' por 'sympy.sqrt' para garantir a interpretação correta
        expressao = sympify(expressao_str, locals={'sqrt': sympy.sqrt})

        # Primeiro, tenta separar em numerador e denominador, que é a verificação mais comum.
        numerador, denominador = expressao.as_numer_denom()

        if denominador != 1:
            lim_numerador = limit(numerador, x, ponto)
            lim_denominador = limit(denominador, x, ponto)

            if lim_numerador == 0 and lim_denominador == 0:
                return "0/0"
            if abs(lim_numerador) == oo and abs(lim_denominador) == oo:
                return "∞/∞"

        # Se não for uma indeterminação fracionária, verifica outros tipos.


        # Caso de potência: 1**∞, 0**0, ou ∞**0
        if expressao.is_Pow:
            base = expressao.base
            expoente = expressao.exp
            lim_base = limit(base, x, ponto)
            lim_expoente = limit(expoente, x, ponto)

            if lim_base == 1 and abs(lim_expoente) == oo:
                return "1**∞"
            elif lim_base == 0 and lim_expoente == 0:
                return "0**0"
            elif abs(lim_base) == oo and lim_expoente == 0:
                return "∞**0"

        # Caso de produto: 0 * ∞
        elif expressao.is_Mul:
            fatores = expressao.args
            # Assegura que estamos lidando com um produto simples de dois termos
            if len(fatores) == 2:
                lim_fator1 = limit(fatores[0], x, ponto)
                lim_fator2 = limit(fatores[1], x, ponto)

                if (lim_fator1 == 0 and abs(lim_fator2) == oo) or \
                   (abs(lim_fator1) == oo and lim_fator2 == 0):
                    return "0 * ∞"

        # Caso de subtração: ∞ - ∞
        elif expressao.is_Add:
            # Esta verificação é mais complexa e pode ser heurística
            termos = expressao.args
            limites_termos = [limit(termo, x, ponto) for termo in termos]
            
            tem_inf_pos = any(l == oo for l in limites_termos)
            tem_inf_neg = any(l == -oo for l in limites_termos)

            if tem_inf_pos and tem_inf_neg:
                return "∞ - ∞"

        # Se nenhuma indeterminação foi encontrada, calcula o limite.
        resultado_limite = limit(expressao, x, ponto)
        if resultado_limite.is_finite is False or isinstance(resultado_limite, sympy.AccumulationBounds):
             return "Não foi possível determinar a indeterminação de forma direta. O limite é complexo ou não existe."

        return f"O limite é {resultado_limite}, não uma forma indeterminada."

    except (sympy.SympifyError, TypeError, ValueError) as e:
        return f"Erro: Função ou ponto inválido. Detalhe: {e}"

if __name__ == "__main__":

    funcao_usuario = input()
    ponto_usuario = input()

    tipo_indeterminacao = encontrar_indeterminacao(funcao_usuario, ponto_usuario)
    print(tipo_indeterminacao)