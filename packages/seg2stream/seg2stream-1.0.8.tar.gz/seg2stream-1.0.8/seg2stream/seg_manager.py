from decorator import DEF
import queue
import asyncio
from typing import List, Callable, Dict
import multiprocessing
import threading
import queue

from .seg2stream import (
    SegmentationPipeline as SegSent2StreamPipeline,
    SegmentationConfig as SegSent2StreamConfig,
)
from .seg2generator import (
    SegmentationPipeline as SegSent2GeneratorPipeline,
    SegmentationConfig as SegSent2GeneratorConfig,
)
from .segmenters import get_sentence_segmenter


class SegmentationTask:
    def __init__(
        self,
        id: str,
        pipeline: SegSent2StreamPipeline | SegSent2GeneratorPipeline,
        out_queue: queue.Queue,
    ):
        self.id = id
        self.pipeline = pipeline
        self.out_queue = out_queue
        self.future = asyncio.gather(self.process_output(), pipeline.segment())

    async def process_output(self):
        async for output in self.pipeline.output_stream():
            self.out_queue.put_nowait((self.id, output))
        self.out_queue.put_nowait((self.id, None))

    def send(self, text: str | None):
        self.pipeline.fill(text)


class SegmentationManager:
    def __init__(
        self,
        seg_config: SegSent2StreamConfig | SegSent2GeneratorConfig,
        segmenters: List[Callable[[str], str]] | None = None,
        interval=1e-7,
    ):
        if isinstance(seg_config, SegSent2StreamConfig):
            self.seg_pipeline_class = SegSent2StreamPipeline
            manager = multiprocessing.Manager()
            self.in_queue = manager.Queue()
            self.out_queue = manager.Queue()
            self.seg_job = multiprocessing.Process(
                target=self.segmentation_job, name="segmentation", daemon=True
            )
        elif isinstance(seg_config, SegSent2GeneratorConfig):
            self.seg_pipeline_class = SegSent2GeneratorPipeline
            self.in_queue = queue.Queue()
            self.out_queue = queue.Queue()
            self.seg_job = threading.Thread(
                target=self.segmentation_job, name="segmentation", daemon=True
            )

        self.seg_config = seg_config
        self.segmenters = segmenters if segmenters else [get_sentence_segmenter()]
        self.interval = interval

    def segmentation_job(self):
        async def main():
            tasks: Dict[str, SegmentationTask] = {}

            while True:
                try:
                    id, text = self.in_queue.get_nowait()
                except queue.Empty:
                    await asyncio.sleep(self.interval)
                    continue

                if id is None:
                    break
                if id not in tasks:
                    tasks[id] = SegmentationTask(
                        id=id,
                        pipeline=self.seg_pipeline_class(
                            config=self.seg_config, segmenters=self.segmenters
                        ),
                        out_queue=self.out_queue,
                    )
                tasks[id].send(text)

            for i in tasks.values():
                await i.future

        loop = asyncio.new_event_loop()
        loop.run_until_complete(main())

    def start(self):
        self.seg_job.start()

    def add_text(self, id: str | None, text: str | None):
        self.in_queue.put_nowait((id, text))

    async def get_async_output(self):
        while True:
            try:
                id, output = self.out_queue.get_nowait()
            except queue.Empty:
                await asyncio.sleep(self.interval)
                continue
            if id is None:
                return
            yield (id, output)

    def get_output(self):
        while True:
            id, output = self.out_queue.get()
            if id is None:
                return
            yield (id, output)

    def close(self):
        self.in_queue.put((None, None))
        self.seg_job.join()
        self.out_queue.put((None, None))
