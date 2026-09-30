"""
===============================================================================

 CIRCUITO HALF ADDER QUÂNTICO EM QISKIT


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


 Como o programa é implementado com Qiskit, que usa notação little-endian |q₃q₂q₁q₀⟩,
 será utilizada esta convenção na notação de Dirac (Bra-Ket). Dessa forma, a ordem
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

 Um sistema quântico pode estar em um desses estados ou pode existir em uma 
 superposição de vários estados ou todos ao mesmo tempo. Este é o ponto chave para
 entender o circuito quântico implementado neste código-fonte.

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
 é uma combinação desses dois estados ao mesmo tempo (cara e coroa).

 Em computação quântica, a superposição é uma propriedade essencial dos qubits.
 Enquanto um bit clássico pode assumir apenas os valores 0 ou 1, um qubit pode
 existir em uma combinação dos estados 0 e 1 ao mesmo tempo. Isso permite que um
 sistema quântico represente simultaneamente diversas possibilidades, constituindo
 a base para algoritmos quânticos capazes de explorar espaços de solução de forma
 mais eficiente do que algoritmos clássicos em determinados tipos de problemas.

 Em termos matemáticos, o principio da superposição quântica diz que a combinação
 linear de dois ou mais vetores de estados no mesmo espaço de Hilbert, também é um
 estado do sistema. Para entender isso, considere um sistema com um único qubit.
 Nele, os estados são representados pelos vetores:


   |0⟩
   |1⟩


 onde:


         ┌ ┐            ┌ ┐
         │1│            │0│
   |0⟩ = │ │      |1⟩ = │ │
         │0│            │1│
         └ ┘            └ ┘


 Os vetores |0⟩ e |1⟩ formam a base computacional no espaço de Hilbert ℋ = ℂ².
 
 A superposição dos vetores |0⟩ e |1⟩ é representada na notação de Dirac por:


   |ψ⟩ = α|0⟩ + β|1⟩


 onde |ψ⟩ (Ket) representa um estado quântico, α e β são números complexos que
 representam as amplitudes de probabilidades para cada estado (são coeficientes 
 complexos do vetor de estado que indicam "quanto" de cada estado base existe na
 decomposição).
 
 Pode-se representar o Ket também na forma vetorial, denominada de state vector:
 
 
         ┌ ┐
         │α│
   |ψ⟩ = │ │
         │β│
         └ ┘


 State vector é o vetor que contém as amplitudes de probabilidade de todos os 
 estados possíveis da base computacional, permitindo descrever completamente seu
 estado quântico. Este conceito é importante, pois estaremos utilizando este modo
 de representação no simulador Qiskit Aer.

 Medindo o qubit, ele vai assumir o estado |0⟩ ou |1⟩. Pela regra de Born, as
 probabilidades de medir |0⟩ ou |1⟩ são calculadas, respectivamente, como:


   P(0) = ∣α∣²

   P(1) = ∣β∣²


 Como a soma das probabilidades de todos os resultados possíveis deve ser 1, então:


   |α|² + |β|² = 1


 é a condição de normalização de um qubit. Significa que a soma das probabilidades
 de todos os resultados possíveis deve ser 100%.

 Por exemplo, considere:

         _
   α = (√3/2)

   β = (1/2)


 então:

            _
   |α|² = (√3/2)² = 3/4

   |β|² = (1/2)² = 1/4


 Logo:


   3/4 + 1/4 = 1


 Isso significa que neste sistema:


   > Há 75% de probabilidade de medir |0⟩ (|α|² = 3/4).


   > Há 25% de probabilidade de medir |1⟩ (|β|² = 1/4).


   > Somando 75% de probabilidade de medir |0⟩ e 25% de probabilidade de medir |1⟩,
     obtém-se 100%, o que condiz com a condição de normalização imposta.
 

 Representando esta superposição na notação de Dirac, temos:
 
          _
   |ψ⟩ = √3/2|0⟩ + 1/2|1⟩


 e no state vector:
 
 
         ┌ _  ┐
         │√3/2│
   |ψ⟩ = │    │
         │ 1/2│
         └    ┘


 Ampliando agora o espaço de Hilbert para quatro qubits, temos que, se cada qubit 
 individual i possui um espaço de Hilbert ℋᵢ = ℂ², o sistema combinado de 4 qubits
 é o produto tensorial desses quatro espaços:


   ℋₜ = ℋ₁ ⊗ ℋ₂ ⊗ ℋ₃ ⊗ ℋ₄ = ℂ² ⊗ ℂ² ⊗ ℂ² ⊗ ℂ² = ℂ¹⁶


 O produto tensorial de quatro qubits combina os estados individuais de cada qubit, 
 formando um único espaço de Hilbert de dimensão 2⁴ = 16. Assim, a base computacional
 do sistema de quatro qubits é dada por:
 
 
   |0⟩ ⊗ |0⟩ ⊗ |0⟩ ⊗ |0⟩ = |0000⟩
   |0⟩ ⊗ |0⟩ ⊗ |0⟩ ⊗ |1⟩ = |0001⟩
   |0⟩ ⊗ |0⟩ ⊗ |1⟩ ⊗ |0⟩ = |0010⟩
   |0⟩ ⊗ |0⟩ ⊗ |1⟩ ⊗ |1⟩ = |0011⟩
   |0⟩ ⊗ |1⟩ ⊗ |0⟩ ⊗ |0⟩ = |0100⟩
   |0⟩ ⊗ |1⟩ ⊗ |0⟩ ⊗ |1⟩ = |0101⟩
   |0⟩ ⊗ |1⟩ ⊗ |1⟩ ⊗ |0⟩ = |0110⟩
   |0⟩ ⊗ |1⟩ ⊗ |1⟩ ⊗ |1⟩ = |0111⟩
   |1⟩ ⊗ |0⟩ ⊗ |0⟩ ⊗ |0⟩ = |1000⟩
   |1⟩ ⊗ |0⟩ ⊗ |0⟩ ⊗ |1⟩ = |1001⟩
   |1⟩ ⊗ |0⟩ ⊗ |1⟩ ⊗ |0⟩ = |1010⟩
   |1⟩ ⊗ |0⟩ ⊗ |1⟩ ⊗ |1⟩ = |1011⟩
   |1⟩ ⊗ |1⟩ ⊗ |0⟩ ⊗ |0⟩ = |1100⟩
   |1⟩ ⊗ |1⟩ ⊗ |0⟩ ⊗ |1⟩ = |1101⟩
   |1⟩ ⊗ |1⟩ ⊗ |1⟩ ⊗ |0⟩ = |1110⟩
   |1⟩ ⊗ |1⟩ ⊗ |1⟩ ⊗ |1⟩ = |1111⟩
   
   
 Onde:
 
 
            ┌ ┐               ┌ ┐               ┌ ┐               ┌ ┐ 
            │1│               │0│               │0│               │0│ 
            │0│               │1│               │0│               │0│ 
            │0│               │0│               │1│               │0│ 
            │0│               │0│               │0│               │1│ 
            │0│               │0│               │0│               │0│ 
            │0│               │0│               │0│               │0│ 
            │0│               │0│               │0│               │0│ 
            │0│               │0│               │0│               │0│ 
   |0000⟩ = │0│      |0001⟩ = │0│      |0010⟩ = │0│      |0011⟩ = │0│ 
            │0│               │0│               │0│               │0│ 
            │0│               │0│               │0│               │0│ 
            │0│               │0│               │0│               │0│ 
            │0│               │0│               │0│               │0│ 
            │0│               │0│               │0│               │0│ 
            │0│               │0│               │0│               │0│ 
            │0│               │0│               │0│               │0│ 
            └ ┘               └ ┘               └ ┘               └ ┘ 
 
            ┌ ┐               ┌ ┐               ┌ ┐               ┌ ┐
            │0│               │0│               │0│               │0│
            │0│               │0│               │0│               │0│
            │0│               │0│               │0│               │0│
            │0│               │0│               │0│               │0│
            │1│               │0│               │0│               │0│
            │0│               │1│               │0│               │0│
            │0│               │0│               │1│               │0│
            │0│               │0│               │0│               │1│
   |0100⟩ = │0│      |0101⟩ = │0│      |0110⟩ = │0│      |0111⟩ = │0│
            │0│               │0│               │0│               │0│
            │0│               │0│               │0│               │0│
            │0│               │0│               │0│               │0│
            │0│               │0│               │0│               │0│
            │0│               │0│               │0│               │0│
            │0│               │0│               │0│               │0│
            │0│               │0│               │0│               │0│
            └ ┘               └ ┘               └ ┘               └ ┘

            ┌ ┐               ┌ ┐               ┌ ┐               ┌ ┐ 
            │0│               │0│               │0│               │0│ 
            │0│               │0│               │0│               │0│ 
            │0│               │0│               │0│               │0│ 
            │0│               │0│               │0│               │0│ 
            │0│               │0│               │0│               │0│ 
            │0│               │0│               │0│               │0│ 
            │0│               │0│               │0│               │0│ 
            │0│               │0│               │0│               │0│ 
   |1000⟩ = │1│      |1001⟩ = │0│      |1010⟩ = │0│      |1011⟩ = │0│ 
            │0│               │1│               │0│               │0│ 
            │0│               │0│               │1│               │0│ 
            │0│               │0│               │0│               │1│ 
            │0│               │0│               │0│               │0│ 
            │0│               │0│               │0│               │0│ 
            │0│               │0│               │0│               │0│ 
            │0│               │0│               │0│               │0│ 
            └ ┘               └ ┘               └ ┘               └ ┘ 
  
            ┌ ┐               ┌ ┐               ┌ ┐               ┌ ┐
            │0│               │0│               │0│               │0│
            │0│               │0│               │0│               │0│
            │0│               │0│               │0│               │0│
            │0│               │0│               │0│               │0│
            │0│               │0│               │0│               │0│
            │0│               │0│               │0│               │0│
            │0│               │0│               │0│               │0│
            │0│               │0│               │0│               │0│
   |1100⟩ = │0│      |1101⟩ = │0│      |1110⟩ = │0│      |1111⟩ = │0│
            │0│               │0│               │0│               │0│
            │0│               │0│               │0│               │0│
            │0│               │0│               │0│               │0│
            │1│               │0│               │0│               │0│
            │0│               │1│               │0│               │0│
            │0│               │0│               │1│               │0│
            │0│               │0│               │0│               │1│
            └ ┘               └ ┘               └ ┘               └ ┘  


 Representando a superposição destes estados na notação de Dirac:
 
 
   |ψ⟩ = α₀|0000⟩ +  α₁|0001⟩ +  α₂|0010⟩ +  α₃|0011⟩ +  
         α₄|0100⟩ +  α₅|0101⟩ +  α₆|0110⟩ +  α₇|0111⟩ + 
         α₈|1000⟩ +  α₉|1001⟩ + α₁₀|1010⟩ + α₁₁|1011⟩ +
        α₁₂|1100⟩ + α₁₃|1101⟩ + α₁₄|1110⟩ + α₁₅|1111⟩
         
         
 e no state vector:
 
 
         ┌   ┐
         │ α₀│
         │ α₁│
         │ α₂│
         │ α₃│
         │ α₄│
         │ α₅│
         │ α₆│
         │ α₇│
   |ψ⟩ = │ α₈│
         │ α₉│
         │α₁₀│
         │α₁₁│
         │α₁₂│
         │α₁₃│
         │α₁₄│
         │α₁₅│
         └   ┘
 
 
 Como regra geral, para um espaço de Hilbert de n qubits:


             ⊗n
   ℋₙ = (ℂ²)


 A dimensão deste espaço (número de estados da base computacional) é calculada
 como:


   dim(ℋₙ) = 2ⁿ

 
 Esta equação estabelece uma relação direta entre um computador quântico e um 
 computador clássico, desta forma:
 
   
   Número de bits clássicos = 2ⁿ × m
   
 
 Onde:
 
 
   n: Número de qubits.
   
   
   m: Número de bits em ponto flutuante para representar a amplitude de probabilidade
   de cada estado da base computacional. No Qiskit, utilizando state vector de 
   precisão dupla (complex128), a representação padrão de uma amplitute é:
   
     > Parte real: 64 bits.
     
     > Parte imaginária: 64 bits.
     
   No total, cada amplitude utiliza 128 bits (16 bytes) para ser representada.
 
 
 Isso implica que para emular n qubits, será necessário um computador clássico 
 com 2ⁿ × m bits, somente para representar as amplitudes de probabilidades de todos
 os estados. Em decorrência disso, podemos simular circuitos com relativamente
 poucos qubits usando um computador clássico com Qiskit ou outro ambiente para 
 simulação que utilize state vector, pois conforme adicionamos mais qubits, vai 
 se esgotando rapidamente toda a memória para representá-los. 
 
 Num computador com 32 Gigabytes livres de memória RAM, por exemplo, consegue-se
 simular 31 qubits apenas usando o Qiskit com state vector de precisão dupla 
 (complex128):
 
 
   2ⁿ × m ⇒
 
   2³¹ × 128 = 2³¹ × 2⁷ = 2³⁸ bits ⇒
    
   2³⁸ / 2³  = 2³⁵ bytes ⇒
    
   2³⁵ / 2³⁰ = 2⁵ Gigabytes ⇒ 32 Gigabytes
    
 
 State vector armazena todas as 2ⁿ amplitudes na memória. Por isso o esgotamento 
 rápido dos recursos à medida que representamos mais qubits. Outros métodos de 
 representar as amplitudes como Tensor Network, Matrix Product State (MPS),
 Stabilizer State podem ocupar menos memória, portanto, permitem a representação
 de mais (às vezes muito mais) qubits com a mesma quantidade de memória. Mas nestes
 casos, isso dependerá muito das características do circuito representado. Mesmo
 os mais potentes supercomputadores da atualidade não conseguem representar mais
 do que 48 qubits em representação state vector de precisão dupla.

 Na tabela abaixo, calculei alguns valores de dim(ℋₙ) apenas para demonstração de
 como se dá este crescimento exponencial do número de estados da base computacional 
 conforme se aumenta o número de qubits no sistema:


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
 de 1 × 10⁸⁰. Isso significa que se cada átomo pudesse ser transformado num bit
 clássico, ainda assim seriam necessários 4,18 x 10⁷² universos iguais ao nosso
 para construir um computador clássico que simulasse estes 500 qubits.
 
 Com base nestes números, é muito fácil entender como o computador Sycamore do
 Google conseguiu alcançar a suplemacia quântica em 2019. O termo suplemacia quântica
 (quantum supremacy) foi cunhado pelo físico teórico John Preskill, do Caltech,
 em 2012, no trabalho Quantum Computing and the Entanglement Frontier. Este termo
 se refere a demonstrar que um computador quântico consegue realizar uma tarefa
 computacional qualquer que um computador clássico não consegue realizar de forma
 viável.
 
 A tarefa escolhida para o Sycamore foi Random Circuit Sampling (RCS) - amostrar 
 os resultados de um circuito quântico pseudoaleatório. Não era um algoritmo de 
 aplicação prática e sim um benchmark destinado a tornar evidente a diferença entre
 computação quântica e computação clássica. O computador do Google tinha 54 qubits,
 porém um dos qubits apresentou defeito, e ele realizou o processamento com apenas
 53 qubits. Conclui a tarefa em 200 segundos. Um supercomputador da época, usando
 métodos clássicos conhecidos, exigiria cerca de 10.000 anos para concluir esta
 mesma tarefa.

 É importante não confundir dimensão com quantidade de estados quânticos possíveis.

 Quando escrevemos:


   dim(ℋ₄) = 16


 significa que o espaço de Hilbert de 4 qubits possui 16 vetores de base computacional.
 Mas estes estados são apenas os "eixos" do espaço vetorial ℂ¹⁶.

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
     ▲
     │           (3,3)
   3 │          ◌ 
     │                      
   2 │
     │(0,1)
   1 ●
     │   (1, 0)
   0 └──●───────────▶ x
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
 
 Representando o circuito Half Adder em um Diagrama de Circuito Quântico:


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
	

 Neste circuito de exemplo, inicialmente A está em superposição (A = α∣0⟩ + β∣1⟩),
 B = |1⟩, SUM = |0⟩ e CARRY = |0⟩. Quando são aplicadas as portas CNOT e CCX na 
 sequência de operações do circuito, o estado do sistema passa a ser uma superposição 
 de dois estados:


   ∣ψ⟩ = α∣0110⟩ + β∣1011⟩
 

 Os dois ramos da superposição têm origem na superposição inicial do qubit A, 
 enquanto as portas CNOT e CCX propagam essa estrutura para os demais qubits, 
 gerando correlações quânticas, incluindo o emaranhamento entre A, SUM e CARRY. 
 Dessa forma, cada componente evolui de maneira consistente sob a mesma
 transformação unitária. B influencia o estado global, porém está desacoplado (não
 emaranhado). Ele atua como um qubit clássico controlador fixo no circuito.

 Emaranhamento quântico, ou entrelaçamento quântico, é um fenômeno em que dois ou
 mais sistemas quânticos passam a ser descritos por um único estado quântico conjunto,
 de modo que não é possível descrever completamente cada sistema de forma independente.
 Em termos matemáticos, um estado emaranhado não pode ser escrito como o produto dos
 estados individuais dos subsistemas.
 
 Em computação quântica é o princípio que permite que um circuito quântico produza
 e manipule correlações quânticas entre vários qubits. Por exemplo, considere o
 estado de Bell:

             _
   ∣Φ⁺⟩ = 1/√2 (|00⟩ + ∣11⟩)


 Como um estado de Bell é um estado quântico de dois qubits maximamente emaranhados,
 se medirmos o primeiro qubit e o resultado for 0, o segundo qubit também será 0.
 Se o resultado for 1, o segundo também será 1. No caso, as medições estarão
 correlacionadas.

 Usando uma analogia, imagine duas caixas fechadas contendo cartões. Você sabe 
 apenas que existem duas possibilidades: ou as duas caixas contêm um cartão azul
 cada uma, ou um cartão vermelho, mas você não sabe qual das duas situações ocorrerá. 
 Ao abrir a primeira caixa, se encontrar o cartão azul, sabe imediatamente que
 da outra também é azul. Se encontrar o cartão vermelho, sabe que da outra é vermelho.
 Muito a grosso modo, emaranhamento é isto. Ele estabelece uma correlação entre
 as partículas emaranhadas. Mas esta correlação não pode ser explicada por simples
 "cartões escondidos" previamente determinados, como nesse exemplo, conforme veremos
 adiante com os testes das desigualdades de Bell.

 Quando as portas CNOT e Toffoli emaranharem A, SUM e CARRY na sequência de operações
 do circuito de exemplo citado acima, estes qubits passarão a formar um "único
 sistema". Ler 1 em A, acarreta que SUM seja 0 e CARRY seja 1. Ler 0, que SUM seja
 1 e CARRY seja 0. Os resultados passam a guardar esta correlação.
 		                                       _
 Para o caso de superposição uniforme ∣A⟩ = 1/√2 (∣0⟩ + ∣1⟩), o estado final torna-se:

            _
   ∣ψ⟩ = 1/√2 (|0110⟩ + ∣1011⟩)


 Isso implica que, ao realizar uma medição, o sistema colapsa para |0110⟩ ou |1011⟩
 com probabilidade 50% para cada estado. Como não há um mecanismo de interferência
 neste circuito de exemplo, projetado para amplificar um resultado específico, as 
 amplitudes permanecem balanceadas conforme a evolução linear do circuito.
 
 Um detalhe interessante sobre o emaranhamento quântico é que você pode separar
 cada um dos sistemas quânticos emaranhados a longas distâncias e eles continuarão
 a se comportar como um único sistema. Esta propriedade foi chamada pejorativamente
 por Albert Einstein de ação fantasmagórica à distância (em alemão spukhafte
 Fernwirkung), pois ele acreditava que nada no universo, nem matéria, nem energia, 
 nem informação poderia viajar mais rápido do que a velocidade da luz no vácuo,
 e esta é a base da Teoria da Relatividade Especial, um princípio chamado localidade.
 
 No emaranhamento, no entanto, duas partículas ficam conectadas de tal forma que
 o estado de uma depende instantaneamente do estado da outra. Se você separar essas
 duas partículas, mantendo uma na Terra e enviando a outra para a estrela mais
 próxima (a 4 anos-luz de distância), por exemplo, ao medir a partícula na Terra
 e ver que ela virou o "Polo Norte", a partícula na estrela instantaneamente vira
 o "Polo Sul". Para Einstein, isso violava a sua teoria, pois a "informação" da
 medição teria de ter viajado a uma velocidade infinita, parecendo pura bruxaria
 ou telepatia. Daí o uso pejorativo do termo ação fanstasmagórica à distância.
 
 Einstein achava que as partículas já carregavam instruções secretas desde o momento
 em que foram criadas, as chamadas "variáveis ocultas locais" (hidden variables),
 como no exemplo dos cartões nas caixas que citei acima. Se você abre uma caixa 
 e vê o cartão vermelho, já sabe que a outra caixa também tem o cartão vermelho. Se
 vê azul, sabe que na outra tem azul. Não há nenhum cartão "conversado" magicamente
 com o outro à distância. Seus estados já estavam definidos deste o começo.
 
 Décadas mais tarde, experimentos bastante rigorosos provaram que Einstein estava
 errado:
 
 
   1935 — Einstein, Boris Podolsky e Nathan Rosen publicam o famoso argumento EPR,
   questionando se a mecânica quântica fornecia uma descrição completa da realidade
   física. A questão envolvia, entre outras coisas, a possibilidade de que partículas 
   possuíssem propriedades bem definidas que não eram completamente descritas pela
   mecânica quântica, ideia que posteriormente seria associada às variáveis ocultas.


   1964 — John Bell publica seu trabalho sobre as desigualdades de Bell. O avanço
   fundamental foi transformar a discussão filosófica do argumento EPR em uma questão 
   experimentalmente testável. Bell mostrou que qualquer teoria de variáveis ocultas 
   locais satisfaz determinadas desigualdades, enquanto a mecânica quântica prevê
   violações dessas desigualdades.

   
   1972 — Stuart Freedman e John F. Clauser realizaram um dos primeiros testes 
   experimentais importantes da desigualdade de Bell. Eles produziram pares de 
   fótons emaranhados e mediram suas polarizações usando filtros. O resultado
   mostrou uma violação da desigualdade de Bell, em concordância com a mecânica
   quântica. Esse experimento foi muito importante, mas ainda existiam limitações
   experimentais, os chamados loopholes (lacunas).
   
   
   1981–1982 — Alain Aspect e seus colaboradores realizaram uma sequência de
   experimentos que aprimorou significativamente os testes anteriores. O experimento
   mais famoso foi publicado em 1982. Os pesquisadores conseguiram mudar rapidamente
   as configurações dos analisadores enquanto os fótons já estavam em trânsito.
   Isso era importante porque a teoria de variáveis ocultas locais poderia tentar 
   explicar as correlações supondo que as partículas já "soubessem" antecipadamente
   quais configurações seriam utilizadas. No experimento, a configuração do aparelho
   podia mudar depois que os fótons haviam deixado a fonte. O resultado novamente
   violou a desigualdade de Bell.
   
   
   1990–2000 — Nas décadas seguintes, diversos grupos fizeram experimentos cada
   vez mais precisos com partículas entrelaçadas. O objetivo não era simplesmente
   repetir Bell, mas fechar diferentes loopholes que poderiam, em princípio, deixar
   uma explicação alternativa para os resultados. Anton Zeilinger e colaboradores 
   tiveram um papel importante nessa fase, incluindo experimentos com fótons 
   entrelaçados e configurações de medição escolhidas aleatoriamente.
   
   
   2015 — Diferentes grupos conseguiram realizar testes de Bell que fecharam
   simultaneamente as principais lacunas experimentais de localidade e detecção,
   usando diferentes plataformas experimentais (loophole-free). Esse tipo de 
   experimento tornou muito mais difícil explicar a violação da desigualdade de
   Bell observada por meio de falhas experimentais convencionais.
 
 
 Por estes experimentos, os pesquisadores Alain Aspect, John F. Clauser e Anton
 Zeilinger dividiram o Prêmio Nobel de física de 2022.
 
 O que os experimentos provaram é que não existem variáveis ocultas locais (eles
 não excluem a possibilidade de que existam variáveis ocultas não locais, mas 
 esta já é uma outra questão). Se não existem variáveis ocultas locais, significa
 que o universo é fundamentalmente não-local e que o resultado de uma medição
 quântica não estava determinado antes de acontecer. O termo não-local significa 
 que um evento que acontece num determinado ponto do universo pode influenciar 
 instantaneamente noutro ponto, sem que nenhuma matéria, energia ou informação 
 viaje pelo espaço entre eles. 
 
 Ainda não existem meios de medir algo que acontece instantaneamente, mas a velocidade
 mínima da "ação fantasmagórica à distância" foi medida em 2013 pela equipe de 
 Juan Yin na Universidade de Ciência e Tecnologia da China em mais de 100.000 vezes
 a velocidade da luz.
 
 
 DECOERÊNCIA
 
 
 Neste projeto não será simulado decoerência por uma questão de simplificação 
 do código. Isso seria possível usando o módulo qiskit_aer.noise. 
 
 A decoerência é o processo pelo qual um sistema quântico perde coerência de fase 
 devido à interação indesejada e inevitável com o ambiente externo (ruído térmico, 
 campos magnéticos, etc.), fazendo com que seu comportamento efetivo se aproxime
 do comportamento clássico. É por este motivo que os computadores quânticos atuais
 tem mecanismos para geração de temperaturas criogênicas, afim de evitar ruído 
 térmico, e funcionam em salas isoladas para tentar evitar os outros tipos de ruídos.

 Quando ocorre a decoerência, há:
 
 
   1. Perda de Fase (Dephasing): O ambiente atua como uma medição constante e 
   indesejada, destruindo a relação de fase sutil entre as amplitudes complexas
   (os αi do espaço de Hilbert).
                                                       _    
   2. Transição de Estado: O estado de superposição 1/√2 (∣0⟩ + ∣1⟩) colapsa para 
   uma mistura puramente clássica (ou é |0⟩, ou é |1⟩, sem propriedades de 
   interferência).
   
   3. Dissipação de Energia (Relaxamento): Além da perda de fase, a decoerência 
   frequentemente caminha junto com o relaxamento térmico. O sistema quântico 
   troca energia com o ambiente até atingir o equilíbrio. Para um qubit, isso 
   geralmente significa decair de um estado de maior energia (|1⟩) de volta para 
   o estado fundamental (|0⟩).
 
 
 Em um hardware real afetado por ruído, como o IBMQ, por exemplo, o resultado 
 final medido diverge das probabilidades ideais calculadas por este programa,
 logo, aqui estamos simulando um sistema ideal.
 
 
 ALGORITMO DE GROVER
 
 
 O circuito Half Adder do exemplo acima tem um comportamento probabilístico. Se 
 ele for executado, em aproximadamente 50% das vezes ele colapsará no estado |0110⟩
 e em aproximadamente 50% das vezes ∣1011⟩, pois estará em superposição uniforme
 destes dois estados:
 
            _
   ∣ψ⟩ = 1/√2 (|0110⟩ + ∣1011⟩)


 Para que ele se torne um circuito prático, é necessário selecionar qual ramo é
 de interesse. Vou implementar neste programa a soma de A = |0⟩ e B = |1⟩, que
 fará o circuito colapsar no estado |0110⟩. Para isso, eu optei por filtrar os
 estados de entrada usando o algoritmo de Grover.
 
 Este algoritmo foi proposto por Lov K. Grover, pesquisador indiano-americano do 
 Bell Labs, em 1996. O artigo original foi publicado com o título: A fast quantum
 mechanical algorithm for database search. Como o título indica, ele foi criado
 para realizar a busca em banco de dados não estruturados. O algoritmo utiliza
 propriedades da mecânica quântica para reduzir a complexidade de uma busca não 
 estruturada _ de O(N), e que requer em média N/2 consultas em um sistema clássico,
 para     O(√N) consultas com o algoritmo de Grover.
 
 Para o circuito deste projeto  _ que tem uma única solução, o número aproximado 
 de iterações quânticas é  π/4(√N), resultando em um speedup assintótico quadrático
 (quadratic asymptotic speedup) em relação à busca clássica. Ou seja, o tamanho 
 do problema cresce quadraticamente em relação ao número de operações quânticas.
 
 Suponha: 
 
 
   N = 1.000.000
 
 
 Uma busca clássica, em média, precisaria de aproximadamente:
 
 
   N/2 = 500.000
 
 
 consultas para encontrar a solução.
 
 Com o algoritmo de Grover precisaria de aproximadamente:
 
        _
   π/4(√N) ⇒
        ________
   π/4(√1000.000) ⇒
   
   π/4(1000) = ≈785


 consultas para encontrar a solução.

 Comparando com a média de uma busca clássica:
 
 
   (500.000 / 785) = ≈637


 Nesse exemplo, portanto, a quantidade média de consultas cai de aproximadamente
 500.000 para 785, uma redução de 637 vezes no número de passos na busca.
 
 O ponto mais importante é o comportamento quando N cresce:
 
             _
   O(N) → O(√N) 
 
 
 Conforme N cresce, o ganho com o algoritmo de Grover vai ficando maior. Por exemplo,
 para N = 1.000.000.000:
 
        _
   π/4(√N) ⇒
        _____________
   π/4(√1.000.000.000) ⇒
             __
   π/4(10000√10) = ≈24.836
   
   
 Comparando com a média de passos de uma busca clássica (N/2):
 
 
   (500.000.000 / 24.836) = ≈20.132
 
 
 O speedup assintótico quadrático, portanto, descreve uma situação em que um algoritmo
 consegue resolver um problema de forma quadraticamente mais rápida do que outro
 à medida que o volume de dados cresce para infinito (N → ∞).
 
 Para o circuito Half Adder que tem apenas 4 estados de entrada, |00⟩, |01⟩, |10⟩
 e |11⟩, o número de buscas ficará:

        _
   π/4(√N) ⇒ 
        _
   π/4(√4) ⇒
   
   π/4(2) = ≈1
   
   
 Logo, não será necessário iterar sobre o conjunto, pois em um passo já se encontra
 a solução procurada.
 
 O algoritmo de Grover funciona da seguinte forma:
 
 
   1. Cria a superposição:
 
      Cria a superposição de todos os qubits a serem filtrados (exemplo: q₀ e q₁).


   2. Oráculo:
   
      O oráculo identifica o estado a ser buscado.
      
      Suponha que a solução procurada seja:
      
      
        ∣10⟩
        
        
      O oráculo deve realizar:
      
      
        ∣x⟩ → (−1)ᶠ⁽ˣ⁾∣x⟩
        
        
      ou seja:
      
      
        ∣10⟩ → −∣10⟩
        
        
      Todos os outros estados permanecem iguais:
      
      
        ∣x⟩ → ∣x⟩          ∀x, x ≠ 10

        
      O oráculo não aumenta a probabilidade do estado procurado, apenas muda a
      fase da amplitude.
      
      Logo, antes do oráculo, temos:
      
      
        ∣ψ⟩ = 1/2(|00⟩ + |01⟩ + |10⟩ + |11⟩)
        
        
      Depois:
      
      
                                Estado
                                Marcado
                                  ↓
        ∣ψ⟩ = 1/2(|00⟩ + |01⟩ + −|10⟩ + |11⟩)
        
     
   3. Operador de difusão:

      Depois do oráculo aplica-se o chamado operador de difusão (diffusion operator):


        D = 2∣s⟩⟨s∣ − I

        
      Esse operador pode ser interpretado como uma inversão em relação à média das
      amplitudes.
      
      Depois do oráculo, as fases de amplitudes dos estados ficarão como:
     
     
        |00⟩ ⇒  1/2
        |01⟩ ⇒  1/2
        |10⟩ ⇒ −1/2
        |11⟩ ⇒  1/2
     
     
      A média das amplitudes é calculada como:
     
     
        ((1/2 + 1/2 − 1/2 + 1/2) / 4) = 1/4
     
     
      A difusão pega cada amplitude i e faz:

     
        ảᵢ = 2ā - aᵢ
     
     
      onde ā é a média da amplitudes, que neste caso, é 0,25.
     
      Para o estado alvo |10⟩ a amplitude é:
     
     
        a = −1/2
     
     
      então:
     
     
        ả = 2(1/4) − (−1/2)
        ả = 1/2 + 1/2
        ả = 1
     
     
      Para os demais estados (|00⟩, |01⟩ e |11⟩), a amplitude é calculada como:
     
     
        ả = 2(1/4) − 1/2
        ả = 1/2 − 1/2
        ả = 0
     
     
      Logo, antes da difusão tínhamos estas amplitudes para cada estado:
     
     
        |00⟩ ⇒  1/2
        |01⟩ ⇒  1/2
        |10⟩ ⇒ −1/2
        |11⟩ ⇒  1/2
     
     
      Depois da difusão:
     
     
        |00⟩ ⇒ 0
        |01⟩ ⇒ 1
        |10⟩ ⇒ 0
        |11⟩ ⇒ 0
        
        
      Isso significa que tem próximo de 100% de probabilidade de 
        
      Para este problema com apenas 4 estados, calculamos o número de iterações
      como:
        
        
        π/4(√N) ⇒ 
             _
        π/4(√4) ⇒
   
        π/4(2) = ≈1
        
        
      Logo, com 1 iteração já encontra a solução.
      
      Para N estados, repete-se oráculo → difusão k vezes:
      
                 ___
        k ≈ π/4 √N/M
      
      
      Onde:
      
      
        N: número total de estados.
      
        M: número de estados que são soluções.
 
 
 O operador de difusão usa interferência destrutiva para os estados não desejados
 e interferência construtiva para o estado desejado, desta forma:
 
                 
                         Oráculo cria diferença de fase
                         
                                      ⇓
                     
                     Difusão faz as amplitudes interferirem
                                      
                                      ⇓
                   
                   Solução é reforçada, demais são canceladas
                   
   
 Interferência quântica é um fenômeno da mecânica quântica que surge da natureza 
 ondulatória de partículas quânticas como elétrons ou fótons. 
 
 Na física clássica, costumamos separar:


   > Partículas → objetos localizados, como uma pequena esfera;


   > Ondas → fenômenos distribuídos, como ondas na água ou ondas sonoras.


 Na mecânica quântica, essa separação deixa de funcionar completamente. Elétrons,
 fótons, átomos podem apresentar fenômenos característicos tanto de partículas 
 quanto de ondas.

 
 (continua...)
 
 


 INSTALAÇÃO DO QISKIT E QISKIT-AER NO PYTHON:

 
 Para testar este programa é necessário que se instale o SDK Qiskit junto com o
 Python. Instale o Python, depois abra o terminal do Windows (cmd) ou Linux e 
 digite:


   pip install qiskit

  
 Tecle ENTER e aguarde a instalação terminar.

 Abra novamente o terminal e digite:


   pip install qiskit-aer

  
 Tecle ENTER e aguarde a instalação terminar.

 Com isso, é instalado o SDK para programação para o computador quântico da IBM
 (IBMQ) e o simulador, para testar o código na máquina local.

 Para instalar os utilitários de visualização de gráficos, abra o terminal e 
 digite: 


   pip install "qiskit[visualization]" matplotlib pylatexenc
  
  
 Tecle ENTER e aguarde a instalação terminar.
 
 
 https://quantum.cloud.ibm.com/learning/pt/courses/basics-of-quantum-information
 
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
#
# IMPLEMENTAÇÃO DO CIRCUITO HALF ADDER QUÂNTICO COM 4 QUBITS:
#
# Cria um circuito quântico contendo 4 qubits e 4 registradores clássicos para
# leitura destes qubits.
#
# =============================================================================


qc = QuantumCircuit(4, 4)




# =============================================================================
#
# SUPERPOSIÇÃO INICIAL DE TODAS AS ENTRADAS:
#
#
# Ao aplicar a superposição em A e B, que inicialmente eram ∣00⟩, tem-se:
#
#
#   ∣00⟩ → 1/2(∣00⟩ + ∣01⟩ + ∣10⟩ + ∣11⟩)
#
#
# Os quatro estados entram em superposição uniforme, com amplitude de probabilidade
# 1/2 cada um.
#
# Pela regra de Born, a probabilidade de cada estado é calculada como:
#
#
#   |1/2|² = 1/4 = 25%
#
#
# Antes de aplicar o algoritmo de Grover, portanto, a amplitude de probabilidade
# de cada estado é a seguinte:
#
#
#   |00⟩ ⇒ 1/2
#   |01⟩ ⇒ 1/2
#   |10⟩ ⇒ 1/2
#   |11⟩ ⇒ 1/2
#
# =============================================================================


# Aplica a porta Hadamard no qubit 0 (entrada A), colocando-o em superposição.
#
# A porta Hadamard é descrita pela matriz 2×2:
#
#
#            ┌    ┐
#          _ │1  1│
#   H = 1/√2 │    │
#            │1 -1│
#            └    ┘
#
#
# Aplicando H ao vetor ∣0⟩, temos:
#
#
#               ┌    ┐ ┌ ┐          ┌ ┐
#             _ │1  1│ │1│        _ │1│
#   H∣0⟩ = 1/√2 │    │ │ │  =  1/√2 │ │
#               │1 -1│ │0│          │1│
#               └    ┘ └ ┘          └ ┘
#
#
# Na notação de Dirac:
#
#             
#          ∣0⟩ + ∣1⟩
#   H∣0⟩ = ────────
#             √2          
#
#
# Temos então uma superposição uniforme. 
#
# A amplitude de cada estado é:
#
#      _
#   1/√2
#
#
# Aplicando H ao vetor ∣1⟩, temos:
#
#
#               ┌    ┐ ┌ ┐          ┌  ┐
#             _ │1  1│ │0│        _ │ 1│
#   H∣1⟩ = 1/√2 │    │ │ │  =  1/√2 │  │ 
#               │1 -1│ │1│          │-1│
#               └    ┘ └ ┘          └  ┘
#
#
# Na notação de Dirac:
#
#
#          ∣0⟩ - ∣1⟩
#   H∣1⟩ = ────────
#             √2
#
# 
# O sinal é negativo. As probabilidades continuam sendo 50%/50%, mas a fase das
# amplitudes é diferente.

qc.h(0)

# Aplica a porta Hadamard no qubit 1 (entrada B), colocando-o em superposição.
  
qc.h(1)  




# =============================================================================
#
# ORÁCULO PARA MARCAR APENAS O ESTADO |10⟩:
#
# =============================================================================


# Inversão do qubit q0 (A).

qc.x(0)

# Aplica a fase controlada (CZ).

qc.cz(0, 1)

# Desfaz a inversão do qubit q0 (A).

qc.x(0)




# =============================================================================
#
# DIFUSÃO (OPERADOR DE GROVER PARA AMPLIFICAR O ESTADO ALV0 |01⟩):
#
#
# Essa sequência implementa:
#
#   D = 2∣s⟩⟨s∣ − I
#
# chamado de inversão sobre a média.
#
# Depois do oráculo, as amplitudes dos estados ficarão como:
#
#   |00⟩ ⇒ +1/2
#   |01⟩ ⇒ −1/2
#   |10⟩ ⇒ +1/2
#   |11⟩ ⇒ +1/2
#
# A média das amplitudes é calculada como:
#
#   ((0,5 − 0,5 + 0,5 + 0,5) / 4) = 1/4 ou 0,25
# 
# A difusão pega cada amplitude i e faz:
#
#   ảᵢ = 2ā - aᵢ
#
# onde ā é a média da amplitudes, que neste caso, é 0,25.
#
# Para o estado alvo |01⟩ a amplitude é:
#
#   a = −0,5
#
# então:
#
#   ả = 2(0,25) − (−0,5)
#   ả = 0,5 + 0,5
#   ả = 1
#
# Para os demais estados (|00⟩, |10⟩, |11⟩), a amplitude é calculada como:
#
#   ả = 2(0,25) − 0,5
#   ả = 0,5 − 0,5
#   ả = 0
#
# Logo, antes da difusão tínhamos estas amplitudes para cada estado:
#
#   |00⟩ ⇒ +1/2
#   |01⟩ ⇒ −1/2
#   |10⟩ ⇒ +1/2
#   |11⟩ ⇒ +1/2
#
# Depois da difusão:
#
#   |00⟩ ⇒ 0
#   |01⟩ ⇒ 1
#   |10⟩ ⇒ 0
#   |11⟩ ⇒ 0
#
# =============================================================================


# Aplica Hadamard no qubit 0 para a inversão sobre a média.

qc.h(0)

# Aplica Hadamard no qubit 1 para a inversão sobre a média.

qc.h(1)

# Aplica a porta X no qubit 0 para inverter o sinal lógico.  

qc.x(0)

# Aplica a porta X no qubit 1 para inverter o sinal lógico.  

qc.x(1)

# Aplica Hadamard no qubit 1.

qc.h(1)

# Aplica CNOT entre o qubit 0 e o qubit 1 para o espelhamento de fase. 

qc.cx(0, 1)

# Aplica Hadamard no qubit 1.

qc.h(1)

# Reverte a porta X no qubit 0. 

qc.x(0)

# Reverte a porta X no qubit 1.

qc.x(1)

# Aplica Hadamard final no qubit 0.

qc.h(0)

# Aplica Hadamard final no qubit 1.

qc.h(1)




# =============================================================================
#
# EXECUTA O CIRCUITO HALF ADDER SOBRE O ESTADO JÁ FILTRADO PELO ALGORITMO DE
# GROVER
# 
#
# Graças à interferência do Algoritmo de Grover, o sistema não está mais dividindo
# as probabilidades igualmente entre |00⟩, |01⟩, |10⟩ e |11⟩. O estado de entrada 
# A = |1⟩ e B = |0⟩ foi amplificado a ponto de ocupar quase 100% da probabilidade 
# do vetor de estados. Os outros estados ainda existem matematicamente na 
# superposição, mas com amplitudes de probabilidades próximas de 0%.
#
# Quando as portas lógicas do Half Adder atuam sobre as entradas, elas então 
# calculam sobre esta superposição. Como o estado |01⟩ domina quase totalmente 
# o vetor (amplitude próxima de 100%), o somador executa a operação para esse
# estado dominante: 0 + 1 = 1 (com carry 0). Como os qubits de saída SUM e CARRY
# foram conectados aos de entrada por portas CNOT e Toffoli, eles ficam emaranhados 
# com A e B, formando um único sistema. Como o estado predominante nas entradas
# é |01⟩, a saída gerada emaranhada a ele será |1⟩ para SUM e |0⟩ para o CARRY.
#
# =============================================================================


# Aplica a sequência de transformações unitárias no espaço de Hilbert para 
# implementar reversivelmente um Half Adder quântico:
#
#   |0,0,B,A⟩
#       ↓
#   |0,A,B,A⟩
#       ↓
#   |0,A⊕B,B,A⟩
#       ↓
#   |A⋅B,A⊕B,B,A⟩
#
# As operações realizadas são as seguintes:
#
#   1. CNOT(A → SUM)
#   2. CNOT(B → SUM)
#   3. CCX(A,B → CARRY)


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
# O qubit SUM agora contém a soma binária sem carry (ver colunas 1, 2 e 3 da 
# tabela verdade acima).

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
#
# EXTRAÇÃO DE DADOS MATEMÁTICOS DO CIRCUITO (STATEVECTOR e OPERATOR):
#
#
# Cria uma cópia temporária do circuito sem as medições para fins de análise 
# matemática e impressão no terminal.
#
# =============================================================================


qc_no_meas = qc.remove_final_measurements(inplace=False)

U = Operator(qc_no_meas)

state = Statevector.from_instruction(qc_no_meas) # Statevector(qc_no_meas)




# =============================================================================
#
# Medição do circuito (colapso da função de onda):
#
# A medição quântica é destrutiva e probabilística. A medição dos qubits A, B,
# SUM e CARRY projeta o sistema no estado correlacionado da superposição. Como
# o algoritmo de Grover fez com que a entrada |01⟩ ficasse com amplitude de quase
# 100%, então, o resultado esperado da medição será |0101⟩, descartando-se todos
# os demais ramos que não levavam a este resultado.
#
# =============================================================================


# Mede A.

qc.measure(0, 0) 

# Mede B.
 
qc.measure(1, 1)

# Mede SUM. Lê o valor que foi fixado pelo colapso de A.

qc.measure(2, 2) 

# Mede CARRY. Lê o valor que foi fixado pelo colapso de A.

qc.measure(3, 3)




# =============================================================================
#
# Execução da simulação com AerSimulator:
#
# =============================================================================


# Inicializa o simulador quântico do Qiskit.

simulator = AerSimulator(method="statevector")

# Executa o circuito 1000 vezes para coletar estatísticas de probabilidade.

result = simulator.run(qc, shots=1000).result()

# Extrai um dicionário com a contagem das bitstrings obtidas nas medições.

counts = result.get_counts()


# Lê os bits A, B, SUM e CARRY.

bitstring = list(counts.keys())[0]
A = int(bitstring[3])
B = int(bitstring[2])
SUM = int(bitstring[1])
CARRY = int(bitstring[0])




# =============================================================================
#
# Impressão do estado do sistema quântico no prompt:
#
# =============================================================================


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
#
# Geração dos gráficos do circuito:
#
# =============================================================================


# Janela 1: Diagrama de Circuito Quântico em Matplotlib.

fig_circuit = plt.figure(figsize=(8, 5))
ax_circ = fig_circuit.add_subplot(111)
qc.draw(output='mpl', ax=ax_circ)
ax_circ.set_title("Diagrama de Circuito Quântico")
plt.tight_layout()


# Janela 2: Histograma com as contagens das execuções.

fig_hist = plt.figure(figsize=(7, 5))
ax_hist = fig_hist.add_subplot(111)
counts_dirac = {f"|{string}⟩": valor for string, valor in counts.items()}
plot_histogram(counts_dirac, ax=ax_hist)
ax_hist.set_title("Resultados da Simulação")
plt.tight_layout()


# Janela 3: Esferas de Bloch Individuais para cada qubit.

fig_bloch = plot_bloch_multivector(state, title="Esferas de Bloch (Estado dos Qubits)")


# Janela 4: Q-Sphere para visualizar as amplitudes e fases globais.

fig_qsphere = plot_state_qsphere(state)


# Janela 5: State City para mapear tridimensionalmente a Matriz de Densidade.

fig_city = plot_state_city(state, title="State City (Matriz de Densidade)", figsize=(10, 6))


# Destaca em vermelho os estados predominantes no State City.

active_states = list(counts.keys())
for ax in fig_city.get_axes():
    for tick in ax.get_xticklabels():
        if tick.get_text() in active_states:
            tick.set_color("red")
            tick.set_weight("bold")
    for tick in ax.get_yticklabels():
        if tick.get_text() in active_states:
            tick.set_color("red")
            tick.set_weight("bold")


# Renderiza simultaneamente todas as janelas gráficas geradas.

plt.show()