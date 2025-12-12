from importlib.metadata import version

__version__ = version("netmagus")
__all__ = ["form", "rpc", "screen", "session"]
from .form import (  # noqa: F401
    CheckBox,
    DropDownMenu,
    FileDownloadLink,
    FilesUpload,
    Form,
    PasswordInput,
    RadioButton,
    SelectDrop,
    TextArea,
    TextInput,
)
from .rpc import (  # noqa: F401
    Html,
    rpc_connect,
    rpc_disconnect,
    rpc_form_query,
    rpc_receive,
    rpc_send,
)
from .screen import BackButtonPressed, CancelButtonPressed, ScreenBase  # noqa: F401
from .session import NetMagusSession  # noqa: F401
