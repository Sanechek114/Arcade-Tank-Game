TITLE = 'игра про танки'
RELOUDTIME = 4
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
DEAD_ZONE_W = int(SCREEN_WIDTH * 0.35)
DEAD_ZONE_H = int(SCREEN_HEIGHT * 0.45)
SCALE = SCREEN_HEIGHT / 540
MAX_SPEED = 125 * SCALE
ACCELERATION = 50 * SCALE
BRAKINGFORCE = 50 * SCALE
TURRETROTATIONSPEED = 70
HULLROTATIONSPEED = 80
CAMERA_LERP = 1
ANIMATION_SPEED = 0.25
BULLET_TIME = 3
BULLET_SPEED = 400 * SCALE
ENEMY_VIEW = 250 * SCALE
LIVES = 3

# Координаты спавна игрока на разных картах
PLAYER_COORDS = [
    (0, 0),
    (2, 11),
    (25, 50),
    (50, 50)
    ]
# Координаты врагов на разных картах
ENEMY_COORDS_TYPE = [
    [
        (4.5, 4.5, 1),
        (2, 11, 2)
        ],
    [
        (9, 12, 1),
        (14, 7, 2),
        (14, 12, 2),
        (17, 4, 2),
        (8, 3, 1)
        ],
    [
        (450, 450, 2),
        (100, 100, 2)
        ],
    [
        (10, 6, 4),
        (5, 3, 2),
        (14, 11, 2)
        ]
]
