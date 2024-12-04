from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, List, Tuple
from pathlib import Path
import threading
from dataclasses import dataclass
from queue import Queue
import time

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
    
    def __init__(self, max_workers: int = 5, max_retries: int = 3):
        self.max_workers = max_workers
        self.max_retries = max_retries
        self.validator = ContentValidator()
        self._progress_queue = Queue()
        self._stop_progress = threading.Event()
    
    def download_chapters(
        self,
        book: Book,
        url_template: str,
        start_chapter: int,
        end_chapter: int,
        progress_callback=None
    ) -> List[DownloadResult]:
        """
        Download multiple chapters concurrently.
        
        Args:
            book: Book object
            url_template: URL template for chapters
            start_chapter: Starting chapter number
            end_chapter: Ending chapter number
            progress_callback: Optional callback for progress updates
        """
        chapters_to_download = list(range(start_chapter, end_chapter + 1))
        results = []
        
        # Start progress reporting thread if callback provided
        if progress_callback:
            progress_thread = threading.Thread(
                target=self._progress_reporter,
                args=(len(chapters_to_download), progress_callback)
            )
            progress_thread.start()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_chapter = {
                executor.submit(
                    self._download_chapter_with_retry,
                    url_template,
                    chapter_num
                ): chapter_num
                for chapter_num in chapters_to_download
            }
            
            for future in as_completed(future_to_chapter):
                chapter_num = future_to_chapter[future]
                try:
                    result = future.result()
                    results.append(result)
                    self._progress_queue.put(1)
                except Exception as e:
                    results.append(DownloadResult(
                        chapter_number=chapter_num,
                        content=None,
                        validation=None,
                        error=str(e)
                    ))
                    self._progress_queue.put(1)
        
        # Stop progress reporting
        if progress_callback:
            self._stop_progress.set()
            progress_thread.join()
        
        return sorted(results, key=lambda x: x.chapter_number)
    
    def _download_chapter_with_retry(
        self,
        url_template: str,
        chapter_number: int
    ) -> DownloadResult:
        """Download a single chapter with retry logic."""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                with HTMLFetcher() as fetcher:
                    url = url_template.format(chapter_number=chapter_number)
                    content = fetcher.fetch(url)
                    
                    if not content:
                        raise ValueError("Empty content received")
                    
                    # Validate content
                    validation = self.validator.validate_chapter(content, chapter_number)
                    
                    if validation.is_valid:
                        return DownloadResult(
                            chapter_number=chapter_number,
                            content=content,
                            validation=validation
                        )
                    
                    # If content is invalid, try again
                    last_error = f"Invalid content: {', '.join(validation.errors)}"
                    time.sleep(1 * (attempt + 1))  # Exponential backoff
                    
            except Exception as e:
                last_error = str(e)
                time.sleep(1 * (attempt + 1))
        
        return DownloadResult(
            chapter_number=chapter_number,
            content=None,
            validation=None,
            error=f"Failed after {self.max_retries} attempts: {last_error}"
        )
    
    def _progress_reporter(self, total_chapters: int, callback) -> None:
        """Report download progress through callback."""
        completed = 0
        
        while not self._stop_progress.is_set():
            try:
                completed += self._progress_queue.get(timeout=0.1)
                callback(completed, total_chapters)
            except:
                continue
