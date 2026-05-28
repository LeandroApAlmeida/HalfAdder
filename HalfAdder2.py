# Importa a classe QuantumCircuit da biblioteca Qiskit.
# Ela permite criar e manipular circuitos quânticos.
from qiskit import QuantumCircuit

# Importa o simulador quântico AerSimulator.
# Ele executa o circuito em um simulador clássico.
from qiskit_aer import AerSimulator


# Cria um circuito com:
# - 4 qubits quânticos
# - 4 bits clássicos para armazenar medições
qc = QuantumCircuit(4, 4)

# =====================================================
# PREPARAÇÃO
# =====================================================

# Aplica uma porta X no qubit 1.
# A porta X funciona como um NOT:
# |0> -> |1>
#
# Isso define:
# B = 1
qc.x(1)

# Aplica uma porta Hadamard no qubit 0.
#
# A porta H cria superposição:
# |0> -> (|0> + |1>) / sqrt(2)
#
# Assim, o qubit A passa a representar
# simultaneamente 0 e 1.
qc.h(0)

# =====================================================
# COMPUTE
# =====================================================

# CNOT:
# Se q0 = 1, inverte q2.
#
# q2 começa em 0.
# Depois dessa operação:
# q2 = q0
#
# Aqui q2 começa a armazenar parte da soma.
qc.cx(0, 2)

# Outra CNOT:
# Se q1 = 1, inverte q2.
#
# Resultado:
# q2 = q0 XOR q1
#
# Isso calcula o bit SUM de uma soma binária.
qc.cx(1, 2)

# Porta Toffoli (CCX):
# Controlada por q0 e q1.
#
# Só inverte q3 se:
# q0 = 1 E q1 = 1
#
# Resultado:
# q3 = q0 AND q1
#
# Isso calcula o CARRY da soma binária.
qc.ccx(0, 1, 3)

# Aplica uma porta Z no qubit 3.
#
# A porta Z altera a fase do estado:
# |1> ganha um sinal negativo.
#
# Isso "marca" o estado desejado usando fase,
# técnica comum em algoritmos quânticos.
qc.z(3)

# =====================================================
# UNCOMPUTE
# =====================================================

# Reverte a operação Toffoli anterior.
#
# Como portas quânticas são reversíveis,
# aplicar a mesma CCX desfaz o cálculo.
qc.ccx(0, 1, 3)

# Desfaz a segunda CNOT.
qc.cx(1, 2)

# Desfaz a primeira CNOT.
qc.cx(0, 2)

# Nesse ponto, os qubits auxiliares voltam
# ao estado original.
#
# Isso é chamado de "uncompute":
# limpar lixo quântico intermediário.
# Muito importante em computação quântica.

# =====================================================
# INTERFERÊNCIA
# =====================================================

# Aplica novamente Hadamard no qubit 0.
#
# Isso provoca interferência quântica:
# amplitudes podem se reforçar ou cancelar.
#
# Dependendo da fase marcada antes,
# alguns resultados ficam mais prováveis.
qc.h(0)

# =====================================================
# MEDIÇÃO
# =====================================================

# Mede todos os qubits.
#
# range(4) -> qubits 0,1,2,3
# range(4) -> bits clássicos 0,1,2,3
#
# O estado quântico colapsa para valores clássicos.
qc.measure(range(4), range(4))

# =====================================================
# SIMULAÇÃO
# =====================================================

# Cria uma instância do simulador.
sim = AerSimulator()

# Executa o circuito 1000 vezes (shots=1000).
#
# Cada execução pode produzir resultados
# diferentes devido à natureza probabilística
# da mecânica quântica.
result = sim.run(qc, shots=1000).result()

# Obtém a contagem de resultados medidos.
#
# Exemplo:
# {'0010': 520, '1010': 480}
counts = result.get_counts()

# Exibe os resultados brutos.
print("\nRESULTADO BRUTO:\n")
print(counts)

# Pega uma das bitstrings medidas.
#
# next(iter(counts)) pega a primeira chave
# do dicionário.
bitstring = next(iter(counts))

# O Qiskit imprime os bits na ordem:
#
# q3 q2 q1 q0
#
# Ou seja:
# bit mais significativo -> menos significativo
q3, q2, q1, q0 = bitstring

# Converte q0 para inteiro.
#
# q0 representa A.
A = int(q0)

# Converte q1 para inteiro.
#
# q1 representa B.
B = int(q1)

# Recalcula classicamente:
#
# XOR -> soma binária sem carry
SUM = A ^ B

# AND -> carry da soma binária
CARRY = A & B

print("\nRESULTADO INTERPRETADO:\n")

# Mostra o valor de A
print("A     =", A)

# Mostra o valor de B
print("B     =", B)

# Mostra o bit de soma
print("SUM   =", SUM)

# Mostra o carry
print("CARRY =", CARRY)

print("\nDIAGRAMA:\n")

# Desenha o circuito quântico em formato texto.
print(qc.draw())