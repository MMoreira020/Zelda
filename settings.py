# game setup
WIDTH    = 1280 
HEIGTH   = 720
FPS      = 60
TILESIZE = 64

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'graphics/tilemap/font/joystix.ttf'
UI_FONT_SIZE = 18

# Cores Gerais
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# cores de interface do usuário
#UI_BG_COLOR = (50, 50, 50)  # Exemplo de cinza escuro
HEALTH_COLOR = (255, 0, 0)  # Vermelho
ENERGY_COLOR = (0, 0, 255)  # Verde
UI_BORDER_COLOR_ACTIVE = (255, 215, 0) # gold


# armas
weapon_data ={
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': 'weapons/weapons/sword/full.png'},
    'lance': {'cooldown': 400, 'damage': 30, 'graphic': 'weapons/weapons/lance/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic': 'weapons/weapons/axe/full.png'},
    'rapier': {'cooldown': 50, 'damage': 8, 'graphic': 'weapons/weapons/rapier/full.png'},
    'sai': {'cooldown': 80, 'damage': 10, 'graphic': 'weapons/weapons/sai/full.png'}
}

# mágica
magic_data = {
	'flame': {'strength': 5,'cost': 20,'graphic':'magic/particles/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'magic/particles/heal/heal.png'}}