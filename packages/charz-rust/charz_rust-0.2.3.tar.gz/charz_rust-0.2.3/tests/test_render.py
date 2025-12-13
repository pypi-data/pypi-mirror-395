from charz import Screen, Camera, Sprite, Vec2
from charz_rust._core import render_all


EXPECTED = "#####     \n#@@##     \n @@       \n          \n          \n          \n          \n          "


def test_render_working() -> None:
    class TestBoxA(Sprite):
        texture = [
            "#####",
            "#####",
        ]

    class TestBoxB(Sprite):
        texture = [
            "@@",
            "@@",
        ]

    test_screen = Screen(
        width=10,
        height=8,
        color_choice=Screen.COLOR_CHOICE_NEVER,
        initial_clear=False,
        final_clear=False,
    )
    test_boxes = [
        TestBoxA(position=Vec2.ZERO),
        TestBoxB(position=Vec2.ONE),
    ]
    test_camera = Camera()

    result = render_all(
        test_screen,
        test_boxes,
        test_camera,
        camera_centering_x=0,
        camera_centering_y=0,
        use_color=False,
    )
    print("\n---")
    print(result)
    print("---")
    assert result == EXPECTED
