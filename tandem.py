import random
from dataclasses import dataclass
from typing import List


@dataclass
class FilaConfig:
	intervalo_chegada: tuple
	intervalo_atendimento: tuple
	servidores: int
	capacidade: int


@dataclass
class Evento:
	tipo: str
	tempo: float


@dataclass
class EventoProcessado:
	tipo: str
	fila: int
	tempo: float
	fila_prev: 'Fila'
	fila_next: 'Fila'
	# estado: List


class Fila:

	def __init__(self, config: FilaConfig):
		self.fila_prev = config.fila_prev
		self.fila_next = config.fila_next
		self.intervalo_chegada = config.intervalo_chegada
		self.intervalo_atendimento = config.intervalo_atendimento
		self.servidores = config.servidores
		self.capacidade = config.capacidade 
		self.clientes_na_fila = 0
		self.sim_ocorridas = 0
		self.eventos: List[Evento] = []
		self.eventos_processados = []

	def escolhe_evento(self):
		proximo = self.eventos[0]
		for evento in self.eventos:
			if evento.tempo < proximo:
				proximo = evento
		return proximo

	def projeta_saida(self):
		self.sim_ocorridas += 1
		rand = random.uniform(0, 1)
		return ((self.intervalo_atendimento[1] - self.intervalo_atendimento[0]) * rand) + self.intervalo_atendimento[0]

	def projeta_chegada(self):
		self.sim_ocorridas += 1
		rand = random.uniform(0, 1)
		return ((self.intervalo_chegada[1] - self.intervalo_chegada[0]) * rand) + self.intervalo_chegada[0]

	def simular(self, primeira_chegada: float, num_simulacoes: int):
		
		self.eventos.append(
			Evento('chegada', primeira_chegada)
		)
		self.eventos.append(
			Evento('saida', self.projeta_saida())
		)

		while self.sim_ocorridas < num_simulacoes:
			atual = self.escolhe_evento()

			if atual.tipo == 'chegada':
				self.clientes_na_fila += 1
			elif atual.tipo == 'saida':
				self.clientes_na_fila -= 1
		
			self.eventos_processados.append(
				EventoProcessado(atual.tipo, self.clientes_na_fila, atual.tempo)
			)


# class Tandem:

# 	def __init__(self, filas: List[Fila]):
# 		self.filas = filas

# 	def simula(self, primeira_chegada: float, num_simulacoes: int):
		
# 		self.filas[0].eventos.append(
# 			Evento('chegada', primeira_chegada)
# 		)
# 		saida = Evento('saida', primeira_chegada + self.filas[0].projeta_saida())
# 		self.filas[0].eventos.append(saida)
# 		self.filas[1].eventos.append(
# 			Evento('chegada', saida.tempo)
# 		)
# 		self.filas[1].eventos.append(
# 			Evento('saida', saida.tempo + self.filas[1].projeta_saida())
# 		)
# 		sim_ocorridas = 2

# 		while sim_ocorridas < num_simulacoes:



config = FilaConfig(
	intervalo_chegada=(1, 4),
	intervalo_atendimento=(3, 4),
	capacidade=3,
	servidores=2
)

fila = Fila(config)


