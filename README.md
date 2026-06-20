<h3>Half Adder Quântico em Qiskit</h3>

<br>

Neste projeto implemento um Half Adder (meio somador) quântico, com 2 qubits de entrada (A e B) e 2 qubits auxiliares (SUM e CARRY). O circuito produz como saída o resultado da soma (bit menos significativo) em SUM (A⊕B) e o carry (vai um) em CARRY (A⋅B).

O circuito em questão é equivalente ao circuito clássico:

<p align="center">
  <img src="https://github.com/user-attachments/assets/5cacbaf1-c68f-4f37-a350-44779aa6b485" width="20%">
</p>

Para testá-lo, é necessário que se tenha o Python instalado, e que se instale as seguintes bibliotecas:

<b>> pip install qiskit</b>

<b>> pip install qiskit-aer</b>

<b>> pip install "qiskit[visualization]" matplotlib pylatexenc</b>

Com estas bibliotecas instaladas, não é necessário testar o código em um computador quântico real (IBMQ), pois elas vão simulador um computador quântico em sua máquina local.

Para entender como o circuito funciona, leia os comentários no arquivo de código-fonte "HalfAdder.py".

<br>

