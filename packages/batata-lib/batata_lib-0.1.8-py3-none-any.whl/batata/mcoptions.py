import subprocess
import threading
import time
from pathlib import Path

from batata import JSONManager
from batata.aliases import *

__all__ = ['start_server', 'save_servers', 'load_servers', 'list_servers', 'get_server', 'list_mods']


def stream_output(process, prefix="[SERVER]"):
    """Thread que printa output do processo em tempo real"""
    try:
        for line in process.stdout:
            print(f"{prefix} {line}", end="")
    except Exception as e:
        err(f"Erro ao ler output: {e}")


def start_stream_thread(process, prefix):
    """Inicia thread pra printar output"""
    t = threading.Thread(target=stream_output, args=(process, prefix), daemon=True)
    t.start()


def start_server(server_name: str, tipo: str = 'PaperMC', online: bool = False, proxy_type: str = 'BIN',
                 json_path: str = './') -> None:
    """
    Inicia um servidor MineCraft a partir do .jar fornecido.

    :param server_name: O nome do server (salvo no arquivo JSON)
    :param tipo: O tipo do servidor
    :param online: Se o servidor deve rodar em modo online ou offline
    :param proxy_type: O tipo do proxy (binario, .jar, etc)
    :param json_path: Localização do arquivo dos servidores
    :return: None
    """

    server: dict[str, str] = get_server(server_name=server_name, path=json_path)

    if not server:
        err(f'Servidor "{server_name}" não encontrado!')
        return

    # Paths do servidor
    server_path: Path = Path(server['server_path']).expanduser()
    jar_name: str = server.get('jar_name', 'server.jar')
    jar_full_path = server_path / jar_name

    # Verifica se JAR existe
    if not jar_full_path.exists():
        err(f'O arquivo {jar_full_path} não foi encontrado!')
        return

    info(f'Iniciando o servidor {server_name} ({tipo})...')
    info(f'Path: {server_path}')
    info(f'JAR: {jar_name}')

    # Inicia servidor
    server_process = subprocess.Popen(
        [
            'java',
            '-Xmx2048M',  # RAM máxima
            '-Xms2048M',  # RAM inicial
            '-jar',
            str(jar_full_path),
            'nogui'
        ],
        cwd=server_path,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    info(f'Servidor iniciado! PID: {server_process.pid}')
    start_stream_thread(server_process, f"[{tipo}]")

    # Inicia proxy se modo online
    if online:
        proxy_name: str | None = server.get('proxy_name')
        proxy_path_str: str | None = server.get('proxy_path')

        if not proxy_name or not proxy_path_str:
            warn('Proxy não configurado! Servidor rodando sem proxy.')
            warn('Use: mccontroller save <nome> <path> <jar> <proxy_name> <proxy_path>')
            return

        proxy_path: Path = Path(proxy_path_str).expanduser()
        proxy_full_path = proxy_path / proxy_name

        # Verifica se proxy existe
        if not proxy_full_path.exists():
            err(f'Proxy não encontrado: {proxy_full_path}')
            return

        # Espera servidor inicializar um pouco
        time.sleep(5)

        info(f'Iniciando proxy: {proxy_name}')
        info(f'Tipo: {proxy_type}')

        # Remove ponto inicial se tiver (.jar → jar)
        if proxy_type.startswith('.'):
            proxy_type = proxy_type[1:]

        match proxy_type.upper():
            case 'JAR':
                proxy_process = subprocess.Popen(
                    [
                        'java',
                        '-jar',
                        proxy_name
                    ],
                    cwd=proxy_path,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
                info(f'Proxy iniciado! PID: {proxy_process.pid}')
                start_stream_thread(proxy_process, "[PROXY-JAR]")

            case 'BIN' | 'BINARY':
                proxy_process = subprocess.Popen(
                    [str(proxy_full_path)],
                    cwd=proxy_path,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
                info(f'Proxy iniciado! PID: {proxy_process.pid}')
                start_stream_thread(proxy_process, "[PROXY-BIN]")

            case _:
                err(f'Tipo de proxy "{proxy_type}" não suportado!')
                err('Tipos válidos: JAR, BIN')
                return

    # Keep-alive: espera servidor terminar
    info('\n✅ Servidor e proxy rodando!')
    info('Pressione Ctrl+C para parar\n')

    try:
        # Fica esperando o servidor terminar
        server_process.wait()
    except KeyboardInterrupt:
        info('\n\n⚠️  Parando servidor...')

        # Para servidor
        server_process.terminate()
        try:
            server_process.wait(timeout=10)
            info('Servidor parado!')
        except:
            warn('Servidor não respondeu, forçando parada...')
            server_process.kill()

        # Para proxy se tiver
        if online and 'proxy_process' in locals():
            info('Parando proxy...')
            proxy_process.terminate()
            try:
                proxy_process.wait(timeout=5)
                info('Proxy parado!')
            except:
                proxy_process.kill()

        info('✅ Tudo parado!')


def save_servers(
        server_name: str,
        server_path: str,
        jar_name: str,
        proxy_name: str | None = None,
        proxy_path: str | None = None,
        arquivo: str = 'servers.json',
        path: str = './'
) -> None:
    """
    Salva as informações do servidor num arquivo JSON.

    :param server_name: O nome do servidor
    :param server_path: O caminho do servidor
    :param jar_name: Nome do arquivo JAR
    :param proxy_name: O nome do proxy (opcional)
    :param proxy_path: O caminho do proxy (opcional)
    :param arquivo: O arquivo para salvar (padrão: 'servers.json')
    :param path: O caminho onde salvar (padrão: './')
    :return: None
    """
    manager: JSONManager = JSONManager(
        path=path,
        name=arquivo,
        indent=2,
    )

    # Valida se server já existe
    servers = manager.read()
    for server in servers:
        if server.get('server_name') == server_name:
            warn(f'Servidor "{server_name}" já existe! Sobrescrevendo...')
            # TO-DO: implementar update ao invés de duplicar
            break

    manager.write({
        'server_name': server_name,
        'server_path': server_path,
        'jar_name': jar_name,
        'proxy_name': proxy_name,
        'proxy_path': proxy_path,
    })

    info(f'Servidor "{server_name}" salvo com sucesso!')
    info(f'  Path: {server_path}')
    info(f'  JAR: {jar_name}')
    if proxy_name:
        info(f'  Proxy: {proxy_name} ({proxy_path})')


def load_servers(arquivo: str = 'servers.json', path: str = './') -> list[dict[str, str]]:
    """
    Carrega as informações dos servidores de um arquivo JSON.

    :param arquivo: O arquivo de onde carregar (padrão: 'servers.json')
    :param path: O caminho para o arquivo (padrão: './')
    :return: Lista de servidores
    """
    manager: JSONManager = JSONManager(
        path=path,
        name=arquivo,
        indent=2,
    )

    try:
        return manager.read()
    except:
        warn('Nenhum servidor encontrado. Use "save" para adicionar.')
        return []


def list_servers(arquivo: str = 'servers.json', path: str = './') -> list[dict[str, str]]:
    """
    Lista as informações dos servidores salvos.

    :param arquivo: O arquivo de onde carregar (padrão: 'servers.json')
    :param path: O caminho para o arquivo (padrão: './')
    :return: Lista de servidores
    """
    servers: list[dict[str, str]] = load_servers(arquivo=arquivo, path=path)

    if not servers:
        warn('Nenhum servidor salvo encontrado.')
        return []

    out('\n📋 Servidores cadastrados:\n')
    for server in servers:
        name = server.get('server_name', '???')
        path = server.get('server_path', '???')
        jar = server.get('jar_name', '???')
        proxy = server.get('proxy_name', 'Nenhum')

        print(f'  • {name}')
        print(f'    Path: {path}')
        print(f'    JAR: {jar}')
        print(f'    Proxy: {proxy}')
        print()

    return servers


def list_mods(server_path: str, server_config_path: str, server: str) -> list[str]:
    mods: list[str] = []
    server = get_server(path=server_config_path, server_name=server)
    mods_path = Path(server['server_path']).expanduser() / 'mods'

    for mod in mods_path.iterdir():
        if mod.name != '.DS_Store':
            mods.append(mod.name)

    return mods


def get_server(server_name: str, path: str = './') -> dict[str, str]:
    """
    Busca servidor por nome

    :param server_name: Nome do servidor
    :param path: O caminho do servidor
    :return: Dicionário com dados do servidor ou vazio
    """
    servers: list[dict[str, str]] = load_servers(arquivo='servers.json', path=path)

    for server in servers:
        if server.get('server_name') == server_name:
            return server

    warn(f'Servidor "{server_name}" não encontrado.')
    return {}


if __name__ == '__main__':
    SERVERS_PATH = str(Path('~/Desktop/Coisas Do Decaptado/Mine Server/').expanduser())
    SERVERS_CONFIGS = str(Path('~/Desktop/Coisas Do Decaptado/MineServer-Controller/').expanduser())

    print(list_mods(server_path=SERVERS_PATH, server_config_path=SERVERS_CONFIGS, server='Survivors'))
