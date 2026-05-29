@namespace
class SpriteKind:
    Sword = SpriteKind.create()
    door = SpriteKind.create()
    mainbadguy = SpriteKind.create()
    Friend = SpriteKind.create()
    LAVA = SpriteKind.create()
    Bat = SpriteKind.create()


ChestOpened = False
Generic_swipe_attack_enemy: Sprite = None
ENEMY_ENGAGED = False
coin: Sprite = None
Coin_level_1_secret_room_location_list: List[tiles.Location] = []
Bat2: Sprite = None
floorisLava: Sprite = None

facing_left = False
facing_right = True
HasSword = False
myEnemy_start_to_follow_player = False
Enemy_on_level_2_has_spawned = False
mySprite_attacking = False
Lava_activated_level_1_ssecret_room = False
lava_active = False
lava_room_complete = False
onLadder = False
Chest: Sprite = None
mySprite: Sprite = None
Follower: Sprite = None
Show_door_diologe_promt_level_one_seceret_door = False


def set_level_1_background():
    scene.set_background_image(assets.image("""
        Level 1 background
    """))


def stop_lava():
    global lava_active, floorisLava
    lava_active = False
    sprites.destroy_all_sprites_of_kind(SpriteKind.LAVA)
    floorisLava = None


def start_lava():
    global floorisLava, lava_active, Lava_activated_level_1_ssecret_room

    if Lava_activated_level_1_ssecret_room == False and lava_room_complete == False:
        Lava_activated_level_1_ssecret_room = True
        lava_active = True

        floorisLava = sprites.create(assets.image("""
            LAVA
        """), SpriteKind.LAVA)

        floorisLava.set_position(mySprite.x, mySprite.y + 120)
        floorisLava.vy = 0
        floorisLava.set_flag(SpriteFlag.GHOST_THROUGH_WALLS, True)

        game.splash("Duck Friend: HURRY! WATCH OUT FOR THE RISING LAVA!!!")
        scene.camera_shake(4, 1000)


def on_update_lava():
    if lava_active == True:
        if floorisLava:
            if floorisLava.y > mySprite.y + 40:
                floorisLava.vy = -4
            else:
                floorisLava.vy = -2

game.on_update(on_update_lava)


def on_lava_trigger(sprite2, location2):
    start_lava()

scene.on_overlap_tile(SpriteKind.player, assets.tile("""
    pressure plate senser radar of dungen secret room level 1
"""), on_lava_trigger)


def on_lava_touch(sprite4, otherSprite):
    stop_lava()
    info.change_life_by(-1)

    tiles.set_current_tilemap(tilemap("""
        Level1 Medieval assessmentPlatformer
    """))

    set_level_1_background()
    tiles.place_on_tile(mySprite, tiles.get_tile_location(15, 1))

sprites.on_overlap(SpriteKind.player, SpriteKind.LAVA, on_lava_touch)


def on_secret_room_exit(sprite8, location7):
    global lava_room_complete, Lava_activated_level_1_ssecret_room

    stop_lava()

    lava_room_complete = True
    Lava_activated_level_1_ssecret_room = True

    tiles.set_current_tilemap(tilemap("""
        Level1 Medieval assessmentPlatformer
    """))

    set_level_1_background()
    tiles.place_on_tile(mySprite, tiles.get_tile_location(19, 11))
    scene.camera_follow_sprite(mySprite)

scene.on_overlap_tile(SpriteKind.player, assets.tile("""
    Way out of level 1 secret room
"""), on_secret_room_exit)


def on_enter_secret_room(sprite5, location4):
    global Coin_level_1_secret_room_location_list, coin, ENEMY_ENGAGED
    global Lava_activated_level_1_ssecret_room, lava_active, lava_room_complete

    stop_lava()

    Lava_activated_level_1_ssecret_room = False
    lava_active = False
    lava_room_complete = False

    tiles.set_current_tilemap(tilemap("""
        secret level 1
    """))

    scene.set_background_image(assets.image("""
        Secret room level one
    """))

    tiles.place_on_tile(mySprite, tiles.get_tile_location(1, 30))

    Coin_level_1_secret_room_location_list = tiles.get_tiles_by_type(assets.tile("""
        Coin marker level one in secret room
    """))

    for value in Coin_level_1_secret_room_location_list:
        coin = sprites.create(assets.image("""
            coin1 seret room level 1
        """), SpriteKind.food)

        tiles.place_on_tile(coin, value)
        tiles.set_tile_at(value, assets.tile("""
            transparency16
        """))

        animation.run_image_animation(coin, assets.animation("""
            Coin spinning
        """), 500, True)

    ENEMY_ENGAGED = False

scene.on_overlap_tile(SpriteKind.player, assets.tile("""
    Door to secret level 1
"""), on_enter_secret_room)


def on_a_pressed():
    if mySprite.is_hitting_tile(CollisionDirection.BOTTOM):
        mySprite.vy = -150

controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)


def on_left_pressed():
    global facing_right, facing_left
    mySprite.set_image(assets.image("""
        Main character
    """))
    facing_right = False
    facing_left = True

controller.left.on_event(ControllerButtonEvent.PRESSED, on_left_pressed)


def on_right_pressed():
    global facing_left, facing_right
    mySprite.set_image(assets.image("""
        Main character
    """))
    facing_left = False
    facing_right = True

controller.right.on_event(ControllerButtonEvent.PRESSED, on_right_pressed)


def on_b_pressed():
    global mySprite_attacking

    if HasSword == True:
        mySprite_attacking = True
        pause(500)
        mySprite_attacking = False

controller.B.on_event(ControllerButtonEvent.PRESSED, on_b_pressed)


def on_spike_overlap(sprite, location):
    info.change_life_by(-1)
    tiles.place_on_tile(mySprite, tiles.get_tile_location(0, 10))

scene.on_overlap_tile(SpriteKind.player, assets.tile("""
    Spike
"""), on_spike_overlap)


def spawnEnemies():
    global Generic_swipe_attack_enemy, Enemy_on_level_2_has_spawned

    if HasSword == True and Enemy_on_level_2_has_spawned == False:
        for value2 in tiles.get_tiles_by_type(assets.tile("""
            Danger
        """)):
            Generic_swipe_attack_enemy = sprites.create(assets.image("""
                Bad guy multipe uses
            """), SpriteKind.enemy)

            tiles.place_on_tile(Generic_swipe_attack_enemy, value2)
            tiles.set_tile_at(value2, assets.tile("""
                transparency16
            """))

            Generic_swipe_attack_enemy.ay = 300
            Generic_swipe_attack_enemy.set_velocity(50, 0)

        Enemy_on_level_2_has_spawned = True


def on_level_2_door(sprite3, location3):
    global Bat2

    stop_lava()

    scene.camera_follow_sprite(mySprite)
    scene.set_background_image(assets.image("""
        Level 2 background
    """))

    tiles.set_current_tilemap(tilemap("""
        Level 2 medieval assessmet platformer
    """))

    tiles.place_on_tile(mySprite, tiles.get_tile_location(3, 14))

    Bat2 = sprites.create(assets.image("""
        Bat in cave level 2
    """), SpriteKind.Bat)

    tiles.place_on_random_tile(Bat2, assets.tile("""
        cave cones
    """))

    animation.run_image_animation(Bat2, assets.animation("""
        Bat left
    """), 500, True)

    game.splash("Press 'X' to use your sword!")
    spawnEnemies()

scene.on_overlap_tile(SpriteKind.player, assets.tile("""
    cave right level 1 to levl 2
"""), on_level_2_door)


def on_secret_door_prompt(sprite6, location5):
    global Show_door_diologe_promt_level_one_seceret_door

    if Show_door_diologe_promt_level_one_seceret_door == False:
        game.set_dialog_frame(assets.image("""
            Thought bubble
        """))
        game.show_long_text("I wonder whats in that door???", DialogLayout.TOP)
        Show_door_diologe_promt_level_one_seceret_door = True

scene.on_overlap_tile(SpriteKind.player, assets.tile("""
    Show promt for door on level one
"""), on_secret_door_prompt)


def on_coin_collect(sprite9, otherSprite2):
    if otherSprite2 != Chest:
        info.change_score_by(1)
        sprites.destroy(otherSprite2, effects.confetti, 500)

sprites.on_overlap(SpriteKind.player, SpriteKind.food, on_coin_collect)


def on_enemy_engage(sprite10, location8):
    global myEnemy_start_to_follow_player, ENEMY_ENGAGED
    myEnemy_start_to_follow_player = True
    ENEMY_ENGAGED = True

scene.on_overlap_tile(SpriteKind.player, assets.tile("""
    Enemyengageactivated
"""), on_enemy_engage)


def on_player_enemy_overlap(sprite11, otherSprite3):
    if ENEMY_ENGAGED == True:
        pause(1000)
        info.change_life_by(-1)

sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_player_enemy_overlap)


def on_enemy_hit_wall(sprite7, location6):
    if sprite7.is_hitting_tile(CollisionDirection.LEFT):
        sprite7.set_velocity(50, 0)
        sprite7.set_bounce_on_wall(True)
    elif sprite7.is_hitting_tile(CollisionDirection.RIGHT):
        sprite7.set_velocity(-50, 0)
        sprite7.set_bounce_on_wall(True)
    else:
        sprite7.set_bounce_on_wall(False)

scene.on_hit_wall(SpriteKind.enemy, on_enemy_hit_wall)


info.set_life(5)

set_level_1_background()

tiles.set_current_tilemap(tilemap("""
    Level1 Medieval assessmentPlatformer
"""))

mySprite = sprites.create(assets.image("""
    Main character
"""), SpriteKind.player)

tiles.place_on_tile(mySprite, tiles.get_tile_location(0, 10))
scene.camera_follow_sprite(mySprite)

controller.move_sprite(mySprite, 100, 0)
mySprite.ay = 300

Follower = sprites.create(assets.image("""
    Follower
"""), SpriteKind.Friend)

Follower.follow(mySprite)

Chest = sprites.create(assets.image("""
    Chest
"""), SpriteKind.food)

tiles.place_on_tile(Chest, tiles.get_tile_location(21, 11))

game.show_long_text("Lydia: We must go save the princess!", DialogLayout.BOTTOM)


def on_update_ladders():
    if mySprite.tile_kind_at(TileDirection.CENTER, assets.tile("""
        Ladder
    """)) or mySprite.tile_kind_at(TileDirection.CENTER, assets.tile("""
        sky ladder
    """)):
        if controller.up.is_pressed():
            mySprite.vy = -50
        elif controller.down.is_pressed():
            mySprite.vy = 50
        else:
            mySprite.vy = 0
            mySprite.ay = 0
    else:
        mySprite.ay = 300

game.on_update(on_update_ladders)


def on_update_chest():
    global ChestOpened, HasSword

    if mySprite.overlaps_with(Chest):
        if ChestOpened == False:
            Chest.set_image(assets.image("""
                Open Chest
            """))
            ChestOpened = True
            HasSword = True
            game.splash("You got a Sword")

game.on_update(on_update_chest)


def on_update_enemy_follow():
    if myEnemy_start_to_follow_player == True:
        if Generic_swipe_attack_enemy:
            Generic_swipe_attack_enemy.follow(mySprite, 60)

game.on_update(on_update_enemy_follow)