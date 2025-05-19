import os
import flet as ft

def get_file_icon(filename):
    _, ext = os.path.splitext(filename.lower())
    icons = {
        ".exe": "🔴", ".txt": "📄", ".pdf": "📕", ".doc": "📘", ".docx": "📘",
        ".xls": "📗", ".xlsx": "📗", ".ppt": "📙", ".pptx": "📙",
        ".jpg": "🖼️", ".jpeg": "🖼️", ".png": "🖼️", ".gif": "🖼️",
        ".mp3": "🎵", ".mp4": "🎥", ".py": "🐍", ".js": "☕",
        ".html": "🌐", ".css": "🎨", ".zip": "🗜️", ".rar": "🗜️",
    }
    return icons.get(ext, "📄")

def main(page: ft.Page):
    page.title = "Улучшенный проводник файлов"
    page.padding = 20

    current_path = ft.Text()
    files_view = ft.ListView(expand=1, spacing=10)
    path_input = ft.TextField(label="Введите путь", expand=True)

    def update_files(path):
        try:
            path = os.path.abspath(path)
            if not os.path.exists(path):
                raise FileNotFoundError
            
            files_view.controls.clear()
            current_path.value = path
            path_input.value = path

            if path != "/":
                files_view.controls.append(ft.TextButton(text="📂 ..", on_click=lambda _: update_files(os.path.dirname(path))))

            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    files_view.controls.append(
                        ft.TextButton(
                            text=f"📁 {item}",
                            on_click=lambda _, p=full_path: update_files(p)
                        )
                    )
                else:
                    icon = get_file_icon(item)
                    files_view.controls.append(ft.Text(f"{icon} {item}"))

            page.update()
        except PermissionError:
            page.snack_bar = ft.SnackBar(content=ft.Text("Отказано в доступе"))
            page.snack_bar.open = True
            page.update()
        except FileNotFoundError:
            page.snack_bar = ft.SnackBar(content=ft.Text("Путь не найден"))
            page.snack_bar.open = True
            page.update()

    def on_submit(e):
        if e.control.value:
            update_files(e.control.value)

    path_input.on_submit = on_submit

    go_button = ft.ElevatedButton("Перейти", on_click=lambda _: update_files(path_input.value))

    page.add(
        ft.Row([path_input, go_button]),
        current_path,
        files_view
    )

    update_files(os.path.expanduser("~"))

ft.app(target=main)
