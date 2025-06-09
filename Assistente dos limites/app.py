from flask import Flask, request, jsonify, render_template
from sympy import sympify, limit, oo, zoo, S

app = Flask(__name__)


from sympy import sympify, limit, oo, zoo, S, Add, Mul, Pow, sqrt


from sympy import sympify, limit, oo, zoo, S, Add, Mul, Pow, sqrt

# --- FUNÇÃO DE CÁLCULO COM TAGS <strong> ---
def calcular_limite_e_verificar_indeterminacao(f_str, ponto_str):
    try:
        x = S('x')
        f = sympify(f_str, locals={'sqrt': sqrt})
        
        if 'oo' in ponto_str:
            ponto = oo if '-' not in ponto_str else -oo
        else:
            ponto = S(ponto_str)

        lim_final = limit(f, x, ponto)
        indeterminacao_tipo = None

        if f.is_rational_function() or (f.as_numer_denom()[1] != 1):
            numerador, denominador = f.as_numer_denom()
            lim_numerador = limit(numerador, x, ponto)
            lim_denominador = limit(denominador, x, ponto)
            if lim_numerador == 0 and lim_denominador == 0:
                indeterminacao_tipo = "Indeterminação do tipo 0/0"
            elif lim_numerador in [oo, -oo] and lim_denominador in [oo, -oo]:
                indeterminacao_tipo = "Indeterminação do tipo ∞/∞"
        
        elif isinstance(f, Add):
            limites_termos = [limit(termo, x, ponto) for termo in f.as_ordered_terms()]
            if oo in limites_termos and -oo in limites_termos:
                indeterminacao_tipo = "Indeterminação do tipo ∞ - ∞"
        
        elif isinstance(f, Mul):
            limites_fatores = [limit(fator, x, ponto) for fator in f.as_ordered_factors()]
            if 0 in limites_fatores and (oo in limites_fatores or -oo in limites_fatores):
                indeterminacao_tipo = "Indeterminação do tipo 0 * ∞"
        
        elif isinstance(f, Pow):
            base = f.base
            expoente = f.exp
            lim_base = limit(base, x, ponto)
            lim_expoente = limit(expoente, x, ponto)
            if lim_base == 1 and lim_expoente in [oo, -oo]:
                indeterminacao_tipo = "Indeterminação do tipo 1^∞"
            elif lim_base == 0 and lim_expoente == 0:
                indeterminacao_tipo = "Indeterminação do tipo 0^0"
            elif lim_base in [oo, -oo] and lim_expoente == 0:
                indeterminacao_tipo = "Indeterminação do tipo ∞^0"

        if indeterminacao_tipo:
            return f"Detectada uma <strong>{indeterminacao_tipo}</strong>. Após os cálculos, o resultado do limite é <strong>{lim_final}</strong>."
        else:
            return f"O limite é <strong>{lim_final}</strong>. Não foi detectada uma indeterminação comum."

    except Exception as e:
        return f"Erro ao processar a função: {e}. Verifique a sintaxe."


# --- FUNÇÃO DE SUGESTÃO COM TAGS <strong> ---
def sugerir_metodos(texto_resultado):
    tipo_indeterminacao = ""
    if "<strong>Indeterminação do tipo" in texto_resultado:
        # Pega o texto entre a primeira tag <strong> e </strong>
        tipo_indeterminacao = texto_resultado.split('<strong>')[1].split('</strong>')[0]

    if tipo_indeterminacao == "Indeterminação do tipo 0/0":
        return [
            "<strong>Regra de L'Hôpital:</strong> Derive o numerador e o denominador e calcule o limite novamente.",
            "<strong>Fatoração e Simplificação:</strong> Fatore os polinômios para cancelar termos comuns.",
            "<strong>Racionalização:</strong> Multiplique pelo conjugado (comum em funções com raízes)."
        ]
    elif tipo_indeterminacao == "Indeterminação do tipo ∞/∞":
        return [
            "<strong>Regra de L'Hôpital:</strong> Derive o numerador e o denominador.",
            "<strong>Dividir pela Maior Potência:</strong> Divida todos os termos pela maior potência de x no denominador.",
            "<strong>Análise de Ordem de Grandeza:</strong> Compare o crescimento das funções."
        ]
    elif tipo_indeterminacao == "Indeterminação do tipo ∞ - ∞":
        return [
            "<strong>Racionalização (Multiplicar pelo Conjugado):</strong> Método mais comum para expressões com raízes.",
            "<strong>Encontrar um Denominador Comum:</strong> Para unir os termos em uma única fração e tentar chegar a 0/0 ou ∞/∞.",
            "<strong>Colocar o Termo de Maior Grau em Evidência.</strong>"
        ]
    elif tipo_indeterminacao in ["Indeterminação do tipo 1^∞", "Indeterminação do tipo 0^0", "Indeterminação do tipo ∞^0"]:
         return [
            "<strong>Utilizar o Limite Exponencial Fundamental:</strong> Reescreva a expressão usando a forma `e^ln(f(x)) = f(x)`.",
            "<strong>Aplicação de Logaritmos:</strong> Aplique `ln` dos dois lados para 'baixar' o expoente e então calcule o limite da expressão resultante.",
            "Transforme a expressão para que o resultado do novo limite seja o expoente de `e`."
        ]
    elif tipo_indeterminacao == "Indeterminação do tipo 0 * ∞":
        return [
            "<strong>Manipulação Algébrica:</strong> Reescreva a expressão como uma fração para transformá-la em 0/0 ou ∞/∞.",
            "Exemplo: `f(x) * g(x)` pode ser reescrito como `f(x) / (1/g(x))`."
        ]
    else:
        return []
    
# Rota principal que serve o arquivo HTML
@app.route('/')
def index():
    return render_template('index.html')

# Rota da API que o JavaScript vai chamar
# app.py -> Substitua a função calcular() por esta

# Rota da API que o JavaScript vai chamar

@app.route('/calcular', methods=['POST'])
def calcular():
    data = request.get_json()
    funcao_usuario = data.get('funcao')
    
    if not funcao_usuario:
        return jsonify({'erro': 'Nenhuma função fornecida'}), 400

    try:
        # A melhor forma é dividir a string diretamente pelo separador "x->"
        if 'x->' not in funcao_usuario:
            raise ValueError("Separador 'x->' não encontrado.")

        partes = funcao_usuario.split('x->')
        
        if len(partes) != 2:
            raise ValueError("Formato inválido. Use 'x->' apenas uma vez.")

        funcao_str = partes[0].replace('lim', '').strip()
        ponto_str = partes[1].strip()

        # Verifica se a função ou o ponto não ficaram vazios após o split
        if not funcao_str or not ponto_str:
            raise ValueError("A função ou o ponto do limite estão vazios.")

    except ValueError as e:
        return jsonify({
            'tipo': 'Erro de Formato',
            'metodos': [
                f"Erro na formatação: {e}",
                "Por favor, use o formato: `(função) x->ponto`",
                "Exemplo: `(x**2 - 1)/(x - 1) x->1`"
            ]
        })
    # --- FIM DA LÓGICA DE PARSING ---

    tipo_indeterminacao = calcular_limite_e_verificar_indeterminacao(funcao_str, ponto_str)
    metodos_sugeridos = sugerir_metodos(tipo_indeterminacao)
    
    return jsonify({
        'tipo': tipo_indeterminacao,
        'metodos': metodos_sugeridos
    })

if __name__ == '__main__':
    app.run(debug=True)