from typing import Sequence as _Sequence

from charz import (
    Screen as _Screen,
    Camera as _Camera,
    TextureComponent as _TextureComponent,
)

def render_all(
    screen: _Screen,
    nodes: _Sequence[_TextureComponent],
    camera: _Camera,
    camera_centering_x: float,
    camera_centering_y: float,
    use_color: bool,
) -> str: ...
