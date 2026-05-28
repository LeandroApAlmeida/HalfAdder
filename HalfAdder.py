"""
===========================================================

 CIRCUTO HALF ADDER (MEIO SOMADOR) QUÂNTICO


 Este programa implementa um Half Adder reversível de 2 qubits
 de entrada (A e B) e 2 qubits de saída (SUM e CARRY) utilizando
 portas CNOT (Controlled-NOT gate) e CCX (Toffoli Gate),
 realizando a seguinte transformação unitária no espaço de
 Hilbert de 4 qubits:


   |A,B,0,0⟩
       ↓
   |A,B,A,0⟩
       ↓
   |A,B,A⊕B,0⟩
       ↓
   |A,B,A⊕B,A⋅B⟩


 O circuito em questão realiza a soma binária de A e B, 
 produzindo como saída:


   > SUM = A⊕B    (A XOR B)

   > CARRY = A⋅B  (A AND B)


 sem apagar os qubits de entrada.

 Em computação quântica, o estado de um sistema é representado
 dentro de um espaço matemático chamado espaço de Hilbert.

 Para o sistema com 4 qubits deste circuito, existem:


   2^4 = 16


 estados básicos possíveis. Estes 16 estados formam uma base
 ortonormal para o espaço de Hilbert, chamada de base 
 computacional:


   |0000⟩, |0001⟩, |0010⟩, |0011⟩,
   |0100⟩, |0101⟩, |0110⟩, |0111⟩,
   |1000⟩, |1001⟩, |1010⟩, |1011⟩,
   |1100⟩, |1101⟩, |1110⟩, |1111⟩


 Um sistema quântico não precisa estar em apenas um desses
 estados. Ele pode existir em uma superposição de vários 
 estados ao mesmo tempo (ou todos os estados). O sistema
 tem uma amplitude de probabilidade associada a cada estado.
 Ao medí-lo, ele colapsa para um único estado de forma
 probabilística (colapso da função de onda). 

 A probabilidade de cada resultado é dada por:


   ∣αi​∣²


 O circuito quântico atua linearmente sobre qualquer estado
 do espaço de Hilbert. Isso significa que a mesma transformação
 unitária é aplicada ao estado quântico completo, afetando
 simultaneamente todos os componentes da superposição. Isso
 não corresponde a paralelismo clássico no sentido tradicional, 
 mas à evolução linear de um vetor de estado no espaço de 
 Hilbert.

 No circuito Half Adder quântico implementado neste projeto, 
 as operações aplicadas são:


   CNOT(A → SUM)
   CNOT(B → SUM)
   CCX(A,B → CARRY)


 A evolução linear é dada por:


   |ψout⟩ = UCCX⋅UCNOT(B→SUM)⋅UCNOT(A→SUM) |ψin⟩


 O circuito é inicializado em:


   |A,B,0,0⟩


 e produz como resultado da transformação unitária:


   |A,B,A⊕B,A⋅B⟩


 A tabela verdade para o circuito é a seguinte:


   ┌───┬───┬─────┬───────┬───────────────────────┐
   │ A │ B │ SUM │ CARRY │ OPERAÇÃO              │                                                         │         
   ╞═══╪═══╪═════╪═══════╪═══════════════════════╡
   │ 0 │ 0 │  0  │   0   │ 0 + 0 = 0 → CARRY 0   │
   ├───┼───┼─────┼───────┼───────────────────────┤  
   │ 0 │ 1 │  1  │   0   │ 0 + 1 = 1 → CARRY 0   │
   ├───┼───┼─────┼───────┼───────────────────────┤    
   │ 1 │ 0 │  1  │   0   │ 1 + 0 = 1 → CARRY 0   │
   ├───┼───┼─────┼───────┼───────────────────────┤ 
   │ 1 │ 1 │  0  │   1   │ 1 + 1 = 0 → CARRY 1 * │ 
   └───┴───┴─────┴───────┴───────────────────────┘
   * Em binário, 1 + 1 = 10. Como na soma comum em 
     decimal, mantém-se o 0 e "sobe" 1. O carry é 
     o valor que "sobe" na soma binária pelo meio-
     somador.


 Observe que se trata da mesma tabela de um circuito Half Adder
 clássico. Mas diferentemente de um Half Adder clássico, este
 circuito não é hardwired (impresso no chip), e sim programado 
 temporalmente durante a execução.
 
 Representando em um Diagrama de Circuito Quântico:


             ┌───┐ 
   q0(A)  ───┤ H ├─────■─────────────────■──────
             └───┘     │                 │
             ┌───┐     │                 │
   q1(B)  ───┤ X ├─────┼─────────■───────■──────
             └───┘     │         │       │
                     ┌─┴─┐     ┌─┴─┐     │
   q2(S)  ───────────┤ X ├─────┤ X ├─────┼──────
                     └───┘     └───┘     │
                       ▲         ▲       │
                       │         │       │
                     SUM=A    SUM=A⊕B    │
                                         │
                                       ┌─┴─┐
   q3(C)  ─────────────────────────────┤ X ├────
                                       └───┘
                                         ▲
                                         │
                                     CARRY=A⋅B


 Com A em superposição (∣A⟩ = α∣0⟩ + β∣1⟩), B = |1⟩, SUM = |0⟩
 e CARRY = |0⟩ inicialmente, o estado do sistema passa a ser 
 uma superposição de dois estados.


   ∣ψ⟩ = α∣0,1,1,0⟩ + β∣1,1,0,1⟩
 
 
 Onde:
 
 
   α: Amplitude de probabilidade do primeiro estado (∣0,1,0,0⟩).
   
   β: Amplitude de probabilidade do segundo estado (∣1,1,0,0⟩).
   
   
 Como A está em superposição uniforme (∣A⟩ = (∣0⟩ + ∣1⟩) ​/ √2),
 então:


   ∣ψ⟩ = 1/√2 (|0,1,1,0⟩ + |1,1,0,1⟩)


 Isso significa que se medir o sistema em um determinado
 instante, terá 50% de chance de colapsar em |0,1,1,0⟩ e 50%
 de chance de colapsar em |1,1,0,1⟩. 
 
 Como não vamos aplicar interferência no circuito para selecionar
 o estado de interesse (exemplo, |1,1,0,1⟩), a cada execução
 do programa poderemos ter um destes dois estados como resultado.
 
 Neste circuito não será simulado decoerência por uma questão de
 simplificação do código. Isso seria possível usando o módulo
 qiskit_aer.noise.
 
 A decoerência é o mecanismo físico pelo qual um sistema quântico
 deixa de se comportar de acordo com as leis da mecânica quântica 
 e passa a se comportar de acordo com a física clássica. Ela
 acontece devido à interação indesejada e inevitável com o 
 ambiente externo (ruído térmico, campos magnéticos, etc.).
 É por este motivo que os computadores quânticos atuais tem
 mecanismos para geração de temperaturas criogênicas, afim de
 evitar ruído térmico, e funcionam em salas isoladas para tentar
 evitar os outros tipos de ruídos.

 Quando ocorre a decoerência, há:
 
 
   1. Perda de Fase (Dephasing): O ambiente atua como uma 
   medição constante e indesejada, destruindo a relação de
   fase sutil entre as amplitudes complexas (os αi do espaço
   de Hilbert).
   
   2. Transição de Estado: O estado de superposição (|0⟩ + |1⟩)/√2
   colapsa para uma mistura puramente clássica (ou é |0⟩, ou
   é |1⟩, sem propriedades de interferência). Em um sistema
   quântico, toda vez que há medição ele colapsa para um estado
   definido (colapso da função de onda).
   
   3. Dissipação de Energia (Relaxamento): Além da perda de
   fase, a decoerência frequentemente caminha junto com o 
   relaxamento térmico. O sistema quântico troca energia com
   o ambiente até atingir o equilíbrio. Para um qubit, isso
   geralmente significa decair de um estado de maior energia
   (|1⟩) de volta para o estado fundamental (|0⟩).
 
 
 Em um hardware real afetado por ruído, o resultado final 
 medido diverge das probabilidades ideais calculadas por 
 este programa.

===========================================================
"""


import os
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector, Operator
from qiskit.visualization import plot_histogram


# =========================================================
# Imprementação do circuito Half Adder quântico
# =========================================================


# Cria um circuito quântico e o armazena na variável qc. Os 
# argumentos (4, 4) definem a estrutura e o tamanho do circuito:
#
# O primeiro 4: Aloca 4 qubits de registradores quânticos. Eles
# são inicializados automaticamente no estado  padrão |0⟩ e
# são indexados como 0, 1, 2 e 3 (q0, q1, q2 e q3).
#
# O segundo 4: Aloca 4 bits clássicos de registradores clássicos,
# também indexados de 0 a 3. Eles servem para armazenar os
# resultados numéricos (0 ou 1) quando medir os qubits, cada
# um representando o valor do qubit no respectivo índice.
#
# No contexto deste programa, que implementa um Half Adder
# quântico, os 4 qubits representam:
#
#   > Índice 0 (q0): Entrada A.
#
#   > Índice 1 (q1): Entrada B.
#
#   > Índice 2 (q2): Soma A⊕B (SUM - bit menos significativo).
#
#   > Índice 3 (q3): Carry A⋅B (vai um).

qc = QuantumCircuit(4, 4)


# Aplica uma porta lógica quântica X (também conhecida como
# porta NOT quântica ou Bit-Flip) em q1. Isso inverte o estado
# do qubit de |0⟩ para |1⟩, fixando a entrada B do circuito
# neste valor.

qc.x(1)


# Aplica a porta Hadamard (H) em q0 (A). Isso transforma
# |0⟩ em (|0⟩ + |1⟩)/√2, colocando a entrada A nos estados
# |0⟩ e |1⟩, em superposição.
#
# O estado global passa então a ser uma superposição de duas 
# entradas:
#
#   |ψ⟩ = 1/√2 (|0,1,1,0⟩ + |1,1,0,1⟩)
#
# Devido à linearidade da transformação unitária, o circuito
# Half Adder processará as duas ramificações da superposição
# simultaneamente:
#
#   Ramo 1:
#
#   A = |0⟩, B = |1⟩ ⇒
#   SUM = |0⟩⊕|1⟩ = |1⟩, CARRY = |0⟩⋅|1⟩ = |0⟩ ⇒
#   |0,1,1,0⟩
#
#   Ramo 2: 
#
#   A = |1⟩, B = |1⟩ ⇒
#   SUM = |1⟩⊕|1⟩ = |0⟩, CARRY = |1⟩⋅|1⟩ = |1⟩ ⇒
#   |1,1,0,1⟩
#
# O estado final esperado no espaço de Hilbert é definido
# como: 
#
#   1/√2 (|0,1,1,0⟩ + |1,1,0,1⟩)
    
qc.h(0)


# Aplica a transformação unitária no espaço de Hilbert:
#
#   |A,B,0,0⟩
#       ↓
#   |A,B,A,0⟩
#       ↓
#   |A,B,A⊕B,0⟩
#       ↓
#   |A,B,A⊕B,A⋅B⟩
#
# para implementação do circuito Half Adder quântico.


# Aplica a operação CNOT(A → SUM):
#
# Matematicamente:
#
#   |A,SUM⟩ → |A,SUM⊕A⟩
#
# Como inicialmente:
#
#   SUM = |0⟩
#
# Então:
#
#   SUM=|0⟩⊕A=A ⇒
#   SUM = A
#
# Após esta etapa, o estado fica:
#
#   |A,B,0,0⟩ → |A,B,A,0⟩
    
qc.cx(0, 2) 


# Aplica a operação CNOT(B → SUM):
#
# Matematicamente:
#
#   |B,SUM⟩ → |B,SUM⊕B⟩
#
# Como:
#
#   SUM = A
#
# Então:
#
#   SUM = A⊕B
#
# Após esta etapa, o estado fica:
#
#   |A,B,A⊕B,0⟩
#
# O qubit SUM agora contém a soma binária sem carry (ver
# colunas 1, 2 e 3 da tabela verdade acima).
    
qc.cx(1, 2)


# Aplica a operação CCX(A,B → CARRY):
#
# Matematicamente:
# 
#   |A,B,C⟩ → |A,B,C⊕(A⋅B)⟩
#
# Como CARRY = |0⟩:
#
#   CARRY = A⋅B
#
# Após esta etapa, o estado fica:
#
#   |A,B,0,0⟩ → |A,B,A⊕B,A⋅B⟩
#
# O qubit CARRY agora contém o "vai um" resultante da
# operação A⋅B. Neste caso, CARRY será |1⟩ somente quando
# A = |1⟩ e B = |1⟩.
    
qc.ccx(0, 1, 3)


# =========================================================
# Medição dos qubits (Colapso da função de onda)
# =========================================================


# A medição quântica, como visto, é destrutiva e probabilística.
# A medição dos qubits A, B, SUM e CARRY projeta o sistema 
# em um dos dois ramos correlacionados da superposição.

qc.measure(0, 0)
qc.measure(1, 1)
qc.measure(2, 2)
qc.measure(3, 3)


# =========================================================
# Impressão do estado do sistema quântico
# =========================================================


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

os.system('cls')


# Imprime o título do circuito.

print("\n                         HALF ADDER QUÂNTICO\n")
print(line)


# Imprime o diagrama do circuito.

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

# input("Pressione Enter para sair...")