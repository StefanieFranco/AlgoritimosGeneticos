# Nome do Projeto: Tech Challenge - Algoritimo Genético

**Objetivo:** O objetivo deste trabalho é desenvolver um sistema inteligente para otimizar rotas de distribuição de medicamentos e insumos médicos. Para isso, são utilizados algoritmos genéticos como forma de resolver uma variação do problema do caixeiro viajante (TSP).

A proposta busca aumentar a eficiência logística no contexto hospitalar, levando em consideração restrições reais, como prioridades de entrega, capacidade dos veículos e limitações operacionais do dia a dia.

Além disso, o sistema incorpora modelos de linguagem (LLMs) para gerar instruções operacionais e relatórios automatizados, facilitando a interpretação dos resultados e apoiando as equipes responsáveis pelas entregas.

O projeto simula um cenário próximo da realidade enfrentada por sistemas de saúde, onde uma distribuição eficiente de recursos pode impactar diretamente a qualidade do atendimento. Dessa forma, a solução combina técnicas de inteligência artificial e otimização para contribuir com a tomada de decisão logística.

## Equipe
* Marcelo Mendonça Lira - RM369892
* Stefanie Barcelos de Franco - RM369893

## Localização do Dataset
Nosso dataset foi gerado por funções que estão no arquivo de Seeders.ipynb, enquanto os arquivos .csv se encontram na pasta data.

## Como executar o projeto
**Baixar via Https**

https://github.com/StefanieFranco/AlgoritimosGeneticos.git

**Baixar via git**

git@github.com:StefanieFranco/AlgoritimosGeneticos.git

python -m venv .venv

.venv\Scripts\activate

pip install --upgrade pip

pip install -r requirements.txt

jupyter notebook

## Análise dos Gráficos

<img width="572" height="390" alt="image" src="https://github.com/user-attachments/assets/10696d34-5c66-4ad1-8cfa-c77e60c82f7d" />

Idade (Age): É o preditor mais forte. Note que o pico de AVC (laranja) ocorre a partir dos 60 anos, 
enquanto os casos negativos estão distribuídos em todas as idades.

<img width="582" height="383" alt="image" src="https://github.com/user-attachments/assets/eaf224fd-ec57-4433-bc26-897d809df213" />

Glicose (avg_glucose_level): Há uma distribuição bimodal. O segundo pico de glicose alta (>200) mostra 
uma concentração proporcionalmente maior de casos de AVC.

<img width="571" height="374" alt="image" src="https://github.com/user-attachments/assets/ef6b4f51-1aa1-4258-a40c-151a0c27a75c" />
<img width="573" height="378" alt="image" src="https://github.com/user-attachments/assets/d6cc486f-1484-4da7-ba8b-7e2b45c071ca" />

Desbalanceamento: O gráfico de "hypertension" e "heart_disease" mostra que, embora essas condições 
aumentem o risco, a vasta maioria da sua base não as possui e não teve AVC. Isso pode fazer com que 
modelos simples "ignorem" quem tem hipertensão por falta de exemplos positivos suficientes.

## Resultados Obtidos
Este estudo buscou desenvolver um modelo de triagem para a identificação de pacientes sob alto risco de AVC. O foco central da modelagem foi a segurança clínica, priorizando a sensibilidade (recall) para minimizar a ocorrência de falsos negativos. Após a avaliação comparativa entre os algoritmos KNN, Random Forest e Regressão Logística, esta última apresentou o desempenho mais robusto e adequado para a aplicação proposta.

Enquanto modelos como o Random Forest apresentaram dificuldades em lidar com o desbalanceamento da classe minoritária, a Regressão Logística obteve um Recall aproximado de 80%. Em um contexto de saúde pública, essa métrica é fundamental, pois garante a identificação de 80% dos casos reais, permitindo intervenções adequadas. Como exemplificado nas imagens abaixo:

<img width="551" height="464" alt="image" src="https://github.com/user-attachments/assets/55ff7258-cee2-4f6f-9ce1-d29ec9288751" />

<img width="1481" height="707" alt="image" src="https://github.com/user-attachments/assets/c5061966-0ff8-463f-844f-9a908382e426" />


Conclui-se que a Regressão Logística é a ferramenta mais indicada para compor um sistema de apoio à decisão clínica. Sua implementação pode servir como um filtro inicial de triagem, sinalizando pacientes prioritários para avaliação médica detalhada e exames confirmatórios. Lembrando que a ferramenta serve de suporte e não substitui a análise de um médico.

