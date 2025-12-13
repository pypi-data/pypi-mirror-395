import hashlib
import os
import re
import sys
from typing import Final

import httpx
import web
from tqdm import tqdm


class Downloader:
    @staticmethod
    def _get_file_path(
            url: str,
            headers: dict[str, str] | None = None,
            file_path: str | None = None,
            dir_path: str | None = None,
            file_name: str | None = None,
            file_prefix: str | None = None,
            file_suffix: str | None = None
    ) -> str:
        """

        Args:
            url:
            headers: response.headers
            file_path: dir_path + file_name
            dir_path:
            file_name: file_prefix + file_suffix
            file_prefix:
            file_suffix:

        Returns:

        """
        # todo：Add more content_type.
        content_type_to_file_ext: Final[dict[str, str]] = {
            "image/png": "png",
            "image/gif": "gif",
            "text/html;charset=utf-8": "html",
            "text/javascript; charset=utf-8": "js",
            "application/json; charset=utf-8": "json",
            "image/jpeg;charset=UTF-8": "jpeg",
            "text/html; charset=utf-8": "html",
        }

        if file_path is None:
            if dir_path is None:
                dir_path = os.path.dirname(os.path.abspath(sys.argv[0]))
            else:
                dir_path = os.path.abspath(dir_path)
            if file_name is None:
                if not (file_prefix is not None and file_suffix is not None):
                    _file_name: str | None = None
                    if _file_name is None:
                        if (content_disposition := headers.get("content-disposition")) is not None:
                            m = re.match(r'attachment;fileName="(.*?)"', content_disposition)
                            if m:
                                _file_name = m.group(1)
                                _file_name = _file_name.replace("/", "_")
                    if _file_name is None:
                        _file_prefix, _file_suffix = os.path.splitext(web.url.get_furl_obj(url).path.segments[-1])
                        if not _file_prefix:
                            _file_prefix = web.url.get_furl_obj(url).host
                        if not _file_suffix:
                            if (content_type := headers.get("content-type")) is not None:
                                _file_ext = content_type_to_file_ext[content_type]
                                _file_suffix = os.path.extsep + _file_ext
                                _file_name = _file_prefix + _file_suffix
                        else:
                            _file_name = _file_prefix + _file_suffix
                    if _file_name is None:
                        _file_name = hashlib.sha256(url.encode()).hexdigest() + os.path.extsep + "bin"

                    if file_prefix is None:
                        file_prefix = os.path.splitext(_file_name)[0]
                    if file_suffix is None:
                        file_suffix = os.path.splitext(_file_name)[-1]

                file_name = file_prefix + file_suffix
            else:
                file_name = os.path.basename(file_name)
            file_path = os.path.join(dir_path, file_name)
        else:
            file_path = os.path.abspath(file_path)

        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        return file_path

    def download(
            self,
            url: str,
            headers: dict[str, str] | None = None,
            file_path: str | None = None,
            dir_path: str | None = None,
            file_name: str | None = None,
            file_prefix: str | None = None,
            file_suffix: str | None = None,
            use_cache: bool = True,
            chunk_size: int = 64 * 1024,
            use_tqdm: bool = False
    ) -> str | None:
        if not web.url.is_valid(url):
            return None

        if headers is None:
            headers = web.headers.get_default()

        try:
            with httpx.Client(timeout=None, follow_redirects=True) as client:
                with client.stream("GET", url, headers=headers) as response:
                    response.raise_for_status()

                    file_path = self._get_file_path(
                        url, response.headers,
                        file_path,
                        dir_path, file_name,
                        file_prefix, file_suffix
                    )

                    if use_cache:
                        if os.path.exists(file_path):
                            return file_path

                    total = int(response.headers.get("content-length", 0))
                    progress: tqdm | None = None

                    if use_tqdm:
                        progress = tqdm(
                            total=total,
                            unit="B",
                            unit_scale=True,
                            unit_divisor=1024,
                            desc=file_path.split("/")[-1],
                            bar_format="{l_bar}{bar} | {n_fmt}/{total_fmt} | {rate_fmt} | ETA {remaining}",
                        )

                    with open(file_path, "wb") as file:
                        for chunk in response.iter_bytes(chunk_size=chunk_size):
                            file.write(chunk)
                            if progress is not None:
                                progress.update(len(chunk))

                    if progress is not None:
                        progress.close()
        except Exception as e:  # noqa
            file_path = None

        return file_path


__all__ = ["Downloader"]
