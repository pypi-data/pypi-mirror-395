from pydantic import BaseModel

class PrettyModel(BaseModel):
    def __str__(self):
        try:
            from rich.console import Console
            from rich.syntax import Syntax
            console = Console()
            json_str = self.model_dump_json(indent=2)
            syntax = Syntax(json_str, "json", theme="ansi_dark", line_numbers=False)
            with console.capture() as capture:
                console.print(syntax)
            return capture.get()
        except ImportError:
            # Fallback si rich no está disponible
            return self.model_dump_json(indent=2)
        except Exception as e:
            return str(e)
