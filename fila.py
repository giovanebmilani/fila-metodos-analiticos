import random

num_eventos = 100000  # Total de eventos aleatórios


def proximo_tempo(intervalo):
    return random.uniform(intervalo[0], intervalo[1])


# Configuração inicial para duas filas em tandem
filas_config = [
    {
        "intervalo_chegadas": (2, 5),
        "intervalo_servico": (3, 5),
        "num_servidores": 1,
        "capacidade": 5
     },
    {
        "intervalo_servico": (3, 5),
        "num_servidores": 2,
        "capacidade": 5
    }
]


# Estrutura para manter o estado das filas
class Fila:
    def __init__(self, intervalo_servico, num_servidores, capacidade, intervalo_chegadas=None):
        self.intervalo_chegadas = intervalo_chegadas
        self.intervalo_servico = intervalo_servico
        self.num_servidores = num_servidores
        self.capacidade = capacidade
        self.clientes = []
        self.clientes_perdidos = 0
        self.tempo_acumulado = 0.0

    def processar_chegada(self, tempo_atual):
        if len(self.clientes) < self.capacidade:
            tempo_servico = proximo_tempo(self.intervalo_servico)
            self.clientes.append(tempo_atual + tempo_servico)
        else:
            self.clientes_perdidos += 1

    def processar_servico(self, tempo_atual):
        if self.clientes:
            return self.clientes.pop(0)
        return None


# Inicializando as filas com a configuração correta
filas = [Fila(**config) for config in filas_config]

# Reinicializando variáveis da simulação
tempo_atual = 2.0  # Início da simulação
eventos_processados = 0
fila_atual = 0

# Simulação para duas filas em tandem
while eventos_processados < num_eventos:
    # Processar chegadas na primeira fila
    if fila_atual == 0:
        filas[fila_atual].processar_chegada(tempo_atual)
        tempo_atual += proximo_tempo(filas[fila_atual].intervalo_chegadas)

    # Processar serviço e transferir para a próxima fila, se aplicável
    tempo_servico = filas[fila_atual].processar_servico(tempo_atual)
    if tempo_servico is not None:
        eventos_processados += 1
        proxima_fila = fila_atual + 1
        if proxima_fila < len(filas):
            filas[proxima_fila].processar_chegada(tempo_servico)

    # Verificar se deve voltar para a primeira fila ou continuar na atual
    fila_atual = 0 if proxima_fila >= len(filas) else proxima_fila

# Resultados da simulação para duas filas em tandem
resultados_tandem = {
    'Fila 1 - Clientes Perdidos': filas[0].clientes_perdidos,
    'Fila 2 - Clientes Perdidos': filas[1].clientes_perdidos,
    'Tempo Global da Simulação': tempo_atual,
    'Eventos Processados': eventos_processados
}

print(resultados_tandem)
