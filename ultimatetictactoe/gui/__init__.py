from .botbattle import BotBattle
from .hotseatgame import HotSeatGame
from .spectatebotbattle import BotBattleMenu, SpectateBattle
from .singleplayer import SinglePlayer, SinglePlayerMenu
from .singleplayergame import SinglePlayerGame
from .multiplayerserver import ServerGame
from .multiplayerclient import ClientGame
from .multiplayer import MultiPlayerMenu, MultiPlayer
from .maingame import MainGameMenu, MainGame
from .qboards import QMacroBoard, QMicroBoard
from .qgame import QGame
__all__ = ['BotBattle', 'HotSeatGame', 'BotBattleMenu', 'SpectateBattle',
           'SinglePlayer', 'SinglePlayerMenu', 'SinglePlayerGame',
           'ServerGame', 'ClientGame', 'MultiPlayerMenu', 'MultiPlayer',
           'MainGameMenu', 'MainGame', 'QMacroBoard', 'QMicroBoard', 'QGame']
