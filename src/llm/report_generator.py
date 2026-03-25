import os
from dotenv import load_dotenv
from google import genai

# Carrega as variáveis do arquivo .env
load_dotenv()

# Busca a chave da variável de ambiente
api_key = os.getenv("GEMINI_API_KEY")

# Verifica se a chave foi encontrada para evitar erros chatos
if not api_key:
    raise ValueError("ERRO: A GEMINI_API_KEY não foi encontrada no arquivo .env")

# Substitua pela sua chave real
client = genai.Client(api_key=api_key)

def gerar_relatorio_llm_logistica(df_results, tipo_problema="VRP"):
    """
    Gera um relatório customizado via Gemini 1.5 Flash.
    tipo_problema: "VRP" ou "TSP"
    """
    # Pega o melhor experimento da tabela
    melhor_exp = df_results.loc[df_results['best_fitness'].idxmin()]
    
    v_nome = melhor_exp.get('veiculo', 'Frota Mista')
    fitness = melhor_exp['best_fitness']
    pop = melhor_exp['population']
    gen = melhor_exp['generations']
    mut = melhor_exp['mutation']

    # --- SEPARAÇÃO DOS PROMPTS POR TIPO DE PROBLEMA ---
    if tipo_problema == "VRP":
        contexto_especifico = f"""
        CONTEXTO: Problema de Roteamento de Veículos (VRP) com Frota Heterogênea.
        FOCO DA ANÁLISE: Gestão de múltiplos veículos simultâneos.
        DETALHE: Observe como a carga foi distribuída. A 'Lógica de Fragmentação' permitiu que motos 
        e mini-caminhões operassem em alta rotatividade (múltiplas viagens).
        """
        instrucao_extra = "Analise a sinergia da frota e a viabilidade de usar veículos menores para reduzir custos."
    
    else: # Caso seja TSP
        contexto_especifico = f"""
        CONTEXTO: Problema do Caixeiro Viajante (TSP) com veículo único ({v_nome}).
        FOCO DA ANÁLISE: Sequenciamento de rota e custo de deslocamento individual.
        DETALHE: O custo de R$ {fitness:,.2f} reflete as sucessivas idas e vindas ao CD 
        devido à capacidade limitada do veículo {v_nome}.
        """
        instrucao_extra = f"Avalie se a estratégia de usar apenas o veículo {v_nome} é sustentável ou se o custo de reabastecimento está alto demais."

    # --- PROMPT FINAL UNIFICADO ---
    prompt = f"""
    Atue como um Engenheiro de Logística Sênior. 
    {contexto_especifico}

    DADOS DO EXPERIMENTO VENCEDOR:
    - Custo Final (Fitness): R$ {fitness:,.2f}
    - Parâmetros: {gen} gerações, população {pop}, mutação {mut*100}%

    TAREFA:
    Escreva um parágrafo técnico (máximo 120 palavras) para um relatório de diretoria.
    1. Seja direto e use um tom de auditoria técnica.
    2. {instrucao_extra}
    3. Mencione que o algoritmo priorizou Hospitais conforme a regra de negócio.
    4. Comente se a curva de aprendizado (fitness) indica que o resultado é satisfatório ou se precisa de mais gerações.
    """

    try:
        # 3. Chamada utilizando a nova estrutura da google-genai
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Erro ao gerar relatório: {str(e)}"
    