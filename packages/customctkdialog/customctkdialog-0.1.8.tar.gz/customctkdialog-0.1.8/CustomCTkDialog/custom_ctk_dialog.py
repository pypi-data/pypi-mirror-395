from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton, CTkFrame, CTkFont, set_appearance_mode # type: ignore
from typing import Dict, Optional, List, cast
from tkinter import PhotoImage, Tk, filedialog
from pathlib import Path
from enum import Enum
import subprocess
import time
import json
import os

MIN_WINDOW_WIDTH: int = 500
DEFAULT_WINDOW_HEIGHT: int = 150
BUTTON_SPACING: int = 10

PACKAGE_DIR: Path = Path(__file__).parent
EXE_PATH: str = str(PACKAGE_DIR / "folder-picker.exe")

class AlertType(Enum):
    """
    Types of alerts for visual differentiation.
    
    >>> AlertType.INFO: # Informational alert.
    >>> AlertType.SUCCESS: # Success alert.
    >>> AlertType.WARNING: # Warning alert.
    >>> AlertType.ERROR: # Error alert.
    """
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"

def folder_picker(
    initialdir: Optional[str] = None,
    return_full_paths: bool = True,
    title: Optional[str] = None,
    multi_folder: bool = True
) -> List[str]:
    """
    Runs the external multi-folder picking utility and returns selected folder paths.

    Arguments
    ------------
    initialdir (str | None): Initial directory path for the picker dialog.
    return_full_paths (bool): Whether to return full folder paths.
    title (str | None): Title of the picker dialog window.
    multi_folder (bool): Whether multiple folder selection is allowed.

    Returns
    ---------
    selected_paths (List[str]): List of selected folder paths.
    """
    command: List[str] = [EXE_PATH]

    if initialdir:
        command.append(f'--default_path={initialdir}')

    command.append(f"--return_full_paths={str(return_full_paths).lower()}")

    if title:
        command.append(f'--title={title}')

    command.append(f"--multi-folder={str(multi_folder).lower()}")

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)  

        if result.stderr:
            print("--- Picker STDERR ---\n", result.stderr.strip(), "\n---------------------")            
        
        json_output: str = result.stdout.strip()  

        if not json_output:
            return []      
              
        parsed = json.loads(json_output)
        return parsed if isinstance(parsed, list) else []

    except FileNotFoundError:
        print(f"Picker EXE not found at {EXE_PATH}.")
        return []

    except subprocess.CalledProcessError as error:
        print(f"Error running folder picker: {error.stderr.strip() if error.stderr else error}")
        return []

    except json.JSONDecodeError:
        print("Picker output was not valid JSON.")
        return []

def file_picker(
    initialdir: str = os.getcwd(),
    title: str = "Select Files",
    return_full_paths: bool = True,
    preferred_icon_path: Optional[str] = None # Added optional argument
) -> List[str]:
    """
    A wrapper around tkinter's filedialog to pick one or more files.
    Opens a file picker dialog and returns a list of selected file paths or names.

    Arguments
    ---------
        initialdir (str): The initial directory the dialog opens to.
        title (str): The title of the file picker window.
        return_full_paths (bool): If True, returns full paths. If False, returns only the base filename (basename).
        preferred_icon_path (Optional[str]): Path to a .png or .gif image file to use as the window icon.

    Returns
    -------
        List[str] - files chosen by the user, or [] if cancelled.
    """
    root: Tk = Tk()

    if preferred_icon_path:
        try:
            icon = PhotoImage(file=preferred_icon_path)
            root.iconphoto(True, icon)
        except Exception as error:
            # Handle cases where the file doesn't exist or is an unsupported format
            print(f"Warning: Could not set icon from path '{preferred_icon_path}'. Error: {error}")

    root.withdraw()

    file_paths_tuple = filedialog.askopenfilenames(
        initialdir=initialdir,
        title=title,
    )        
    root.destroy()

    file_paths = list(file_paths_tuple)

    if not file_paths:
        return []

    return file_paths if return_full_paths else [os.path.basename(path) for path in file_paths]
        
class Dialog:

    _app: Optional[CTk] = None

    @classmethod
    def _ensure_app(cls) -> CTk:
        """
        Ensure a single CTk app exists and return it.
        The app is created once and persists for the lifetime of the module.
        It is initially withdrawn (hidden) until a dialog is shown.
        """
        if cls._app is None:
            cls._app = CTk()
            cls._app.withdraw()
            cls._app.resizable(0, 0)
            cls._app.title("Application")
            set_appearance_mode("Dark")

            def _on_close():
                try:
                    cls._clear_app_widgets()
                finally:
                    cls._app.withdraw()

            cls._app.protocol("WM_DELETE_WINDOW", _on_close)

        return cls._app

    @classmethod
    def _clear_app_widgets(cls) -> None:
        """
        Remove all children widgets from the persistent app.
        We destroy them so next dialog draws fresh content into the same app window.
        """
        if cls._app is None:
            return
        
        for child in cls._app.winfo_children():
            try:
                child.destroy()
            except Exception:
                pass

    @staticmethod
    def _center_app(app: CTk, dialog_width: int, dialog_height: int) -> None:
        """
        Centers the given app window on the screen with specified width and height.

        Arguments
        ---------
            app (CTk): The CTk application window to center.
            dialog_width (int): The width of the dialog window.
            dialog_height (int): The height of the dialog window.
        """
        screen_width, screen_height = app.winfo_screenwidth(), app.winfo_screenheight()
        center_x: int = int(screen_width / 2 - dialog_width / 2)
        center_y: int = int(screen_height / 2 - dialog_height / 2)
        app.geometry(f"{dialog_width}x{dialog_height}+{center_x}+{center_y}")

    @staticmethod
    def _modal_wait_until_set(flag_container: dict, key: str, app: CTk, poll_interval: float = 0.01) -> None:
        """
        Simple modal wait: process tkinter events until flag_container[key] is set (not None).
        This allows the function to behave synchronously (blocking) while still updating the UI.

        Arguments
        ---------
            flag_container (dict): A dictionary to hold the flag value.
            key (str): The key in the dictionary to monitor.
            app (CTk): The CTk application window to update.
            poll_interval (float): Time in seconds between UI updates.
        """
        app.deiconify() # ensure visible / focused
        app.lift()
        app.focus_force()

        while flag_container.get(key, None) is None:
            try:
                app.update()
                time.sleep(poll_interval)
            except Exception:
                break

    @staticmethod
    def _apply_window_icon(app: CTk, window_icon_path: Optional[str]):
        """
        Apply a temporary window icon for the current dialog.
        Returns a restore() function that will revert to the previous icon.

        Arguments
        ---------
            app (CTk): The root application window.
            window_icon_path (Optional[str]): Path to .ico file for iconbitmap.

        Returns
        -------
            Callable[[], None]: A function that restores the previous icon.
        """
        if not window_icon_path:
            return lambda: None
        try:
            previous_icon = app.winfo_iconbitmap()
        except Exception:
            previous_icon = None
        try:
            app.iconbitmap(window_icon_path)
        except Exception:
            return lambda: None
        def restore():
            try:
                if previous_icon:
                    app.iconbitmap(previous_icon)
                else:
                    app.iconbitmap("")
            except Exception:
                pass
        return restore

    @classmethod
    def _base_input_dialog(
        cls,
        message: str,
        *,
        is_input: bool = True,
        default_text: str = "",
        confirm_text: str = "Confirm",
        cancel_text: str = "Cancel",
        window_title: Optional[str] = None,
        width: int = MIN_WINDOW_WIDTH,
        height: int = 180,
        window_icon_path: Optional[str] = None,
    ) -> Optional[object]:
        """
        Shared private helper for input-like dialogs.

        - If is_input == True: treat as 'prompt' -> returns string or raises ValueError if canceled/empty.
        - If is_input == False: treat as 'confirm' -> returns bool (True for Confirm/Yes, False otherwise).

        This uses the persistent CTk app: draws widgets into it, waits for user action,
        then clears widgets and hides the app (but does not destroy it).

        Arguments
        ---------
            message (str): The message to display in the dialog.
            is_input (bool): If True, treat as input prompt; if False, treat as confirm dialog.
            default_text (str): Default text for input dialogs.
            confirm_text (str): Text for the confirm button.
            cancel_text (str): Text for the cancel button.
            window_title (Optional[str]): Title of the dialog window.
            width (int): Width of the dialog window.
            height (int): Height of the dialog window.
            window_icon_path (Optional[str]): Path to .ico (or other acceptable) file passed to root.iconbitmap.
                If provided, the existing icon will be saved (if possible) and
                restored after the dialog finishes.

        Returns
        -------
            Optional[object]: For input dialogs, returns str; for confirm dialogs, returns bool.
        """
        if not message:
            raise ValueError("A message must be provided for input dialogs.")

        app = cls._ensure_app()
        cls._clear_app_widgets()
        restore_icon = cls._apply_window_icon(app, window_icon_path)

        if window_title:
            app.title(window_title)

        cls._center_app(app, width, height)
        app.grid_rowconfigure(0, weight=0)
        app.grid_rowconfigure(1, weight=1)
        app.grid_rowconfigure(2, weight=0)
        app.grid_columnconfigure(0, weight=1)

        result_container: Dict[str, Optional[bool]] = {"value": None}

        def _do_cancel() -> None:
            result_container["value"] = None if is_input else False
            return

        def _do_confirm() -> None:
            if is_input and entry:
                value = entry.get().strip()
                result_container["value"] = value if value else None
            else:
                result_container["value"] = True

        message_label = CTkLabel(app, text=message, font=CTkFont(size=14),
                                 wraplength=width - 40, justify="left")
        message_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nw")

        entry: Optional[CTkEntry] = None
        if is_input:
            entry = CTkEntry(app, placeholder_text="Enter your required input here...", font=CTkFont(size=14))
            entry.insert(0, default_text)
            entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        button_frame = CTkFrame(app, fg_color="transparent")
        button_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="se")
        button_frame.grid_columnconfigure((0, 1), weight=0)

        CTkButton(button_frame, text=cancel_text, command=_do_cancel).grid(row=0, column=0, padx=(0, BUTTON_SPACING), sticky="e")
        CTkButton(button_frame, text=confirm_text, command=_do_confirm).grid(row=0, column=1, sticky="e")

        app.bind("<Return>", lambda e=None: _do_confirm())
        app.bind("<Escape>", lambda e=None: _do_cancel())
        if entry:
            entry.focus_set()

        cls._modal_wait_until_set(result_container, "value", app)
        restore_icon()
        try:
            app.unbind("<Return>")
            app.unbind("<Escape>")
        except Exception:
            pass
        cls._clear_app_widgets()
        app.withdraw()

        value = result_container.get("value", None)
        if is_input:
            if value is None:
                raise ValueError("Input required: Dialog was canceled or blank.")
            return value
        return bool(value)

    @classmethod
    def prompt(cls, message: str, default_text: str = "") -> str:
        """
        Show a prompt dialog to get text input from the user.
        Returns the entered non-empty string. Raises ValueError if canceled or blank.

        Arguments
        ---------
            message (str): The message to display in the prompt dialog.
            default_text (str): Default text to pre-fill in the input field.

        Returns
        -------
            str: The non-empty string entered by the user.
        """
        return cast(str, cls._base_input_dialog(
                message, is_input=True, default_text=default_text,
                confirm_text="Confirm", cancel_text="Cancel",
                window_title="Input Required"
            )
        )

    @classmethod
    def confirm(cls, message: str) -> bool:
        """
        Show a confirm (yes/no) dialog. Returns True if user confirmed, False otherwise.

        Arguments
        ---------
            message (str): The message to display in the confirm dialog.

        Returns
        -------
            bool: True if user clicked Confirm/Yes, False if Cancel/No.
        """
        return cast(bool, cls._base_input_dialog(
                message, is_input=False,
                confirm_text="Yes", cancel_text="No",
                window_title="Confirm", height=150
            )
        )

    @classmethod
    def _base_alert_dialog(
        cls,
        title: Optional[str],
        message: str,
        *,
        icon: Optional[str] = None,
        kind: AlertType = AlertType.INFO,
        width: int = MIN_WINDOW_WIDTH,
        height: int = 150,
    ) -> None:
        """
        Base alert dialog: draws message + single dismiss/ok button.
        Accepts an AlertType to differentiate visuals. Icon can be a simple string (emoji) or None.

        Arguments
        ---------
            title (Optional[str]): Title of the alert dialog window.
            message (str): The alert message to display.
            icon (Optional[str]): Optional icon (string/emoji) to display alongside the message.
            kind (AlertType): The type of alert for visual differentiation.
            width (int): Width of the dialog window.
            height (int): Height of the dialog window.
        """
        if message is None:
            raise ValueError("Alert message must be provided.")

        app = cls._ensure_app()
        cls._clear_app_widgets()
        app.title(title or kind.name.title())
        cls._center_app(app, width, height)

        default_icons = {AlertType.INFO: "ℹ️", AlertType.SUCCESS: "✅", AlertType.WARNING: "⚠️", AlertType.ERROR: "❌"}
        display_icon = icon if icon is not None else default_icons.get(kind, "")

        top_frame = CTkFrame(app, fg_color="transparent")
        top_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nw")
        top_frame.grid_columnconfigure(0, weight=0)
        top_frame.grid_columnconfigure(1, weight=1)

        if display_icon:
            CTkLabel(top_frame, text=display_icon, font=CTkFont(size=24)).grid(row=0, column=0, padx=(0, 10), sticky="nw")
        CTkLabel(top_frame, text=message, font=CTkFont(size=14), wraplength=width-120, justify="left").grid(row=0, column=1, sticky="nw")

        button_frame = CTkFrame(app, fg_color="transparent")
        button_frame.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="se")
        button_frame.grid_columnconfigure((0,), weight=1)

        result_container: Dict[str, Optional[bool]] = {"value": None}
        def _dismiss(): result_container["value"] = True
        CTkButton(button_frame, text="OK", command=_dismiss).grid(row=0, column=0, sticky="e")

        app.bind("<Return>", lambda e=None: _dismiss())
        app.bind("<Escape>", lambda e=None: _dismiss())

        cls._modal_wait_until_set(result_container, "value", app)

        try:
            app.unbind("<Return>")
            app.unbind("<Escape>")
        except Exception:
            pass
        cls._clear_app_widgets()
        app.withdraw()

    @classmethod
    def alert(cls, kind: AlertType, title: Optional[str], message: str, icon: Optional[str] = None) -> None:
        """
        Public alert helper. Example usage:
            alert(AlertType.WARNING, "Low Disk Space", "Only 2GB left", icon="⚠️")

        Arguments
        ---------
            kind (AlertType): The type of alert for visual differentiation.
            title (Optional[str]): Title of the alert dialog window.
            message (str): The alert message to display.
            icon (Optional[str]): Optional icon (string/emoji) to display alongside the message.
        """
        cls._base_alert_dialog(title, message, icon=icon, kind=kind)
    