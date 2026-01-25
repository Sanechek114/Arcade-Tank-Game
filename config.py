TITLE = 'игра про танки'
RELOUDTIME = 5.5
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1080
SCALE = SCREEN_HEIGHT / 540
MAX_SPEED = 125 * SCALE
ACCELERATION = 50 * SCALE
BRAKINGFORCE = 50 * SCALE
TURRETROTATIONSPEED = 70
HULLROTATIONSPEED = 60
CAMERA_LERP = 0.12
ANIMATION_SPEED = 0.25
BULLET_TIME = 3
BULLET_SPEED = 400 * SCALE
ENEMY_VIEW = 250 * SCALE
LIVES = 3

# Координаты спавна игрока на разных картах
PLAYER_COORDS = [
    (25, 50),
    (50, 50),
    (25, 50),
    (50, 50)
    ]
# Координаты врагов на разных картах
ENEMY_COORDS_TYPE = [
    [
        (200, 200, 1),
        (100, 100, 2)
        ],
    [
        (300, 200, 1),
        (100, 100, 3)
        ],
    [
        (450, 450, 2),
        (100, 100, 2)
        ],
    [
        (450, 450, 3),
        (100, 100, 4)
        ]
]
