from typing import List, Dict, Any

class Chunker:
    """
    Splits file content into logical segments or chunks of text
    based on character limits and overlap rules.
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_file(self, file_metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Takes file metadata (with content, file_path, file_type) and returns a list of chunks.
        """
        content = file_metadata.get("content", "")
        file_path = file_metadata.get("file_path", "")
        file_type = file_metadata.get("file_type", "")

        chunks = []
        if not content:
            return chunks

        # Handle file contents smaller than chunk_size
        if len(content) <= self.chunk_size:
            chunks.append({
                "chunk_id": f"{file_path}#0",
                "file_path": file_path,
                "file_type": file_type,
                "content": content,
                "start_idx": 0,
                "end_idx": len(content)
            })
            return chunks

        start = 0
        chunk_idx = 0
        while start < len(content):
            end = min(start + self.chunk_size, len(content))
            
            # If we are not at the end of the file, try to break at a newline to avoid splitting lines
            if end < len(content):
                # Search backward for a newline character in the last 15% of the chunk size
                search_start = max(start, end - int(self.chunk_size * 0.15))
                newline_idx = content.rfind("\n", search_start, end)
                if newline_idx != -1:
                    end = newline_idx + 1  # include the newline character

            chunk_text = content[start:end]
            chunks.append({
                "chunk_id": f"{file_path}#{chunk_idx}",
                "file_path": file_path,
                "file_type": file_type,
                "content": chunk_text,
                "start_idx": start,
                "end_idx": end
            })
            
            chunk_idx += 1
            # Next start is calculated using overlap
            next_start = end - self.chunk_overlap
            
            # Guarantee forward progress and avoid infinite loops
            if next_start >= end or next_start <= start:
                start = end
            else:
                start = next_start

        return chunks
