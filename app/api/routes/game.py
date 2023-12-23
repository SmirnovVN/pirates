from fastapi import APIRouter, HTTPException

from app.entities.game import Game
from app.enums.game_type import GameType
from app.service.game_service import leave_deathmatch, register_battle_royal, \
    register_deathmatch

router = APIRouter(prefix='/game')


@router.get("/{game_type}")
async def game_new(game_type: GameType):
    """
    Get any ship details
    """
    game = Game()
    if game.started:
        return 'Game started already. Call game/stop to stop game'
    if game_type == GameType.BATTLE_ROYAL:
        success = await register_battle_royal()
    elif game_type == GameType.DEATHMATCH:
        success = await register_deathmatch()
    else:
        raise HTTPException(400,
                            detail=f'Bad game type: {game_type} . Pass battle_royal or deathmatch')
    if success:
        await game.start()
    return 'Game started'


@router.get("/stop")
async def game_stop():
    """
    Get any ship details
    """
    Game.stop()
    await leave_deathmatch()
    return 'Game stopped'