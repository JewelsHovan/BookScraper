from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, List, Tuple, Callable
from pathlib import Path
import threading
from dataclasses import dataclass
from queue import Queue, Empty
import time
import random

from src.utils.html_fetcher import HTMLFetcher
from src.utils.validator import ContentValidator, ValidationResult
from src.models.book import Book

@dataclass
class DownloadResult:
    chapter_number: int
    content: Optional[str]
    validation: Optional[ValidationResult]
    error: Optional[str] = None

class ChapterDownloader:
    """Handles concurrent chapter downloads with validation and progress tracking."""
    
    def __init__(self, max_workers: int = 5, max_retries: int = 3, chunk_size: int = 10):
        self.max_workers = max_workers
        self.max_retries = max_retries
        self.chunk_size = chunk_size  # Process chapters in chunks to avoid memory issues
        self.validator = ContentValidator()
        self._progress_queue = Queue()
        self._stop_event = threading.Event()
    
    def download_chapters(
        self,
        book: Book,
        url_template: str,
        start_chapter: int,
        end_chapter: int,
        progress_callback: Optional[Callable] = None
    ) -> List[DownloadResult]:
        """
        Download chapters concurrently using a worker pool pattern.
        Implements chunking for better memory management and rate limiting.
        """
        all_results = []
        total_chapters = end_chapter - start_chapter + 1
        
        # Start progress monitoring if callback provided
        if progress_callback:
            progress_thread = threading.Thread(
                target=self._monitor_progress,
                args=(total_chapters, progress_callback)
            )
            progress_thread.daemon = True
            progress_thread.start()

        try:
            # Process chapters in chunks to manage memory
            for chunk_start in range(start_chapter, end_chapter + 1, self.chunk_size):
                chunk_end = min(chunk_start + self.chunk_size - 1, end_chapter)
                chunk_results = self._process_chapter_chunk(
                    url_template, 
                    chunk_start, 
                    chunk_end
                )
                all_results.extend(chunk_results)

        finally:
            # Cleanup
            self._stop_event.set()
            if progress_callback:
                progress_thread.join(timeout=1.0)

        return sorted(all_results, key=lambda x: x.chapter_number)
    
    def _process_chapter_chunk(
        self, 
        url_template: str, 
        start: int, 
        end: int
    ) -> List[DownloadResult]:
        """Process a chunk of chapters using thread pool."""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_chapter = {
                executor.submit(
                    self._download_with_retry,
                    url_template,
                    chapter_num
                ): chapter_num
                for chapter_num in range(start, end + 1)
            }

            for future in as_completed(future_to_chapter):
                try:
                    result = future.result()
                    results.append(result)
                    self._progress_queue.put(1)
                except Exception as e:
                    chapter_num = future_to_chapter[future]
                    results.append(DownloadResult(
                        chapter_number=chapter_num,
                        content=None,
                        validation=None,
                        error=f"Unexpected error: {str(e)}"
                    ))
                    self._progress_queue.put(1)

        return results
    
    def _download_with_retry(
        self,
        url_template: str,
        chapter_number: int,
    ) -> DownloadResult:
        """Download a single chapter with exponential backoff retry logic."""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                with HTMLFetcher() as fetcher:
                    url = url_template.format(chapter_number=chapter_number)
                    content = fetcher.fetch(url)
                    
                    # Debug logging
                    print(f"Chapter {chapter_number} - Content received: {bool(content)} - Length: {len(content) if content else 0}")
                    
                    if not content or len(content.strip()) == 0:
                        raise ValueError(f"Empty or invalid content received for chapter {chapter_number}")
                    
                    validation = self.validator.validate_chapter(content, chapter_number)
                    
                    # Debug validation results
                    if validation.is_valid:
                        print(f"Chapter {chapter_number} - Validation successful")
                        return DownloadResult(
                            chapter_number=chapter_number,
                            content=content,
                            validation=validation,
                            error=None  # Explicitly set to None for successful downloads
                        )
                    else:
                        print(f"Chapter {chapter_number} - Validation failed: {validation.errors}")
                        last_error = f"Content validation failed: {', '.join(validation.errors)}"
                    
            except Exception as e:
                print(f"Chapter {chapter_number} - Attempt {attempt + 1} failed: {str(e)}")
                last_error = str(e)
            
            # Exponential backoff with jitter
            delay = (2 ** attempt) + (random.random() * 0.1)
            time.sleep(delay)
        
        # If we get here, all attempts failed
        print(f"Chapter {chapter_number} - All attempts failed. Last error: {last_error}")
        return DownloadResult(
            chapter_number=chapter_number,
            content=None,
            validation=None,
            error=f"Failed after {self.max_retries} attempts: {last_error}"
        )
    
    def _monitor_progress(self, total_chapters: int, callback: Callable) -> None:
        """Monitor and report download progress."""
        completed = 0
        
        while not self._stop_event.is_set() and completed < total_chapters:
            try:
                completed += self._progress_queue.get(timeout=0.1)
                callback(completed, total_chapters)
            except Empty:
                continue
