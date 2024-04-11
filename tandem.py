from enum import Enum

class TipoEvento(Enum):
    CHEGADA = 'chegada'
    SAIDA = 'saida'
    PASSAGEM = 'passagem'

class Evento:
    def __init__(self, tipo, tempo) -> None:
        self.tipo = tipo
        self.tempo = tempo

    def __str__(self):
        return f'Tipo: {self.tipo} -- Tempo: {self.tempo}'

class Fila:
    def __init__(self, capacidade, servidores, intervalo_chegada, intervalo_servico) -> None:
        self.capacidade = capacidade 
        self.servidores = servidores
        self.intervalo_chegada: Intervalo = intervalo_chegada
        self.intervalo_servico: Intervalo = intervalo_servico
        self.status = 0
        self.perdas = 0
        self.estados = [0] * (capacidade + 1)

    def add(self):
        self.status = self.status + 1

    def out(self):
        self.status = self.status - 1

    def perda(self):
        self.perdas = self.perdas + 1

    def update_estados(self, tempo):
        self.estados[self.status] = self.estados[self.status] + tempo 

    def __str__(self) -> str:
        string = f'capacidade: {self.capacidade}' + '\n'
        string = string + f'Servidores: {self.servidores}' + '\n'
        string = string + f'Tempo Chegada: {self.intervalo_chegada}' + '\n'
        string = string + f'Intervalo Servico: {self.intervalo_servico}' + '\n'
        string = string + f'Status: {self.status}' + '\n'
        string = string + f'Perdas: {self.perdas}' + '\n'
        string = string + f'Estados: {self.estados}'

        return string

class Intervalo:
    def __init__(self, inicio, final) -> None:
        self.inicio = inicio
        self.final = final

    def __str__(self) -> str:
        return f'Inicio {self.inicio} -- Fim {self.final}'

class Escalonador():
    def __init__(self, numero_al):
        self.numero_al = numero_al
        self.escalonador = []

    def add(self, evento: Evento, interval):
        if len(self.numero_al) == 0:
            return
        evento.tempo = evento.tempo + self.get_random(interval)
        self.escalonador.append(evento)
        self.escalonador.sort(key=lambda event: event.tempo)

    def add_rand(self, event, rand_num):
        event.tempo = event.tempo + rand_num
        self.escalonador.append(event)
        self.escalonador.sort(key=lambda event: event.tempo)

    def schedule(self) -> Evento:
        return self.escalonador.pop(0)
    
    def get_random(self, intervalo: Intervalo) -> float:
        rand_num = self.numero_al.pop(0)
        return intervalo.inicio + (intervalo.final - intervalo.inicio) * rand_num

class PseudoNumAleatorio:
    def __init__(self, seed) -> None:
        self.m = 2**28
        self.a = 1317293
        self.c = 12309820398
        self.seed = seed

    def gen_rand(self, n):
        x = self.seed
        arr = []
        for _ in range(n):
            op = (self.a * x + self.c) % self.m
            x = op
            arr.append(op/self.m)
        return arr

class Simulacao:
    def __init__(self, tempo_chegada, fila1, fila2, escalonador):
        self.tempo_chegada = tempo_chegada
        self.fila1: Fila = fila1
        self.fila2: Fila = fila2
        self.escalonador: Escalonador = escalonador
        self.tempo_global = 0

    def run(self):
        self.escalonador.add_rand(Evento(TipoEvento.CHEGADA, self.tempo_chegada), 0)
        while len(self.escalonador.numero_al) != 0:
            prox_evento = self.escalonador.schedule()

            if (prox_evento.tipo == TipoEvento.CHEGADA):
                self.chegada(prox_evento)
            elif (prox_evento.tipo == TipoEvento.SAIDA):
                self.saida(prox_evento)
            elif (prox_evento.tipo == TipoEvento.PASSAGEM):
                self.passagem(prox_evento)

    def chegada(self, event):
        self.__update_global_time(event)
        if self.fila1.status < self.fila1.capacidade:
            self.fila1.add()
            if self.fila1.status <= self.fila1.servidores:
                self.escalonador.add(Evento(TipoEvento.PASSAGEM, self.tempo_global), self.fila1.intervalo_servico)
        else:
            self.fila1.perda()
        self.escalonador.add(Evento(TipoEvento.CHEGADA, self.tempo_global), self.fila1.intervalo_chegada)

    def saida(self, event):
        self.__update_global_time(event)
        self.fila2.out()
        if self.fila2.status >= self.fila2.servidores:
            self.escalonador.add(Evento(TipoEvento.SAIDA, self.tempo_global), self.fila2.intervalo_servico)

    def passagem(self, event):
        self.__update_global_time(event)
        self.fila1.out()
        if self.fila1.status >= self.fila1.servidores:
            self.escalonador.add(Evento(TipoEvento.PASSAGEM, self.tempo_global), self.fila1.intervalo_servico)
        if self.fila2.status < self.fila2.capacidade:
            self.fila2.add()
            if self.fila2.status <= self.fila2.servidores:
                self.escalonador.add(Evento(TipoEvento.SAIDA, self.tempo_global), self.fila2.intervalo_servico)
        else:
            self.fila2.perda()

    def __update_global_time(self, evento):
        self.fila1.update_estados(evento.tempo - self.tempo_global)
        self.fila2.update_estados(evento.tempo - self.tempo_global)
        self.tempo_global = evento.tempo

class Estatisticas:
    def __init__(self, simulacao):
        self.simulacao : Simulacao = simulacao 

    def calc_prob_distribution(self, fila: Fila):
        distribution = [0] * (fila.capacidade + 1)
        estados = fila.estados
        tempo_global = self.simulacao.tempo_global

        for index, estado in enumerate(estados):
            distribution[index] = (index, estado, estado/tempo_global)

        return distribution

    def show_prob_distribution(self, queue):
        distribution = self.calc_prob_distribution(queue)

        print("Estado\t\tTempo\t\tProbabilidade")
        for row in distribution:
            if row[1] != 0:
                print(f"{row[0]}\t\t{round(row[1], 4)}\t\t{row[2] * 100:,.2f}%")

    def show_global_time(self):
        print("Tempo de simulacao:", self.simulacao.tempo_global)

    def show_losses(self, queue: Fila):
        print("Perdas:", queue.perdas)
    
    def report(self):
        filas = [self.simulacao.fila1, self.simulacao.fila2]
        for index, fila in enumerate(filas): 
            print("********************************************************")
            print(f"Fila:  Fila{index+1} (G/G/{fila.servidores}/{fila.capacidade})")
            if fila.intervalo_chegada != None:
                print(f"Chegada: {fila.intervalo_chegada.inicio}..{fila.intervalo_chegada.final}")
            print(f"Servico: {fila.intervalo_servico.inicio}..{fila.intervalo_servico.final}")
            print("********************************************************")
            self.show_prob_distribution(fila)
            self.show_losses(fila)

        self.show_global_time()

def inicia_fila(config, nome) -> Fila:
    config_simulacao = config['filas'][nome]

    capacidade = config_simulacao['capacidade']
    servidores = config_simulacao['servidores']
    intervalo_servico = Intervalo(config_simulacao['minService'], config_simulacao['maxService'])

    if nome == 'FILA1':
        intervalo_chegada = Intervalo(config_simulacao['chegadaMin'], config_simulacao['chegadaMax'])
    else:
        intervalo_chegada = None

    return Fila(capacidade=capacidade, servidores=servidores, intervalo_chegada=intervalo_chegada, intervalo_servico=intervalo_servico)

def main():
    CONFIG = {
		"chegada": {
			"Fila1": 1.5
		},
		"filas": {
			"FILA1": {
			"servidores": 2,
			"capacidade": 3,
			"chegadaMin": 1,
			"chegadaMax": 4,
			"minService": 3,
			"maxService": 4
			},
			"FILA2": {
			"servidores": 1,
			"capacidade": 5,
			"minService": 2,
			"maxService": 3
			}
		},
		"num_aleatorios": 100000,
		"seed": [
			1713
		]
	}

    tempo_chegada = CONFIG['chegada']['Fila1']
    seeds = CONFIG['seed']
    fila1 = inicia_fila(CONFIG, 'FILA1')
    fila2 = inicia_fila(CONFIG, 'FILA2')

    num_aleat = (
        PseudoNumAleatorio(seeds[0]).gen_rand(CONFIG['num_aleatorios'])
    )

    escalonador = Escalonador(num_aleat)

    sim = Simulacao(tempo_chegada=tempo_chegada, fila1=fila1, fila2=fila2, escalonador=escalonador)

    sim.run()

    Estatisticas(sim).report()

if __name__ == '__main__':
    main()
