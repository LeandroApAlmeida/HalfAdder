"""
===============================================================================

 CIRCUITO HALF ADDER QUÂNTICO


 Este programa implementa um Half Adder (meio somador) reversível de 2 qubits de
 entrada (A e B) e 2 qubits auxiliares (SUM e CARRY), utilizando portas CNOT
 (Controlled-NOT gate) e CCX (Toffoli Gate), realizando a seguinte sequência de
 transformações unitárias no espaço de Hilbert de 4 qubits:


   |0,0,B,A⟩
       ↓
   |0,A,B,A⟩
       ↓
   |0,A⊕B,B,A⟩
       ↓
   |A⋅B,A⊕B,B,A⟩


 Como o programa é implementado com Qiskit, que usa little-endian (|q₃,q₂,q₁,q₀⟩),
 será utilizada esta convenção na notação de Dirac (bra-ket). Dessa forma, a ordem
 dos qubits no vetor será a seguinte:


   |CARRY,SUM,B,A⟩


 Para o sistema com 4 qubits deste circuito, existem 2⁴ = 16 estados básicos possíveis.
 Estes 16 estados formam uma base ortonormal para o espaço de Hilbert ℋ = ℂ¹⁶,
 chamada de base computacional:


   |0000⟩
   |0001⟩
   |0010⟩
   |0011⟩
   |0100⟩
   |0101⟩
   |0110⟩
   |0111⟩
   |1000⟩
   |1001⟩
   |1010⟩
   |1011⟩
   |1100⟩
   |1101⟩
   |1110⟩
   |1111⟩
​

 Um sistema quântico pode estar em um desses estados ou pode existir em uma superposição
 de vários estados ou todos ao mesmo tempo. Este é o ponto chave para entender o
 circuito quântico implementado neste código-fonte.

 Superposição é um princípio fundamental da mecânica quântica que afirma que um
 sistema quântico pode existir em uma combinação de múltiplos estados possíveis
 simultaneamente até que uma medição seja realizada. Quando ocorre a medição, o
 sistema deixa de ser descrito pela superposição e passa a apresentar um único
 resultado observável, processo conhecido como colapso da função de onda.

 Para facilitar o entendimento, imagine uma moeda sobre uma mesa. A face visível
 da moeda pode estar em apenas um de 2 estados: cara ou coroa. Agora, imagine que
 a moeda foi lançada e está girando no ar. Enquanto ela gira, não podemos descrever
 seu estado como cara ou coroa. Ela está numa condição que envolve ambas as
 possibilidades até que seja observada ao cair. Muito a grosso modo, a superposição
 se parece com isso, com uma diferença fundamental: uma moeda girando ainda possui
 um estado físico bem definido em cada instante (cara ou coroa). Um sistema quântico
 é uma combinação desses dois estados ao mesmo tempo.

 Em computação quântica, a superposição é uma propriedade essencial dos qubits.
 Enquanto um bit clássico pode assumir apenas os valores 0 ou 1, um qubit pode
 existir em uma combinação dos estados 0 e 1 ao mesmo tempo. Isso permite que um
 sistema quântico represente simultaneamente diversas possibilidades, constituindo
 a base para algoritmos quânticos capazes de explorar espaços de solução de forma
 mais eficiente do que algoritmos clássicos em determinados tipos de problemas.

 Matematicamente, o principio da superposição quântica diz que a combinação linear
 de dois ou mais vetores de estados no mesmo espaço de Hilbert, também é um estado
 do sistema. Para entender isso, considere um sistema com um único qubit. Nele, os
 estados são representados pelos vetores:


   |0⟩
   |1⟩


 onde:


         ┌ ┐
         │1│
   |0⟩ = │ │
         │0│
         └ ┘

         ┌ ┐
         │0│
   |1⟩ = │ │
         │1│
         └ ┘


 Os vetores |0⟩ e |1⟩ formam a base computacional no espaço de Hilbert ℋ = ℂ².
 
 A superposição dos vetores |0⟩ e |1⟩ é representada por:


   |ψ⟩ = α|0⟩ + β|1⟩


 onde α e β são números complexos que representam as amplitudes para cada estado
 (são coeficientes complexos do vetor de estado que indicam "quanto" de cada estado
 base existe na decomposição).

 Medindo o qubit, ele vai assumir o estado |0⟩ ou |1⟩. Pela regra de Born, as
 probabilidades de medir |0⟩ ou |1⟩ são calculadas, respectivamente, como:


   P(0) = ∣α∣²

   P(1) = ∣β∣²


 Como a soma das probabilidades de todos os resultados possíveis deve ser 1, então:


   |α|² + |β|² = 1


 é a condição de normalização de um qubit. Significa que a soma das probabilidades
 de todos os resultados possíveis deve ser 100%.

 Por exemplo, considere:


   α = (√3/2)

   β = (1/2)


 então:


   |α|² = (√3/2)² = 3/4

   |β|² = (1/2)² = 1/4


 Logo:


   3/4 + 1/4 = 1


 Isso significa que neste sistema:


   > Há 75% de probabilidade de medir |0⟩ (|α|² = 3/4).

   > Há 25% de probabilidade de medir |1⟩ (|β|² = 1/4).

   > Somando 75% de probabilidade de medir |0⟩ e 25% de probabilidade de medir |1⟩,
     obtém-se 100%, o que condiz com a condição de normalização imposta.
 

 Ampliando o espaço de Hilbert para 4 qubits, temos que, se cada qubit individual
 i possui um espaço de Hilbert ℋᵢ = ℂ², o sistema combinado de 4 qubits é o produto
 tensorial desses quatro espaços:


   ℋₜ = ℋ₁ ⊗ ℋ₂ ⊗ ℋ₃ ⊗ ℋ₄ = ℂ² ⊗ ℂ² ⊗ ℂ² ⊗ ℂ² = ℂ¹⁶


 O produto tensorial de 4 qubits combina os estados individuais de cada qubit para
 formar um único vetor de estado global em um espaço de Hilbert de 16 dimensões
 (ℋ = ℂ¹⁶).

 Com isso, a base computacional, que com 1 qubit era:


   |0⟩
   |1⟩


 agora passa a ser:


   |0000⟩
   |0001⟩
   |0010⟩
   |0011⟩
   |0100⟩
   |0101⟩
   |0110⟩
   |0111⟩
   |1000⟩
   |1001⟩
   |1010⟩
   |1011⟩
   |1100⟩
   |1101⟩
   |1110⟩
   |1111⟩
 

 Como regra geral, para n qubits:


             ⊗n
   ℋₙ = (ℂ²)


 A dimensão é calculada como:


   dim(ℋₙ) = 2ⁿ


 Dessa relação surge o crescimento exponencial do espaço de estados quânticos. Em
 decorrência disso, podemos simular circuitos com apenas alguns poucos qubits usando
 um computador clássico, pois o espaço de Hilbert cresce exponencialmente conforme
 adicionamos mais qubits, consumindo rapidamente todos os recursos de memória e
 processamento para representá-lo.

 Na tabela abaixo, calculei alguns valores de dim(ℋₙ) apenas para demonstração de
 como se dá este crescimento exponencial:


   ┌─────────────┬─────────────────┐
   │  Qubits (n) │ Dimensão (dim)  │       
   ╞═════════════╪═════════════════╡
   │ 1           │ 2               │
   ├─────────────┼─────────────────┤  
   │ 2           │ 4               │
   ├─────────────┼─────────────────┤    
   │ 3           │ 8               │
   ├─────────────┼─────────────────┤
   │ 4           │ 16              │
   ├─────────────┼─────────────────┤
   │ 5           │ 32              │
   ├─────────────┼─────────────────┤
   │ 10          │ 1.024           │
   ├─────────────┼─────────────────┤
   │ 20          │ 1.048.576       │
   ├─────────────┼─────────────────┤
   │ 50          │ 1,12 × 10¹⁵     │
   ├─────────────┼─────────────────┤
   │ 100         │ 1,26 × 10³⁰     │
   ├─────────────┼─────────────────┤
   │ 500         │ 3,27 × 10¹⁵⁰    │
   ├─────────────┼─────────────────┤
   │ 1.000       │ 1,07 × 10³⁰¹    │
   ├─────────────┼─────────────────┤
   │ 10.000      │ 1,99 × 10³⁰¹⁰   │
   ├─────────────┼─────────────────┤
   │ 100.000     │ 9,99 × 10³⁰¹⁰²  │
   ├─────────────┼─────────────────┤
   │ 1.000.000   │ 9,99 × 10³⁰¹⁰²⁹ │ 
   └─────────────┴─────────────────┘


 Observe que com apenas 500 qubits, o sistema já têm ordens de grandezas mais
 estados que o número de átomos estimado no universo observável, calculado em cerca
 de 1 × 10⁸⁰.

 É importante não confundir dimensão com quantidade de estados quânticos possíveis.

 Quando dizemos:


   dim(ℋ₄) = 16


 significa que o espaço de Hilbert de 4 qubits possui 16 vetores de base ortonormal.
 Mas estes estados da base computacional são apenas os "eixos" do espaço vetorial
 ℂ¹⁶, onde:


   |0000⟩ = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
   |0001⟩ = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
   |0010⟩ = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
   |0011⟩ = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
   |0100⟩ = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
   |0101⟩ = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
   |0110⟩ = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
   |0111⟩ = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
   |1000⟩ = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
   |1001⟩ = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
   |1010⟩ = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
   |1011⟩ = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
   |1100⟩ = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
   |1101⟩ = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
   |1110⟩ = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
   |1111⟩ = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

   * Os valores 0 e 1 nos vetores correspondentes a cada estado
     são amplitudes de probabilidades (αᵢ). No estado |0000⟩,
     por exemplo, apenas α₀ é 1 (100%). Demais amplitudes são
     0 (0%).


 Qualquer estado de 4 qubits pode ser escrito como uma combinação linear:


         15              15
         ⎲              ⎲
   ∣ψ⟩ = ⎳ αᵢ|i⟩  com   ⎳ |αᵢ|² = 1
         i=0             i=0


 Como os coeficientes αᵢ são números complexos contínuos, o conjunto de estados
 possíveis forma um espaço contínuo dentro de ℂ¹⁶, apesar da dimensão ser finita.
 Isso implica que existem infinitos estados possíveis, no sentido de que há infinitas
 escolhas possíveis de amplitudes αᵢ que satisfazem a condição de normalização. Os
 vetores da base computacional, portanto, não representam todos os estados possíveis,
 mas apenas um conjunto de vetores ortonormais de referência que permite expressar
 qualquer estado do espaço de Hilbert.

 A termos de comparação, considere o plano cartesiano ℝ² abaixo: os vetores (1,0)
 e (0,1) definem os eixos do plano, mas não esgotam seus pontos. O vetor (3,3),
 por exemplo, também pertence ao plano, assim como outros infinitos pontos em ℝ². 


     y
     
     │           (3,3)
   3 │          ◌ 
     │                      
   2 │
     │(0,1)
   1 ●
     │   (1, 0)
   0 ┼──●───────────  x
        1   2   3
 

 Um circuito quântico atua linearmente sobre qualquer estado do espaço de Hilbert.
 Isso significa que a mesma transformação unitária é aplicada ao estado quântico
 completo, afetando simultaneamente todos os componentes da superposição. Isso
 não corresponde a paralelismo clássico no sentido tradicional, mas à evolução
 linear de um vetor de estado no espaço de Hilbert.

 No circuito Half Adder quântico implementado neste projeto, as operações aplicadas
 são:


   CNOT(A → SUM)
   CNOT(B → SUM)
   CCX(A,B → CARRY)


 A evolução linear é dada por:


   |ψout⟩ = U_CCX(A,B → CARRY)⋅U_CNOT(B→SUM)⋅U_CNOT(A→SUM) |ψin⟩


 O circuito é inicializado em:


   |0,0,B,A⟩


 e produz como resultado da sequência de operações:


   |A⋅B,A⊕B,B,A⟩


 A tabela verdade para o circuito é a seguinte:


   ┌─────┬─────┬─────┬───────┬───────────────────────┐
   │  A  │  B  │ SUM │ CARRY │ OPERAÇÃO              │       
   ╞═════╪═════╪═════╪═══════╪═══════════════════════╡
   │ |0⟩ │ |0⟩ │ |0⟩ │  |0⟩  │ 0 + 0 = 0 → CARRY 0   │
   ├─────┼─────┼─────┼───────┼───────────────────────┤  
   │ |0⟩ │ |1⟩ │ |1⟩ │  |0⟩  │ 0 + 1 = 1 → CARRY 0   │
   ├─────┼─────┼─────┼───────┼───────────────────────┤    
   │ |1⟩ │ |0⟩ │ |1⟩ │  |0⟩  │ 1 + 0 = 1 → CARRY 0   │
   ├─────┼─────┼─────┼───────┼───────────────────────┤ 
   │ |1⟩ │ |1⟩ │ |0⟩ │  |1⟩  │ 1 + 1 = 0 → CARRY 1 * │ 
   └─────┴─────┴─────┴───────┴───────────────────────┘
   * 1₂ + 1₂ = 10₂. Como na soma em decimal, mantém-se
     o 0 e "sobe" 1. O carry é o valor que "sobe" na 
     soma binária pelo meio-somador.


 Observe que se trata da mesma tabela de um circuito Half Adder clássico. Mas
 diferentemente de um Half Adder clássico, este circuito não é hardwired (impresso
 no chip), e sim programado temporalmente durante a execução.
 
 Representando o circuito em um Diagrama de Circuito Quântico:


             ┌───┐                              ┌─┐
   q0(A)  ───┤ H ├─────■─────────────────■──────┤M├──────────────
             └───┘     │                 │      └╥┘
             ┌───┐     │                 │       ║  ┌─┐
   q1(B)  ───┤ X ├─────┼─────────■───────■───────╫──┤M├──────────
             └───┘     │         │       │       ║  └╥┘ 
                     ┌─┴─┐     ┌─┴─┐     │       ║   ║  ┌─┐
   q2(S)  ───────────┤ X ├─────┤ X ├─────┼───────╫───╫──┤M├──────
                     └───┘     └───┘     │       ║   ║  └╥┘
                                       ┌─┴─┐     ║   ║   ║  ┌─┐
   q3(C)  ─────────────────────────────┤ X ├─────╫───╫───╫──┤M├──
                                       └───┘     ║   ║   ║  └╥┘
                                                 ║   ║   ║   ║
   c:   4/═══════════════════════════════════════╩═══╩═══╩═══╩═══
                                                 0   1   2   3


 Com A em superposição A = α∣0⟩ + β∣1⟩, B = |1⟩, SUM = |0⟩ e CARRY = |0⟩ inicialmente,
 quando forem aplicadas as portas CNOT e CCX na sequência de operações do circuito,
 o estado do sistema passará a ser uma superposição de dois estados:


   ∣ψ⟩ = α∣0110⟩ + β∣1011⟩
 

 Os dois ramos da superposição têm origem na superposição inicial do qubit A, enquanto
 as portas CNOT e CCX propagam essa estrutura para os demais qubits, gerando correlações
 quânticas, incluindo o emaranhamento entre A, SUM e CARRY. Dessa forma, cada componente
 evolui de maneira consistente sob a mesma transformação unitária. B influencia o
 estado global, porém está desacoplado (não emaranhado). Ele atua como como qubit
 clássico controlador fixo no circuito.

 Emaranhamento quântico, ou entrelaçamento quântico, é um fenômeno em que dois ou
 mais sistemas quânticos passam a ser descritos por um único estado quântico conjunto,
 de modo que não é possível descrever completamente cada sistema de forma independente.
 Em termos matemáticos, um estado emaranhado não pode ser escrito como o produto dos
 estados individuais dos subsistemas.

 Por exemplo, considere um sistema de dois qubits no estado:


   ∣ψ⟩ = 1/√2 (|00⟩ + ∣11⟩)


 Se medirmos o primeiro qubit e o resultado for 0, o segundo qubit também será 0.
 Se o resultado for 1, o segundo também será 1. No caso, as medições estarão
 correlacionadas.

 Usando uma analogia, imagine duas caixas fechadas contendo cartões. Você sabe apenas
 que existem duas possibilidades: ou as duas caixas contêm um cartão azul cada uma,
 ou um cartão vermelho, mas você não sabe qual das duas situações ocorrerá. Ao abrir
 a primeira caixa, se encontrar o cartão azul, sabe imediatamente que da outra também
 é azul. Se encontrar o cartão vermelho, sabe que da outra é vermelho. Muito a grosso
 modo, emaranhamento é isto. Ele estabelece uma correlação entre as partículas
 emaranhadas. Mas esta correlação não pode ser explicada por simples "cartões escondidos"
 previamente determinados, como nesse exemplo, conforme foi demonstrado experimentalmente
 por testes das desigualdades de Bell.

 Na computação quântica, o emaranhamento permite que qubits compartilhem informação
 quântica de forma que o estado do sistema completo não possa ser decomposto em estados
 independentes. Quando as portas CNOT e Toffoli emaranharem A, SUM e CARRY na sequência
 de operações do circuito, estes qubits passarão a formar um único sistema. Ler 1 em A,
 acarreta que SUM seja 0 e CARRY seja 1. Ler 0, que SUM seja 1 e CARRY seja 0. Os
 resultados passam a guardar esta correlação.
   
 Para o caso de superposição uniforme em A (∣A⟩ = (∣0⟩ + ∣1⟩)/√2), o estado final
 torna-se:


   ∣ψ⟩ = 1/√2 (|0110⟩ + ∣1011⟩)


 Isso implica que, ao realizar uma medição, o sistema colapsa para |0110⟩ ou |1011⟩
 com probabilidade 50% para cada estado. Como não há um mecanismo de interferência
 projetado para amplificar um resultado específico, as amplitudes permanecem balanceadas
 conforme a evolução linear do circuito.
 
 Neste circuito não será simulado decoerência por uma questão de simplificação 
 do código. Isso seria possível usando o módulo qiskit_aer.noise. A decoerência é
 o processo pelo qual um sistema quântico perde coerência de fase devido à interação
 indesejada e inevitável com o ambiente externo (ruído térmico, campos magnéticos,
 etc.), fazendo com que seu comportamento efetivo se aproxime do comportamento clássico.
 É por este motivo que os computadores quânticos atuais tem mecanismos para geração
 de temperaturas criogênicas, afim de evitar ruído térmico, e funcionam em salas
 isoladas para tentar evitar os outros tipos de ruídos.

 Quando ocorre a decoerência, há:
 
 
   1. Perda de Fase (Dephasing): O ambiente atua como uma medição constante e 
   indesejada, destruindo a relação de fase sutil entre as amplitudes complexas
   (os αi do espaço de Hilbert).
                                                                 
   2. Transição de Estado: O estado de superposição (|0⟩ + |1⟩)/√2 colapsa para 
   uma mistura puramente clássica (ou é |0⟩, ou é |1⟩, sem propriedades de 
   interferência). Em um sistema quântico, toda vez que há medição ele colapsa 
   para um estado definido (colapso da função de onda).
   
   3. Dissipação de Energia (Relaxamento): Além da perda de fase, a decoerência 
   frequentemente caminha junto com o relaxamento térmico. O sistema quântico 
   troca energia com o ambiente até atingir o equilíbrio. Para um qubit, isso 
   geralmente significa decair de um estado de maior energia (|1⟩) de volta para 
   o estado fundamental (|0⟩).
 
 
 Em um hardware real afetado por ruído, como o IBMQ, por exemplo, o resultado 
 final medido diverge das probabilidades ideais calculadas por este programa.

===============================================================================
"""


"""
===============================================================================

INSTALAÇÃO DO QISKIT E QISKIT-AER NO PYTHON:


Com o Python instalado, abra o terminal do Windows (cmd) e digite:


  pip install qiskit

  
Tecle ENTER e aguarde a instalação terminar.

Abra novamente o terminal e digite:


  pip install qiskit-aer

  
Tecle ENTER e aguarde a instalação terminar.

Com isso, é instalado o framework para programação para o computador quântico
da IBM (IBMQ) e o simulador, para testar o código na máquina local.

Para instalar os utilitários de visualização de gráficos, abra o terminal e digite: 


  pip install "qiskit[visualization]" matplotlib pylatexenc
  
  
Tecle ENTER e aguarde a instalação terminar.

===============================================================================
"""

import os
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector, Operator
from qiskit.visualization import (
    plot_histogram,
    plot_state_city, 
    plot_bloch_multivector, 
    plot_state_qsphere
)


# =============================================================================
# Implementação do circuito Half Adder quântico
# =============================================================================


# Cria um circuito quântico e o armazena na variável qc. Os  argumentos (4, 4) 
# definem a estrutura e o tamanho do circuito:
#
# O primeiro 4: Aloca 4 qubits de registradores quânticos. Eles são inicializados 
# automaticamente no estado padrão |0⟩ e são indexados como 0, 1, 2 e 3 (q0, q1, 
# q2 e q3).
#
# O segundo 4: Aloca 4 bits de registradores clássicos, também indexados de 0 a
# 3. Eles servem para armazenar os resultados numéricos (0 ou 1) quando medir os
# qubits, cada um representando o valor do qubit no respectivo índice.
#
# No contexto deste programa, que implementa um Half Adder quântico, os 4 qubits 
# representam:
#
#   > Índice 0 (q0): Entrada A.
#
#   > Índice 1 (q1): Entrada B.
#
#   > Índice 2 (q2): Soma A⊕B (SUM - bit menos significativo).
#
#   > Índice 3 (q3): Carry A⋅B (vai um).

qc = QuantumCircuit(4, 4)


# Aplica uma porta lógica quântica X, também conhecida como porta NOT quântica 
# ou Bit-Flip, em q1. Isso inverte o estado do qubit de |0⟩ para |1⟩, fixando a
# entrada B do circuito neste valor.

qc.x(1)


# Aplica a porta Hadamard (H) em q0 (A). Isso transforma |0⟩ em (|0⟩ + |1⟩)/√2, 
# colocando a entrada A nos estados |0⟩ e |1⟩ em superposição.
#
# Com o emaranhamento de A, SUM e CARRY na sequência de operações unitárias aplicadas
# adiante no código, o estado global passa a ser uma superposição de dois estados:
#
#   |ψ⟩ = 1/√2 (|0110⟩ + ∣1011⟩)
#
# Devido à linearidade da transformação unitária, o circuito Half Adder processará
# as duas ramificações da superposição simultaneamente:
#
#   Ramo 1:
#
#   A = |0⟩, B = |1⟩ ⇒ SUM = |0⟩⊕|1⟩ = |1⟩, CARRY = |0⟩⋅|1⟩ = |0⟩ ⇒ |0110⟩
#
#   Ramo 2: 
#
#   A = |1⟩, B = |1⟩ ⇒ SUM = |1⟩⊕|1⟩ = |0⟩, CARRY = |1⟩⋅|1⟩ = |1⟩ ⇒ ∣1011⟩
#
# Como dito anteriormente, isso não corresponde a paralelismo clássico no sentido
# tradicional, mas à evolução linear de um vetor de estado no espaço de Hilbert.
#
# Diferentemente de uma incerteza clássica, onde o sistema "já está em um estado,
# mas desconhecemos qual", aqui o sistema não possui um valor definido antes da
# medição. A medição projeta o sistema em um dos dois estados possíveis, de forma
# probabilística.
    
qc.h(0)


# Aplica a sequência de operações unitários no espaço de Hilbert para implementar
# reversivelmente um Half Adder quântico:
#
#   |0,0,B,A⟩
#       ↓
#   |0,A,B,A⟩
#       ↓
#   |0,A⊕B,B,A⟩
#       ↓
#   |A⋅B,A⊕B,B,A⟩


# 1. Aplica a operação CNOT(A → SUM):
#
# Matematicamente:
#
#   |SUM,A⟩ → |SUM⊕A,A⟩
#
# Como inicialmente SUM = |0⟩, então:
#
#   SUM = 0⊕A = A ⇒
#   SUM = A
#
# Após esta etapa, o estado fica:
#
#   |0,0,B,A⟩ → |0,A,B,A⟩
    
qc.cx(0, 2) 


# 2. Aplica a operação CNOT(B → SUM):
#
# Matematicamente:
#
#   |SUM,B⟩ → |SUM⊕B,B⟩
#
# Como SUM = A, então:
#
#   SUM = A⊕B
#
# Após esta etapa, o estado fica:
#
#   |0,A,B,A⟩ → |0,A⊕B,B,A⟩
#
# O qubit SUM agora contém a soma binária sem carry (ver colunas 1, 2 e 3 da tabela 
# verdade acima).
    
qc.cx(1, 2)


# 3. Aplica a operação CCX(A,B → CARRY):
#
# Matematicamente:
# 
#   |C,B,A⟩ → |C⊕(A⋅B),B,A⟩
#
# Como CARRY = |0⟩, então:
#
#   CARRY = A⋅B
#
# Após esta etapa, o estado fica:
#
#   |0,A⊕B,B,A⟩ → |A⋅B,A⊕B,B,A⟩
#
# O qubit CARRY agora contém o "vai um" resultante da operação A⋅B. Neste caso,
# CARRY será |1⟩ somente quando A = |1⟩ e B = |1⟩.
    
qc.ccx(0, 1, 3)


# =============================================================================
# Medição dos qubits (Colapso da função de onda)
# =============================================================================


# A medição quântica é destrutiva e probabilística. A medição dos qubits A, B,
# SUM e CARRY projeta o sistema em um dos dois ramos correlacionados da superposição.

qc.measure(0, 0)  # Mede A. Isso força o sistema a escolher o Ramo 1 ou Ramo 2.
qc.measure(1, 1)  # Mede B. Lê o valor que foi fixado pelo colapso de A.
qc.measure(2, 2)  # Mede SUM. Lê o valor que foi fixado pelo colapso de A. 
qc.measure(3, 3)  # Mede CARRY. Lê o valor que foi fixado pelo colapso de A.


# =============================================================================
# Impressão do estado do sistema quântico no prompt
# =============================================================================


# Lê a matriz unitária.

U = Operator(qc.remove_final_measurements(inplace=False))

# Lê o vetor de estados.

state = Statevector.from_instruction(qc.remove_final_measurements(inplace=False))

# Lê o estado do sistema.

sim = AerSimulator()
result = sim.run(qc, shots=1000).result()
counts = result.get_counts()

# Lê os bits A, B, SUM e CARRY.

bitstring = list(counts.keys())[0]
A = int(bitstring[3])
B = int(bitstring[2])
SUM = int(bitstring[1])
CARRY = int(bitstring[0])

# Define uma linha horizontal.

line = "\n=========================================================================\n"


# Limpa o prompt de comandos antes de imprimir.

os.system('cls' if os.name == 'nt' else 'clear')


# Imprime o título do circuito.

print("\n                         HALF ADDER QUÂNTICO\n")
print(line)


# Imprime o diagrama do circuito (caracteres Unicode).

print("DIAGRAMA DE CIRCUITO QUÂNTICO:\n\n")
print(qc.draw())
print(line)


# Imprime a matriz unitária.

print("MATRIZ UNITÁRIA:\n\n")
print(U.data)
print(line)


# Imprime o vetor de estados.

print("STATE VECTOR:\n\n")
print(state)
print(line)


# Imprime as estatísticas do circuito.

print("ESTATÍSTICAS:\n\n")
print("Número de portas:", qc.size())
print("Profundidade:", qc.depth())
print("Contagem de portas:", qc.count_ops())
print(line)


# Imprime o resultado bruto.

print("RESULTADO BRUTO:\n\n")
print(counts)
print(line)


# Imprime o resultado das portas.

print("RESULTADO INTERPRETADO:\n\n")
print("A     :", A)
print("B     :", B)
print("SUM   :", SUM)
print("CARRY :", CARRY)
print(line)


# =============================================================================
# GERAÇÃO E EXIBIÇÃO DOS GRÁFICOS DO CIRCUITO
# =============================================================================


# Janela 1: Diagrama de Circuito Quântico

fig_circuit = plt.figure(figsize=(8, 5))
ax_circ = fig_circuit.add_subplot(111)
qc.draw(output='mpl', ax=ax_circ)
ax_circ.set_title("Diagrama de Circuito Quântico")
plt.tight_layout()


# Janela 2: Histograma dos ramos 1 e 2 após as 1000 medições.

fig_hist = plt.figure(figsize=(7, 5))
ax_hist = fig_hist.add_subplot(111)
counts_dirac = {f"|{string}⟩": valor for string, valor in counts.items()}
plot_histogram(counts_dirac, ax=ax_hist)
ax_hist.set_title("Resultados da Simulação")
plt.tight_layout()


# Janela 3: Esferas de Bloch Individuais para cada um dos 4 qubits.

fig_bloch = plot_bloch_multivector(state, title="Esferas de Bloch (Estado dos Qubits)")


# Janela 4: Q-Sphere para visualizar as amplitudes e fases quânticas globais.

fig_qsphere = plot_state_qsphere(state)


# Janela 5: State City para mapear tridimensionalmente a Matriz de Densidade.

fig_city = plot_state_city(state, title="State City (Matriz de Densidade)", figsize=(10, 6))

states = ["0110", "1011"]

for ax in fig_city.get_axes():
    ticks_x = ax.get_xticklabels()
    labels_x = []
    for tick in ticks_x:
        txt = tick.get_text()
        if txt in states:
            labels_x.append(f"|{txt}⟩")
        else:
            labels_x.append(f"|{txt}⟩" if txt else "")
    ax.set_xticklabels(labels_x)
    
    for tick in ax.get_xticklabels():
        if tick.get_text() in [f"|{e}⟩" for e in states]:
            tick.set_color("red")
            tick.set_weight("bold")

    ticks_y = ax.get_yticklabels()
    labels_y = []
    for tick in ticks_y:
        txt = tick.get_text()
        if txt in states:
            labels_y.append(f"|{txt}⟩")
        else:
            labels_y.append(f"|{txt}⟩" if txt else "")
    ax.set_yticklabels(labels_y)
    
    for tick in ax.get_yticklabels():
        if tick.get_text() in [f"|{e}⟩" for e in states]:
            tick.set_color("red")
            tick.set_weight("bold")


# Renderiza simultaneamente todas as figuras geradas na tela.

plt.show()
