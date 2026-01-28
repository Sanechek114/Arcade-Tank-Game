TITLE = 'игра про танки'
RELOUDTIME = 3
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
DEAD_ZONE_W = int(SCREEN_WIDTH * 0.35)
DEAD_ZONE_H = int(SCREEN_HEIGHT * 0.45)
SCALE = int(SCREEN_HEIGHT / 540)
MAX_SPEED = 125 * SCALE
ACCELERATION = 50 * SCALE
BRAKINGFORCE = 50 * SCALE
TURRETROTATIONSPEED = 100
HULLROTATIONSPEED = 90
CAMERA_LERP = 1
ANIMATION_SPEED = 0.25
BULLET_TIME = 3
BULLET_SPEED = 400 * SCALE
ENEMY_VIEW = 250 * SCALE
LIVES = 3

# Координаты спавна игрока на разных картах
PLAYER_COORDS = [
    (2, 3),
    (2, 11),
    (3, 4),
    (8, 2)
    ]
# Координаты спавна и тип врагов на разных картах
# 1, 2 - координаты. 3 - тип врага от 1 до 4(4 - БОСС).
ENEMY_COORDS_TYPE = [
    [
        (4.5, 4.5, 1),
        (2.5, 12.5, 1),
        (13, 12, 1),
        (18, 2.5, 1),
        (11, 5.5, 2)
        ],
    [
        (9, 12, 1),
        (14, 7, 2),
        (14, 12, 2),
        (17, 4, 2),
        (8, 3, 1)
        ],
    [
        (6, 10, 2),
        (15, 11, 3),
        (18, 3.5, 2),
        (10, 2.5, 3),
        (13, 6, 2)
        ],
    [
        (11, 7, 4),
        (5, 4, 2),
        (14, 7, 2)
        ]
]
