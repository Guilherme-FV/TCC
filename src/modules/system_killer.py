from signal import signal, SIGINT, SIGTERM


class System_Killer:
    """Classe para manejar o fim do programa"""

    @property
    def kill_now(self) -> bool:
        """Obtém a flag que indica o fim do programa"""
        return self.__kill_now
    
    def __init__(self):
        """Cria um objeto responsável por manejar o fim do programa"""
        self.__kill_now = False
        signal(SIGINT, self.system_kill)
        signal(SIGTERM, self.system_kill)

    def system_kill(self, signum, frame):
        """Define que o programa deve ser encerrado ao receber um comando de interrupção (ctrl + C no terminal) ou término (encerramento do processo)"""
        self.__kill_now = True
