from google import genai
import pandas as pd

class ReportGenerator:
    def __init__(self, api_key):
        """
        Versão atualizada 2026 usando o SDK 'google-genai' 
        para eliminar avisos de depreciação.
        """
        # Inicializa o cliente moderno
        self.client = genai.Client(api_key=api_key)
        # Usaremos o 2.0-flash que apareceu na sua lista e é super estável
        self.model_id = "gemini-2.0-flash" 

    def formatar_dados_rota(self, rota, df_destinos, veiculo_obj, custo_final):
        """Extrai as métricas reais para o prompt."""
        df_rota = df_destinos[df_destinos['id'].isin(rota)]
        
        hospitais = df_rota[df_rota['tipo'] == 'hospital'].shape[0]
        casas = df_rota[df_rota['tipo'] == 'casa'].shape[0]
        criticos = df_rota[df_rota['prioridade'] == 2].shape[0]
        carga_total = df_rota['demanda_kg'].sum() if 'demanda_kg' in df_rota.columns else len(rota)
        
        resumo = f"""
        --- DADOS DA OPERAÇÃO LOGÍSTICA ---
        Veículo: {veiculo_obj.id} ({veiculo_obj.tipo})
        Autonomia Utilizada: {custo_final:.2f}km / {veiculo_obj.autonomia_km}km
        Carga total: {carga_total:.2f}kg
        Paradas: {hospitais} Hospitais e {casas} Residências
        Nível de Prioridade: {criticos} pontos de alta urgência atendidos.
        """
        return resumo

    def gerar_relatorio_ia(self, resumo_dados):
        """Gera o relatório final utilizando o novo SDK."""
        prompt = f"""
        Você é o Supervisor de IA da Criativa Humana.
        Analise os dados desta rota hospitalar otimizada:
        {resumo_dados}
        
        Gere um relatório em Markdown com:
        1. Análise de Eficiência (Combustível vs Carga).
        2. Recomendações de segurança para o motorista.
        """
        
        try:
            # Novo padrão de chamada (generate_content)
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Erro na nova API Gemini: {str(e)}"