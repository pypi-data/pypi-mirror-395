# codefusion/core/writer.py
import logging
import sys
import typing as t
import json
import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn, FileSizeColumn
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from .reader import read_file_content
from .grouper import FileGrouper
from ..templates import TemplateRenderer
from .. import __version__

logger = logging.getLogger(__name__)

class CodeWriter:
    def __init__(self, root_dir: Path, output_file: t.Optional[Path],
                 grouper: FileGrouper,
                 template: str = "default", no_grouping: bool = False,
                 to_stdout: bool = False, num_workers: int = 1,
                 resume: bool = False, detect_secrets: bool = False):
        self.root_dir = root_dir
        self.output_file = output_file
        self.grouper = grouper
        self.template = template
        self.no_grouping = no_grouping
        self.to_stdout = to_stdout
        self.num_workers = num_workers
        self.renderer = TemplateRenderer()
        self.resume = resume
        self.detect_secrets = detect_secrets
        
        if self.detect_secrets:
            from .security import SecretDetector
            self.secret_detector = SecretDetector()
        else:
            self.secret_detector = None

        self.state_file = self.root_dir / ".codefusion_state"

    def write(self, files_to_process: t.List[Path], final_extensions: t.Set[str]) -> bool:
        total_files = len(files_to_process)

        if self.no_grouping:
            files_to_process.sort()
            grouped_files = [('all', files_to_process)]
        else:
            grouped_files = self.grouper.group_and_sort_files(files_to_process, self.root_dir)

        # Resume logic
        processed_files_set = set()
        if self.resume and self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    processed_files_set = set(data.get('processed_files', []))
                logger.info(f"Resuming compilation. Skipping {len(processed_files_set)} already processed files.")
            except Exception as e:
                logger.warning(f"Failed to load resume state: {e}")

        if self.output_file and self.output_file.exists() and not self.to_stdout and not self.resume:
            try:
                # If not resuming, ask to overwrite
                response = input(f"Output file '{self.output_file}' exists. Overwrite? (y/N): ")
                if response.lower() != 'y':
                    logger.info("Operation cancelled by user.")
                    return False
            except (EOFError, KeyboardInterrupt):
                logger.info("Operation cancelled by user.")
                return False

        start_time = datetime.datetime.now()

        # For resume, we append if file exists, else write new
        mode = 'a' if self.resume and self.output_file and self.output_file.exists() else 'w'
        
        output_stream = self._setup_output_stream(mode)
        if not output_stream:
            return False

        try:
            if self.template == 'json':
                # JSON doesn't support easy appending/resume without parsing the whole file.
                # For now, we disable resume for JSON or just rewrite.
                if self.resume:
                    logger.warning("Resume is not fully supported for JSON template. Rewriting.")
                self._write_json(output_stream, grouped_files, final_extensions, total_files, start_time)
            else:
                self._write_text(output_stream, grouped_files, final_extensions, total_files, start_time, processed_files_set)

            # Cleanup state file on success
            if self.state_file.exists():
                self.state_file.unlink()
                
            return True

        except KeyboardInterrupt:
            logger.warning("Compilation interrupted. Saving state...")
            self._save_state(processed_files_set)
            return False
        except Exception as e:
            logger.error(f"❌ Fatal error during compilation: {e}")
            self._save_state(processed_files_set)
            return False
        finally:
            if self.output_file and output_stream and not output_stream.closed:
                output_stream.close()

    def _save_state(self, processed_files: t.Set[str]):
        try:
            with open(self.state_file, 'w') as f:
                json.dump({'processed_files': list(processed_files)}, f)
            logger.info(f"State saved to {self.state_file}")
        except Exception as e:
            logger.error(f"Failed to save state: {e}")

    def _setup_output_stream(self, mode='w'):
        if self.to_stdout:
            return sys.stdout
        elif self.output_file:
            self.output_file.parent.mkdir(parents=True, exist_ok=True)
            return self.output_file.open(mode, encoding='utf-8')
        else:
            logger.error("No output destination specified")
            return None

    def _write_json(self, output_stream, grouped_files, final_extensions, total_files, start_time):
        # ... (Existing JSON logic, maybe updated for streaming if needed, but keeping simple for now)
        # We will just use the previous logic but adapted to new reader
        # JSON output is hard to stream efficiently without a custom generator
        # For v1.1.0, let's keep JSON mostly as is but use the new reader (non-streaming mode)
        
        json_data = {}
        timestamp = start_time.strftime('%Y-%m-%d %H:%M:%S')
        extensions_str = ', '.join(sorted(final_extensions)) if final_extensions else 'Auto-detected'
        
        json_data['metadata'] = {
            'generated_at': timestamp,
            'source_directory': str(self.root_dir),
            'extensions': extensions_str,
            'total_files': total_files
        }
        
        json_data['groups'] = []
        processed_count = 0
        error_count = 0
        
        # Use ThreadPool for JSON since we need to build the object anyway
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            for group_name, group_files in grouped_files:
                group_info = {
                    'group': group_name,
                    'description': self.grouper.get_group_description(group_name),
                    'file_count': len(group_files),
                    'files': []
                }
                
                future_to_file = {executor.submit(read_file_content, file_path): file_path for file_path in group_files}
                
                file_results = []
                for future in as_completed(future_to_file):
                    file_path = future_to_file[future]
                    try:
                        content, error_msg = future.result()
                        if error_msg:
                            error_count += 1
                            logger.error(f"Error processing {file_path}: {error_msg}")
                        else:
                            if self.detect_secrets and self.secret_detector:
                                content, _ = self.secret_detector.redact(content)
                            
                            processed_count += 1
                            file_results.append({
                                'path': str(file_path.resolve()),
                                'content': content
                            })
                    except Exception as e:
                        logger.error(f"Error processing {file_path}: {e}")
                        error_count += 1
                
                file_results.sort(key=lambda x: x['path'])
                group_info['files'] = file_results
                json_data['groups'].append(group_info)

        completion_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        json_data['summary'] = {
            'processed_count': processed_count,
            'error_count': error_count,
            'completion_time': completion_time
        }
        
        output_stream.write(json.dumps(json_data, indent=2))

    def _write_text(self, output_stream, grouped_files, final_extensions, total_files, start_time, processed_files_set):
        timestamp = start_time.strftime('%Y-%m-%d %H:%M:%S')
        extensions_str = ', '.join(sorted(final_extensions)) if final_extensions else 'Auto-detected'
        
        # Only write header if not resuming or file is empty
        if not self.resume or (self.output_file and self.output_file.stat().st_size == 0):
            header = self.renderer.render_header(
                self.template,
                timestamp=timestamp,
                source_dir=self.root_dir,
                extensions=extensions_str,
                total_files=total_files
            )
            output_stream.write(header)

        logger.info(f"Compiling {total_files} files...")
        
        processed_count = 0
        error_count = 0

        progress_columns = [
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            FileSizeColumn(),
        ]

        # Sequential processing for streaming support
        with Progress(*progress_columns, transient=True) as progress:
            task = progress.add_task("Compiling...", total=total_files)
            
            # Advance progress for already processed files
            progress.advance(task, len(processed_files_set))

            for group_name, group_files in grouped_files:
                if not self.no_grouping:
                    # We might repeat group headers in resume mode if we stopped mid-group.
                    # Ideally we check if we already wrote this group header?
                    # For simplicity, we just write it. The user can ignore duplicates.
                    group_description = self.grouper.get_group_description(group_name)
                    group_header = self.renderer.render_group_header(
                        self.template,
                        group_name,
                        group_description,
                        len(group_files)
                    )
                    output_stream.write(group_header)
                
                for file_path in group_files:
                    abs_path_str = str(file_path.resolve())
                    
                    if abs_path_str in processed_files_set:
                        continue

                    rel_path_str = file_path.relative_to(self.root_dir).as_posix()
                    progress.update(task, description=f"Processing [cyan]{rel_path_str}[/cyan]")
                    
                    try:
                        # Write File Header
                        file_header = self.renderer.render_file_header(self.template, abs_path_str)
                        output_stream.write(file_header)

                        # Stream Content
                        from .reader import stream_file_content
                        
                        # We need to buffer chunks if we are doing secret detection?
                        # Regex usually needs full context or at least overlapping chunks.
                        # For now, if secret detection is ON, we might need to read full file (or large chunks).
                        # Let's assume for secret detection we read full file for safety, 
                        # OR we just apply regex on chunks (might miss secrets spanning chunks).
                        # Given the requirement "Memory-Efficient Streaming", we should try to stream.
                        # But "Secret Detection" conflicts with strict streaming if secrets span chunks.
                        # Compromise: Read full file if secret detection is on, else stream.
                        
                        if self.detect_secrets and self.secret_detector:
                            # Read full content for accurate detection
                            content, error_msg = read_file_content(file_path)
                            if error_msg:
                                output_stream.write(f"\n[FAILED TO READ: {error_msg}]\n")
                                error_count += 1
                            else:
                                content, _ = self.secret_detector.redact(content)
                                output_stream.write(content)
                                processed_count += 1
                        else:
                            # True Streaming
                            try:
                                for chunk in stream_file_content(file_path):
                                    output_stream.write(chunk)
                                processed_count += 1
                            except Exception as e:
                                output_stream.write(f"\n[FAILED TO READ: {e}]\n")
                                error_count += 1

                        # Write File Footer
                        file_footer = self.renderer.render_file_footer(self.template)
                        output_stream.write(file_footer)
                        
                        # Mark as processed
                        processed_files_set.add(abs_path_str)
                        progress.advance(task, 1)
                        
                    except Exception as e:
                        logger.error(f"Error processing {rel_path_str}: {e}")
                        error_count += 1

                if not self.no_grouping and self.template == "json":
                    group_footer = self.renderer.render_group_footer(self.template)
                    output_stream.write(group_footer)

        completion_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        footer = self.renderer.render_footer(
            self.template,
            processed_count=processed_count,
            error_count=error_count,
            timestamp=completion_time
        )
        output_stream.write(footer)

        elapsed = datetime.datetime.now() - start_time
        if self.output_file:
            logger.info(f"✅ Compilation complete: {self.output_file.resolve()}")
        else:
            logger.info("✅ Compilation complete (output to stdout)")
        
        logger.info(f"📊 Processed {processed_count} files successfully in {elapsed.total_seconds():.2f}s")
        if error_count:
            logger.warning(f"⚠️  {error_count} files had read errors")
