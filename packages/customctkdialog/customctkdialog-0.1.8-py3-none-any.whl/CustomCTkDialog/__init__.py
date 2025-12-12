from .electron_loader import ensure_electron

# Trigger download immediately when package loads
ensure_electron()

from .custom_ctk_dialog import Dialog, folder_picker, file_picker, AlertType

__all__ = ["Dialog", "folder_picker", "file_picker", "AlertType"]
