import asyncio
import os
import re
import datetime
from typing import Iterator, Literal
from collections import defaultdict
from itertools import chain
from heapq import merge
from operator import itemgetter
import binascii
import logging
from tempfile import TemporaryDirectory

import aiohttp
import bgpkit
from bgpkit.bgpkit_broker import BrokerItem

from pybgpkitstream.bgpstreamconfig import BGPStreamConfig
from pybgpkitstream.bgpelement import BGPElement


logger = logging.getLogger(__name__)


def convert_bgpkit_elem(element, is_rib: bool, collector: str) -> BGPElement:
    """Convert pybgpkit element to pybgpstream-like element"""
    return BGPElement(
        type="R" if is_rib else element.elem_type,
        collector=collector,
        time=element.timestamp,
        peer_asn=element.peer_asn,
        peer_address=element.peer_ip,
        fields={
            "next-hop": element.next_hop,
            "as-path": element.as_path,
            "communities": [] if not element.communities else element.communities,
            "prefix": element.prefix,
        },
    )


def crc32(input_str: str):
    input_bytes = input_str.encode("utf-8")
    crc = binascii.crc32(input_bytes) & 0xFFFFFFFF
    return f"{crc:08x}"


class Directory:
    """Permanent directory that mimics TemporaryDirectory interface."""

    def __init__(self, path):
        self.name = str(path)

    def cleanup(self):
        """No-op cleanup for permanent directories."""
        pass


class BGPKITStream:
    def __init__(
        self,
        ts_start: float,
        ts_end: float,
        collector_id: str,
        data_type: list[Literal["update", "rib"]],
        cache_dir: str | None,
        filters: dict = {},
        max_concurrent_downloads: int = 10,
        chunk_time: float | None = datetime.timedelta(hours=2).seconds,
    ):
        self.ts_start = ts_start
        self.ts_end = ts_end
        self.collector_id = collector_id
        self.data_type = data_type
        self.cache_dir: Directory | TemporaryDirectory = (
            Directory(cache_dir) if cache_dir else TemporaryDirectory()
        )
        self.filters = filters
        self.max_concurrent_downloads = max_concurrent_downloads
        self.chunk_time = chunk_time

        self.broker = bgpkit.Broker()

    @staticmethod
    def _generate_cache_filename(url):
        """Generate a cache filename compatible with BGPKIT parser."""

        hash_suffix = crc32(url)

        if "updates." in url:
            data_type = "updates"
        elif "rib" in url or "view" in url:
            data_type = "rib"
        else:
            raise ValueError("Could not understand data type from url")

        # Look for patterns like rib.20100901.0200 or updates.20100831.2345
        timestamp_match = re.search(r"(\d{8})\.(\d{4})", url)
        if timestamp_match:
            timestamp = f"{timestamp_match.group(1)}.{timestamp_match.group(2)}"
        else:
            raise ValueError("Could not parse timestamp from url")

        if url.endswith(".bz2"):
            compression_ext = "bz2"
        elif url.endswith(".gz"):
            compression_ext = "gz"
        else:
            raise ValueError("Could not parse extension from url")

        return f"cache-{data_type}.{timestamp}.{hash_suffix}.{compression_ext}"

    def _set_urls(self):
        """Set archive files URL with bgpkit broker"""
        # Set the urls with bgpkit broker
        self.urls = {"rib": defaultdict(list), "update": defaultdict(list)}
        for data_type in self.data_type:
            items: list[BrokerItem] = self.broker.query(
                ts_start=int(self.ts_start - 60),
                ts_end=int(self.ts_end),
                collector_id=self.collector_id,
                data_type=data_type,
            )
            for item in items:
                self.urls[data_type][item.collector_id].append(item.url)

    async def _download_file(self, semaphore, session, url, filepath, data_type, rc):
        """Helper coroutine to download a single file, controlled by a semaphore"""
        async with semaphore:
            logging.debug(f"{filepath} is a cache miss. Downloading {url}")
            try:
                async with session.get(url) as resp:
                    resp.raise_for_status()
                    with open(filepath, "wb") as fd:
                        async for chunk in resp.content.iter_chunked(8192):
                            fd.write(chunk)
                    return data_type, rc, filepath
            except aiohttp.ClientError as e:
                logging.error(f"Failed to download {url}: {e}")
                # Return None on failure so asyncio.gather doesn't cancel everything.
                return None

    async def _prefetch_data(self):
        """Download archive files concurrently and cache to `self.cache_dir`"""
        self.paths = {"rib": defaultdict(list), "update": defaultdict(list)}
        tasks = []

        semaphore = asyncio.Semaphore(self.max_concurrent_downloads)

        conn = aiohttp.TCPConnector()
        async with aiohttp.ClientSession(connector=conn) as session:
            # Create all the download tasks.
            for data_type in self.data_type:
                for rc, rc_urls in self.urls[data_type].items():
                    for url in rc_urls:
                        filename = self._generate_cache_filename(url)
                        filepath = os.path.join(self.cache_dir.name, filename)

                        if os.path.exists(filepath):
                            logging.debug(f"{filepath} is a cache hit")
                            self.paths[data_type][rc].append(filepath)
                        else:
                            task = asyncio.create_task(
                                self._download_file(
                                    semaphore, session, url, filepath, data_type, rc
                                )
                            )
                            tasks.append(task)

            if tasks:
                logging.info(
                    f"Starting download of {len(tasks)} files with a concurrency of {self.max_concurrent_downloads}..."
                )
                results = await asyncio.gather(*tasks)

                # Process the results, skipping any 'None' values from failed downloads.
                for result in results:
                    if result:
                        data_type, rc, filepath = result
                        self.paths[data_type][rc].append(filepath)
                logging.info("All downloads finished.")

    def _create_tagged_iterator(self, iterator, is_rib, collector):
        """Creates a generator that tags elements with metadata missing in bgpkit."""
        return ((elem.timestamp, elem, is_rib, collector) for elem in iterator)

    def __iter__(self) -> Iterator[BGPElement]:
        # try/finally to cleanup the fetching cache
        try:
            # Manager mode: spawn smaller worker streams to balance fetch/parse
            if self.chunk_time:
                current = self.ts_start

                while current < self.ts_end:
                    chunk_end = min(current + self.chunk_time, self.ts_end)

                    logging.info(
                        f"Processing chunk: {datetime.datetime.fromtimestamp(current)} "
                        f"to {datetime.datetime.fromtimestamp(chunk_end)}"
                    )

                    worker = type(self)(
                        ts_start=current,
                        ts_end=chunk_end
                        - 1,  # remove one second because BGPKIT include border
                        collector_id=self.collector_id,
                        data_type=self.data_type,
                        cache_dir=None,
                        filters=self.filters,
                        max_concurrent_downloads=self.max_concurrent_downloads,
                        chunk_time=None,  # Worker doesn't chunk itself
                    )

                    yield from worker
                    current = chunk_end + 1e-7

                return

            self._set_urls()

            asyncio.run(self._prefetch_data())

            # One iterator for each data_type * collector combinations
            # To be merged according to the elements timestamp
            iterators_to_merge = []

            for data_type in self.data_type:
                is_rib = data_type == "rib"

                # Get rib or update files per collector
                rc_to_paths = self.paths[data_type]

                # Chain rib or update iterators to get one stream per collector / data_type
                for rc, paths in rc_to_paths.items():
                    parsers = [
                        bgpkit.Parser(url=path, filters=self.filters) for path in paths
                    ]

                    chained_iterator = chain.from_iterable(parsers)

                    # Add metadata lost by bgpkit for compatibility with pubgpstream
                    iterators_to_merge.append((chained_iterator, is_rib, rc))

            # Make a generator to tag each bgpkit element with metadata
            # Benefit 1: full compat with pybgpstream
            # Benefit 2: we give a key easy to access for heapq to merge
            tagged_iterators = [
                self._create_tagged_iterator(it, is_rib, rc)
                for it, is_rib, rc in iterators_to_merge
            ]

            # Merge and convert to pybgpstream format
            for timestamp, bgpkit_elem, is_rib, rc in merge(
                *tagged_iterators, key=itemgetter(0)
            ):
                if self.ts_start <= timestamp <= self.ts_end:
                    yield convert_bgpkit_elem(bgpkit_elem, is_rib, rc)

        finally:
            self.cache_dir.cleanup()

    @classmethod
    def from_config(cls, config: BGPStreamConfig):
        return cls(
            ts_start=config.start_time.timestamp(),
            ts_end=config.end_time.timestamp(),
            collector_id=",".join(config.collectors),
            data_type=[
                dtype[:-1] for dtype in config.data_types
            ],  # removes plural form
            cache_dir=str(config.cache_dir) if config.cache_dir else None,
            filters=config.filters.model_dump(exclude_unset=True)
            if config.filters
            else {},
            max_concurrent_downloads=config.max_concurrent_downloads
            if config.max_concurrent_downloads
            else 10,
            chunk_time=config.chunk_time.seconds if config.chunk_time else None,
        )
