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

Arquivo principal com relatório é o Result.ipynb

### Restrições Operacionais aplicadas

A função de fitness foi desenvolvida para transpor a complexidade logística do mundo real para o modelo matemático, indo além da simples minimização de distância. O cálculo baseia-se no custo operacional direto (quilometragem percorrida multiplicada pelo custo por km do veículo), ao qual é aplicado um sistema de funções de penalidade (penalty functions) que balizam a viabilidade das rotas.

#### O desempenho de cada solução é avaliado através de cinco pilares estruturais:

O processo de otimização segue as seguintes etapas:

1. **Dinâmica de Carga e Reabastecimento:**
   O modelo simula a ocupação física do veículo. Sempre que o peso total dos pedidos excede a capacidade nominal, o algoritmo obriga o retorno ao Centro de Distribuição, contabilizando um incremento fixo de 15 minutos para carregamento, além do deslocamento adicional.

2. **Gestão de Risco e Segurança:**
   O modelo incorpora uma regra de segurança patrimonial, aplicando penalidades severas para o transporte de cargas de alto valor (acima de R$ 3.000,00) em motocicletas, incentivando o uso de veículos mais seguros para itens críticos.

3. **Priorização e Urgência:**
   A função favorece o atendimento precoce a destinos sensíveis (hospitais e prioridade nível 1) através de um fator multiplicador baseado na ordem de entrega. **Complementarmente, o modelo aplica uma bonificação (redução do custo total)** quando identifica o uso eficiente de motocicletas para pedidos prioritários de baixo valor. Essa lógica incentiva o algoritmo a aproveitar a agilidade e o baixo custo desse modal para demandas urgentes que não comprometam a segurança da carga.

4. **Janelas de Atendimento e Jornada:**
   O algoritmo monitora o tempo acumulado de viagem. Se o horário de chegada em um destino de perfil "comercial" ultrapassar o limite de 8 horas de turno (480 min), a rota é penalizada por inviabilidade de cumprimento de horário.

5. **Avaliação (Fitness):**
   - Cálculo do custo total da rota considerando distância, capacidade
     do veículo, autonomia e prioridade de entregas.

6. **Autonomia e Restrições de Frota:**
   São aplicadas travas rígidas para garantir que a quilometragem total não exceda a autonomia do veículo. Além disso, o modelo restringe o uso de caminhões em contextos puramente comerciais, buscando uma alocação de frota mais eficiente para zonas urbanas densas.

## Resultados Obtidos TSP
Em exemplo executado com o seguinte detalhes
População = 150
gerações = 2000
mutação = 0.1
veículo = mini truck

<img width="2198" height="1072" alt="image" src="https://github.com/user-attachments/assets/730f6dc0-5519-48ae-b26f-e47ebd18e82c" />

<img width="2390" height="702" alt="image" src="https://github.com/user-attachments/assets/9f2f7ef1-ca64-42f4-b5e0-b30140aae6f1" />

## Resultados Obtidos VRP
Em exemplo executado com o seguinte detalhes
População = 150
gerações = 2000
mutação = 0.1
veículo = frota completa (5 motos, 5 mini trucks, 5 caminhões)


<img width="2246" height="1059" alt="image" src="https://github.com/user-attachments/assets/45207b4d-a9a6-4080-ae80-0289d06a9e12" />

<img width="2070" height="1180" alt="image" src="https://github.com/user-attachments/assets/571d04b0-157a-434c-8eee-329af1230557" />


<img width="2312" height="695" alt="image" src="https://github.com/user-attachments/assets/580df9a3-d1e4-4541-85af-926586db4694" />


