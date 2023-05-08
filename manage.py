import uvicorn
import typer
from typing import Optional
from core import PROJECT_HOST, PROJECT_PORT


app = typer.Typer()


@app.command()
def runserver(
    host: Optional[str] = PROJECT_HOST,
    port: Optional[int] = PROJECT_PORT,
    reload: Optional[bool] = True
):
    """ Команда для запуска сервера
        >>> python manage.py runserver --host [HOST: по умолчанию 127.0.0.1] --port [PORT: по умолчанию 8000] --reload [RELOAD: по умолчанию True]
    """

    typer.secho(
        message=f"\nЗапуск сервера по адресу: {host}:{port}...\n",
        fg=typer.colors.BRIGHT_GREEN)

    uvicorn.run(
        app="main:app",
        host=host,
        port=port,
        reload=reload)
    
    
if __name__ == "__main__":
    app()