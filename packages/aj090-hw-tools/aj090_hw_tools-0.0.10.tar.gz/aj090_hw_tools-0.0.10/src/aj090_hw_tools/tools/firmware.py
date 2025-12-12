__all__ = [
    'firmware'
]

import os
import asyncio
import aiohttp
import logging
import re
import esptool
import numpy as np
import tempfile

from aiofile import async_open
from aioconsole import aprint, ainput
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Any, Optional, Dict, Type, NamedTuple
from esptool.cmds import detect_chip
from pathlib import Path

FIRMWARE_PATTERN = {
    "cell" : r'aj090_cell_controller_firmware_(\w{7}).bin',
    "shelf": r'aj090_shelf_controller_firmware_(\w{7}).bin'
}

# Logger 
FORMAT = '%(name)s:%(levelname)s: %(message)s'
logging.basicConfig(level=logging.ERROR, format=FORMAT)
logger = logging.getLogger(__name__)


class GitHubReleaseManager(AbstractAsyncContextManager):
    """
    """
    API_VERSION = '2022-11-28'

    class GitHubError(Exception):
        pass

    def __init__(
        self, 
        repo_owner: str, 
        repo: str, 
        *, 
        token: str
    ):
        self._repo_owner: str = repo_owner
        self._repo: str = repo
        self._token: str = token
        self._session: Optional[aiohttp.ClientSession] = None
          
    async def latest_release_info_get(self) -> Dict[str, Any]:
        """
        curl -L -H "Accept: application/vnd.github+json" \
            -H "Authorization:Bearer github_pat_11BGD5X..." \
            -H "X-GitHub-Api-Version: 2022-11-28" \
                https://api.github.com/repos/owner/repo/releases/latest
        """
        async with self._session.get(
                url     = f'https://api.github.com/repos/{self._repo_owner}/{self._repo}/releases/latest',
                headers = {
                    'Accept': 'application/vnd.github+json',
                }
            ) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                raise self.GitHubError('Release not found')

    async def asset_download(self, asset_download_url: str, output_file: str) -> int:
        """
        returns downloaded asset size in bytes
        """
        async with self._session.get(
            url     = asset_download_url,
            headers = {
                'Accept': 'application/octet-stream'
            }
        ) as response:
            if response.status == 200:
                async with async_open(output_file, 'wb') as output_file:
                    chunk_size = 4096
                    asset_size = 0
                    async for data in response.content.iter_chunked(chunk_size):
                        asset_size += await output_file.write(data)
                    return asset_size
            else:
               raise self.GitHubError('Asset download failed') 
    
    async def __aenter__(self) -> None:
        loop = asyncio.get_running_loop()
        self._session: aiohttp.ClientSession = aiohttp.ClientSession(
            loop    = loop,
            headers = {
                'Authorization'       : f'Bearer {self._token}',
                'X-GitHub-Api-Version': self.API_VERSION
            }
        )
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        await self._session.close()
        return None

class FirmwareInfo(NamedTuple):
    version: str
    project: str
    build_time: str
    build_date: str
    idf: str
    sha: str

class Firmware():
    """
    """
    def __init__(self, port: Optional[str] = None):
        self._port: str = port if port is not None else esptool.ESPLoader.DEFAULT_PORT

    @staticmethod
    async def info(firmware_file: str) -> FirmwareInfo:
        """
            typedef struct {
                uint32_t magic_word;        /*!< Magic word ESP_APP_DESC_MAGIC_WORD */
                uint32_t secure_version;    /*!< Secure version */
                uint32_t reserv1[2];        /*!< reserv1 */
                char version[32];           /*!< Application version */
                char project_name[32];      /*!< Project name */
                char time[16];              /*!< Compile time */
                char date[16];              /*!< Compile date*/
                char idf_ver[32];           /*!< Version IDF */
                uint8_t app_elf_sha256[32]; /*!< sha256 of elf file */
                uint16_t min_efuse_blk_rev_full; /*!< Minimal eFuse block revision supported by image, in format: major * 100 + minor */
                uint16_t max_efuse_blk_rev_full; /*!< Maximal eFuse block revision supported by image, in format: major * 100 + minor */
                uint8_t mmu_page_size;      /*!< MMU page size in log base 2 format */
                uint8_t reserv3[3];         /*!< reserv3 */
                uint32_t reserv2[18];       /*!< reserv2 */
            } esp_app_desc_t;
        """
        INFO_OFFSET = 262144 + 32

        esp_app_desc_t = np.dtype([
            ('magic_word', '<u4'),
            ('secure_version', '<u4'),
            ('reserv1', '<u4', (2,)),
            ('version', '<u1', (32,)),
            ('project_name', '<u1', (32,)),
            ('time', '<u1', (16,)),
            ('date', '<u1', (16,)),
            ('idf_ver', '<u1', (32,)),
            ('app_elf_sha256', '<u1', (32,)),
            ('min_efuse_blk_rev_full', '<u2'),
            ('max_efuse_blk_rev_full', '<u2'),
            ('reserv3', '<u1', (3,)),
            ('reserv2', '<u4', (18,)),
        ])

        async with async_open(firmware_file, 'rb') as file:
            file.seek(INFO_OFFSET)
            b = await file.read(esp_app_desc_t.itemsize)

        app_desc = np.frombuffer(b, esp_app_desc_t)
        sha      = ''.join([f'{d:02x}' for d in app_desc['app_elf_sha256'].tobytes()])
        def to_str(nd_array):
            return nd_array.tobytes().decode().rstrip('\x00')

        return FirmwareInfo(
            version    = to_str(app_desc['version']),
            project    = to_str(app_desc['project_name']),
            build_time = to_str(app_desc['time']),
            build_date = to_str(app_desc['date']),
            idf        = to_str(app_desc['idf_ver']),
            sha        = sha
        )

    async def write(self, firmware: str) -> None:
        def _write():
            with detect_chip(port=self._port, connect_attempts=0) as esp:
                command = ['write_flash', '0', f'{firmware}']
                logger.debug("Using command ", " ".join(command))
                esptool.main(command, esp)

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, _write)    
        
    async def erase(self) -> None:
        def _erase():
            with detect_chip(port=self._port, connect_attempts=0) as esp:
                command = ['erase_flash']
                logger.debug("Using command ", " ".join(command))
                esptool.main(command, esp)

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, _erase)  


async def firmware_flasher(argv):
    """
    """
    # Create FirmwareFlasher
    firmware = Firmware(argv.port)

    match argv.operation:
        case 'write':
            # Download the firmware from GitHub if the bin_file was not passed directly to the arguments.
            if argv.bin_file is None:
                gh_token = os.getenv('AJ090_FWU_TOKEN', None)
                fw_owner = os.getenv('AJ090_FWU_OWNER', 'Vasencheg-AJPT')
                fw_repo  = os.getenv('AJ090_FWU_REPO', 'aj090_firmware')

                if gh_token is None:
                    await aprint('There is no token for accessing the firmware repository!!!')
                    return -1

                try:
                    async with GitHubReleaseManager(fw_owner, fw_repo, token=gh_token) as github:
                        info       = await github.latest_release_info_get()
                        assets     = info['assets']
                        commit_sha = info['target_commitish']
                        result     = list(filter(lambda i: re.match(FIRMWARE_PATTERN[argv.device], i['name']), assets))
                        # validate result
                        if len(result):
                            firmware_info = {
                                'version': commit_sha[:7],
                                'url'    : result[0]['url'],
                                'name'   : result[0]['name']
                            }
                            
                            fwu_file = str(Path(tempfile.gettempdir()).joinpath(firmware_info['name']))

                            if not os.path.exists(fwu_file):
                                await aprint('The latest firmware version is being downloaded...')
                                await github.asset_download(firmware_info['url'], fwu_file)
                            else:
                                await aprint('A cached firmware file is being used...')
                            
                            bin_file = fwu_file
                        else:
                            await aprint('No firmware found')
                            return -1
                except GitHubReleaseManager.GitHubError as err:
                    await aprint(f'An error occured: {err}')
                    # TODO: search for cached firmwares and flash it
                    return -1
            else:
                await aprint('A local firmware file is being used...')
                bin_file = argv.bin_file

            # Get firmware info
            fw_info = await Firmware.info(bin_file)

            await aprint(
"""Firmware information:
    version     : {version}
    build time  : {build_time}
    build date  : {build_date}
    SHA         : {sha}
""".format(version=fw_info.version, build_time=fw_info.build_time, build_date=fw_info.build_date, sha=fw_info.sha)
            )

            operation = firmware.write(bin_file)
       
        case 'erase':
            operation = firmware.erase()

        case _:
            raise Exception('Unsupported flash operation')

    try:
        await ainput('Press Any key to continue or Ctrl^C to abort operation: ')
        await operation
    except asyncio.CancelledError:
        await aprint('\r\n')
        await aprint('Operation aborted')
        operation.close()
        return -1
    except Exception as ex:
        await aprint(f'An unexpected exception occured: {ex}')
        return -1
    else:
        await aprint('DONE!')
        
    return 0


def firmware(argv) -> int:
    return asyncio.run(firmware_flasher(argv))