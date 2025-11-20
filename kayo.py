
import random
from abc import ABC, abstractmethod
from typing import List, Optional


class Dado:
    """Questão 24 (20 pts): classe utilitária para rolar dados."""
    @staticmethod
    def rolar(min_val: int = 1, max_val: int = 6) -> int:
        return random.randint(min_val, max_val)


class Arma:
    def __init__(self, nome: str, dano: int):
        self.nome = nome
        self.dano = dano

    def __str__(self):
        return f"{self.nome} (Dano: {self.dano})"

class Pocao:
    def __init__(self, nome: str, cura: int):
        self.nome = nome
        self.cura = cura

    def usar(self, alvo: 'Personagem') -> str:
    
        anterior = alvo.hp
        alvo.hp = alvo.hp + self.cura
        return f"{alvo.nome} usou {self.nome}: {anterior} -> {alvo.hp}"

    def __str__(self):
        return f"{self.nome} (+{self.cura} HP)"


espada_longa = Arma("Espada Longa", dano=10)
cajado_magico = Arma("Cajado Mágico", dano=6)
pocao_vida = Pocao("Poção de Vida", cura=30)


class Inventario:
    def __init__(self):
        self.itens: List[object] = []

    def adicionar(self, item: object) -> None:
        self.itens.append(item)

    def remover(self, item: object) -> bool:
        if item in self.itens:
            self.itens.remove(item)
            return True
        return False

    def listar(self) -> List[object]:
        return list(self.itens)

    def encontrar_pocao(self) -> Optional[Pocao]:
        for it in self.itens:
            if isinstance(it, Pocao):
                return it
        return None


class Personagem(ABC):
    def __init__(self, nome: str, hp_max: int, forca: int):
        self.nome = nome
        self._hp_max = hp_max
        self._hp = hp_max  
        self.forca = forca
        self.arma: Optional[Arma] = None
        self.inventario = Inventario()  
        self.habilidades: List['Habilidade'] = []

    
    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, valor: int) -> None:
        if not isinstance(valor, (int, float)):
            raise TypeError("hp deve ser numérico")
        if valor < 0:
            self._hp = 0
        elif valor > self._hp_max:
            self._hp = int(self._hp_max)
        else:
            self._hp = int(valor)

    @property
    def hp_max(self) -> int:
        return self._hp_max

    def esta_vivo(self) -> bool:
        
        return self.hp > 0

    def equipar_arma(self, arma: Arma) -> None:

        self.arma = arma

    def poder_ataque(self) -> int:
        
        arma_dano = self.arma.dano if self.arma else 0
        return self.forca + arma_dano

    def receber_dano(self, dano: int) -> str:
        
        if dano < 0:
            raise ValueError("dano não pode ser negativo")
        anterior = self.hp
        self.hp = self.hp - dano
        return f"{self.nome} recebeu {dano} de dano: {anterior} -> {self.hp}"

    @abstractmethod
    def atacar(self, alvo: 'Personagem') -> str:
        pass

    def __str__(self) -> str:
        arma = str(self.arma) if self.arma else "Nenhuma"
        return f"{self.nome} — HP: {self.hp}/{self.hp_max} | Força: {self.forca} | Arma: {arma}"


class Guerreiro(Personagem):
    def __init__(self, nome: str, hp_max: int = 120, forca: int = 15):
        super().__init__(nome, hp_max, forca)

    def atacar(self, alvo: Personagem) -> str:
    
        base = self.poder_ataque()
        variacao = Dado.rolar(1, 4)
        dano = base + variacao
        res = alvo.receber_dano(dano)
        return f"{self.nome} (Guerreiro) ataca {alvo.nome} com {dano}. {res}"


class Mago(Personagem):
    def __init__(self, nome: str, hp_max: int = 80, forca: int = 8, poder_magico: int = 20):
        super().__init__(nome, hp_max, forca)
        self.poder_magico = poder_magico

    def atacar(self, alvo: Personagem) -> str:
        
        variacao = Dado.rolar(1, 6)
        dano = self.poder_magico + variacao
        res = alvo.receber_dano(dano)
        return f"{self.nome} (Mago) lança magia em {alvo.nome} causando {dano}. {res}"

class Arqueiro(Personagem):
    def __init__(self, nome: str, hp_max: int = 90, forca: int = 10, precisao: int = 14):
        super().__init__(nome, hp_max, forca)
        self.precisao = precisao

    def atacar(self, alvo: Personagem) -> str:
        
        roll = Dado.rolar(1, 20)
        if roll <= self.precisao:
            dano = self.poder_ataque() + Dado.rolar(1, 4)
            res = alvo.receber_dano(dano)
            return f"{self.nome} (Arqueiro) acerta {alvo.nome} com {dano} (roll {roll}). {res}"
        else:
            return f"{self.nome} (Arqueiro) errou o ataque (roll {roll})."

class Monstro(Personagem):
    def __init__(self, nome: str, hp_max: int, forca: int):
        super().__init__(nome, hp_max, forca)

    def atacar(self, alvo: Personagem) -> str:
        dano = self.poder_ataque() + Dado.rolar(1, 4)
        res = alvo.receber_dano(dano)
        return f"{self.nome} (Monstro) ataca {alvo.nome} com {dano}. {res}"

class Goblin(Monstro):
    def __init__(self, nome: str = "Goblin", hp_max: int = 50, forca: int = 8):
        super().__init__(nome, hp_max, forca)

    @classmethod
    def criar_padrao(cls) -> 'Goblin':
    
        return cls()

class Orc(Monstro):
    def __init__(self, nome: str = "Orc", hp_max: int = 100, forca: int = 12, crit_chance: float = 0.2):
        super().__init__(nome, hp_max, forca)
        self.crit_chance = crit_chance

    def atacar(self, alvo: Personagem) -> str:
        
        dano = self.poder_ataque()
        if random.random() < self.crit_chance:
            dano *= 2
            extra = " CRÍTICO!"
        else:
            extra = ""
        dano += Dado.rolar(1, 6)
        res = alvo.receber_dano(dano)
        return f"{self.nome} ataca{extra} {alvo.nome} com {dano}. {res}"


class Habilidade(ABC):

    @abstractmethod
    def usar(self, usuario: Personagem, alvo: Personagem) -> str:
        pass

class AtaqueForte(Habilidade):

    def usar(self, usuario: Personagem, alvo: Personagem) -> str:
        dano = int(usuario.forca * 1.8) + Dado.rolar(1, 4)
        res = alvo.receber_dano(dano)
        return f"{usuario.nome} usa AtaqueForte em {alvo.nome} com {dano}. {res}"

class BolaDeFogo(Habilidade):
    def usar(self, usuario: Personagem, alvo: Personagem) -> str:
        mag = getattr(usuario, "poder_magico", 10)
        dano = mag + Dado.rolar(1, 8) + 5
        res = alvo.receber_dano(dano)
        return f"{usuario.nome} lança BolaDeFogo em {alvo.nome} causando {dano}. {res}"


def usar_habilidade_por_nome(usuario: Personagem, nome_hab: str, alvo: Personagem) -> Optional[str]:
    for hab in usuario.habilidades:
        if hab.__class__.__name__.lower() == nome_hab.lower():
            return hab.usar(usuario, alvo)
    return None

class Batalha:
    
    def __init__(self, a, b):
        
        self.a = a
        self.b = b

    def _eh_equipes(self) -> bool:
        return isinstance(self.a, list) or isinstance(self.b, list)

    def duelo(self, p1: Personagem, p2: Personagem) -> Personagem:
        
        turno = 0
        while p1.esta_vivo() and p2.esta_vivo():
            atacante, defensor = (p1, p2) if turno % 2 == 0 else (p2, p1)
            
            if atacante.habilidades and Dado.rolar(1, 2) == 1:
                hab = random.choice(atacante.habilidades)
                hab.usar(atacante, defensor)
            else:
                atacante.atacar(defensor)
            turno += 1
        vencedor = p1 if p1.esta_vivo() else p2
        return vencedor

    def batalhar_equipes(self, equipe_a: List[Personagem], equipe_b: List[Personagem]) -> str:
        
        turno = 0
        while any(p.esta_vivo() for p in equipe_a) and any(p.esta_vivo() for p in equipe_b):
            turno += 1
            
            for atacante in [p for p in equipe_a if p.esta_vivo()]:
                alvos = [q for q in equipe_b if q.esta_vivo()]
                if not alvos:
                    break
                alvo = random.choice(alvos)
                if atacante.habilidades and Dado.rolar(1, 3) == 1:
                    hab = random.choice(atacante.habilidades)
                    hab.usar(atacante, alvo)
                else:
                    atacante.atacar(alvo)
        
            for atacante in [p for p in equipe_b if p.esta_vivo()]:
                alvos = [q for q in equipe_a if q.esta_vivo()]
                if not alvos:
                    break
                alvo = random.choice(alvos)
                if atacante.habilidades and Dado.rolar(1, 3) == 1:
                    hab = random.choice(atacante.habilidades)
                    hab.usar(atacante, alvo)
                else:
                    atacante.atacar(alvo)
        vencedor = "A" if any(p.esta_vivo() for p in equipe_a) else "B"
        return vencedor

    def iniciar(self):
        if self._eh_equipes():
            equipe_a = self.a if isinstance(self.a, list) else [self.a]
            equipe_b = self.b if isinstance(self.b, list) else [self.b]
            return self.batalhar_equipes(equipe_a, equipe_b)
        else:
            return self.duelo(self.a, self.b)


def criar_cenario_demo() -> dict:
    random.seed(42)  

    g = Guerreiro("Arthos")
    m = Mago("Lunara")
    a = Arqueiro("Faelan")

    g.equipar_arma(espada_longa)
    m.equipar_arma(cajado_magico)

    g.habilidades.append(AtaqueForte())
    m.habilidades.append(BolaDeFogo())

    g.inventario.adicionar(pocao_vida)

    gob = Goblin.criar_padrao()
    orc = Orc()

    return {"guerreiro": g, "mago": m, "arqueiro": a, "goblin": gob, "orc": orc}

def run_tests():
    random.seed(0)
    c = criar_cenario_demo()
    g = c["guerreiro"]
    gob = c["goblin"]

    s = str(g)
    assert 'HP:' in s and 'Força:' in s

    base_sem = Guerreiro("SemArma", hp_max=50, forca=10)
    assert base_sem.poder_ataque() == 10
    base_sem.equipar_arma(Arma("Teste", 5))
    assert base_sem.poder_ataque() == 15

    p = Mago("M", hp_max=10, forca=2, poder_magico=5)
    p.receber_dano(50)
    assert p.hp == 0

    g2 = Goblin.criar_padrao()
    assert isinstance(g2, Goblin)

    heroi = Guerreiro("Her")
    monstro = Goblin.criar_padrao()
    batalha = Batalha(heroi, monstro)
    vencedor = batalha.iniciar()
    assert isinstance(vencedor, Personagem)

    heroi.habilidades.append(AtaqueForte())
    mon = Orc()
    res = usar_habilidade_por_nome(heroi, "ataqueforte", mon)
    assert res is not None

    print("Todos os testes passaram!")

def run_demo():
    c = criar_cenario_demo()
    g = c["guerreiro"]
    m = c["mago"]
    a = c["arqueiro"]
    gob = c["goblin"]
    orc = c["orc"]

    print("=== DEMO: Duelo Guerreiro vs Goblin ===")
    batalha1 = Batalha(g, gob)
    vencedor1 = batalha1.iniciar()
    print(f"Vencedor: {vencedor1.nome}")

    print("=== DEMO: Batalha em equipe (Heróis vs Inimigos) ===")
    equipe_herois = [g, m, a]
    equipe_inimigos = [Goblin.criar_padrao(), Orc(nome='Uruk')]
    batalha_eq = Batalha(equipe_herois, equipe_inimigos)
    vencedor_eq = batalha_eq.iniciar()
    print(f"Vencedor da equipe: {vencedor_eq}")

if __name__ == '__main__':
    run_tests()
    run_demo()


