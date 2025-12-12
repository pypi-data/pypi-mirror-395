"""Wiki client for Mogu SDK"""

import re
import logging
from typing import List, Optional, Set, Tuple

from mogu_sdk.auth import BaseClient
from mogu_sdk.exceptions import NotFoundError
from mogu_sdk.models import (
    CreateWikiFileRequest,
    UpdateWikiFileRequest,
    WikiContent,
    WikiFile,
    WikiSearchMatch,
    WikiSearchResponse,
    WikiSearchResult,
    WikiUpdateResponse,
)

logger = logging.getLogger(__name__)


# Common stop words to filter out from search queries
_STOP_WORDS = {
    # Basic stop words
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could", "should",
    "may", "might", "must", "shall", "can", "need", "dare", "ought", "used",
    "to", "of", "in", "for", "on", "with", "at", "by", "from", "as", "into",
    "through", "during", "before", "after", "above", "below", "between", "under",
    "again", "further", "then", "once", "here", "there", "when", "where", "why",
    "how", "all", "each", "few", "more", "most", "other", "some", "such", "no",
    "nor", "not", "only", "own", "same", "so", "than", "too", "very", "just",
    "and", "but", "if", "or", "because", "until", "while", "although", "though",
    "what", "which", "who", "whom", "this", "that", "these", "those", "am",
    "it", "its", "itself", "they", "them", "their", "theirs", "we", "us", "our",
    "i", "me", "my", "myself", "you", "your", "yours", "he", "him", "his", "she", "her",
    # Common filler words in queries
    "find", "search", "look", "looking", "get", "show", "tell", "explain",
    "mean", "means", "meaning", "definition", "define", "about", "information",
    "please", "help", "want", "like", "know", "understand", "describe",
    # Domain-specific generic words (too broad for useful search)
    "column", "columns", "field", "fields", "table", "tables", "row", "rows",
    "data", "database", "schema", "record", "records", "value", "values",
    "type", "types", "name", "names", "list", "item", "items", "entry", "entries",
    "file", "files", "document", "documents", "page", "pages", "section", "sections",
    "code", "example", "examples", "sample", "samples", "use", "using", "used",
    "create", "read", "update", "delete", "add", "remove", "change", "modify",
    "new", "old", "first", "last", "next", "previous", "current", "default",
    "primary", "secondary", "main", "key", "keys", "foreign", "unique",
    "contains", "contain", "include", "includes", "including", "related",
    "based", "specific", "general", "common", "standard", "custom", "special"
}

# Common abbreviation expansions for data/technical terms
_ABBREVIATION_EXPANSIONS = {
    "cust": "customer", "acct": "account", "amt": "amount", "qty": "quantity",
    "txn": "transaction", "tx": "transaction", "prod": "product", "cat": "category",
    "desc": "description", "dt": "date", "tm": "time", "ts": "timestamp",
    "id": "identifier", "num": "number", "no": "number", "addr": "address",
    "tel": "telephone", "msg": "message", "req": "request", "res": "response",
    "src": "source", "dst": "destination", "tgt": "target", "cfg": "config",
    "env": "environment", "seg": "segment", "stat": "status", "cnt": "count",
    "val": "value", "avg": "average", "max": "maximum", "min": "minimum",
    "pct": "percent", "calc": "calculate", "proc": "process", "info": "information",
    "org": "organization", "dept": "department", "emp": "employee", "mgr": "manager",
    "inv": "invoice", "pmt": "payment", "bal": "balance", "ref": "reference",
    "doc": "document", "spec": "specification", "attr": "attribute", "prop": "property",
    "idx": "index", "seq": "sequence", "grp": "group", "lvl": "level", "typ": "type",
}


class WikiClient:
    """Client for wiki operations"""

    def __init__(self, client: BaseClient) -> None:
        """
        Initialize wiki client.

        Args:
            client: Base HTTP client for making requests
        """
        self._client = client

    async def list_files(
        self,
        workspace_id: str,
        folder_path: Optional[str] = None,
        recursive: bool = True,
    ) -> List[WikiFile]:
        """
        List markdown files in the workspace wiki.

        Args:
            workspace_id: Workspace identifier
            folder_path: Optional subfolder path within docs folder
            recursive: Whether to list files recursively

        Returns:
            List of wiki files and folders

        Raises:
            NotFoundError: If workspace not found
            PermissionDeniedError: If user lacks access
            MoguAPIError: On other API errors
        """
        params = {"recursive": str(recursive).lower()}
        if folder_path:
            params["folder_path"] = folder_path

        response = await self._client.get(
            f"/api/v1/wiki/workspaces/{workspace_id}/files",
            params=params,
        )

        data = response.json()
        return [WikiFile(**file_data) for file_data in data["files"]]

    async def get_content(
        self,
        workspace_id: str,
        path: str,
    ) -> WikiContent:
        """
        Get the content of a markdown file from the wiki.

        Args:
            workspace_id: Workspace identifier
            path: Path to the markdown file within the repository

        Returns:
            Wiki file content

        Raises:
            NotFoundError: If workspace or file not found
            PermissionDeniedError: If user lacks access
            MoguAPIError: On other API errors
        """
        response = await self._client.get(
            f"/api/v1/wiki/workspaces/{workspace_id}/content",
            params={"path": path},
        )

        data = response.json()
        return WikiContent(**data)

    async def create_file(
        self,
        workspace_id: str,
        path: str,
        content: str = "",
        commit_message: str = "Create new wiki file",
    ) -> WikiUpdateResponse:
        """
        Create a new wiki file.

        Args:
            workspace_id: Workspace identifier
            path: File path relative to repository root
            content: Initial file content
            commit_message: Commit message for the Git commit

        Returns:
            Update response with commit ID

        Raises:
            PermissionDeniedError: If user lacks edit permission
            ValidationError: If input validation fails
            MoguAPIError: On other API errors
        """
        request_data = CreateWikiFileRequest(
            path=path,
            content=content,
            commit_message=commit_message,
        )

        response = await self._client.post(
            f"/api/v1/wiki/workspaces/{workspace_id}/content",
            json=request_data.model_dump(),
        )

        data = response.json()
        return WikiUpdateResponse(**data)

    async def update_file(
        self,
        workspace_id: str,
        path: str,
        content: str,
        commit_message: str = "Update wiki file",
    ) -> WikiUpdateResponse:
        """
        Update an existing wiki file.

        Args:
            workspace_id: Workspace identifier
            path: File path relative to repository root
            content: Updated file content
            commit_message: Commit message for the Git commit

        Returns:
            Update response with commit ID

        Raises:
            NotFoundError: If file not found
            PermissionDeniedError: If user lacks edit permission
            ValidationError: If input validation fails
            MoguAPIError: On other API errors
        """
        request_data = UpdateWikiFileRequest(
            path=path,
            content=content,
            commit_message=commit_message,
        )

        response = await self._client.put(
            f"/api/v1/wiki/workspaces/{workspace_id}/content",
            json=request_data.model_dump(),
        )

        data = response.json()
        return WikiUpdateResponse(**data)

    async def create_or_update_page(
        self,
        workspace_id: str,
        path: str,
        content: str,
        commit_message: Optional[str] = None,
    ) -> WikiUpdateResponse:
        """
        Create or update a wiki page intelligently.

        This method automatically detects if the file exists and either creates
        or updates it accordingly. This is the recommended method for page management.

        Args:
            workspace_id: Workspace identifier
            path: File path relative to repository root
            content: Page content
            commit_message: Optional commit message (auto-generated if not provided)

        Returns:
            Update response with commit ID and operation message

        Raises:
            PermissionDeniedError: If user lacks edit permission
            ValidationError: If input validation fails
            MoguAPIError: On other API errors
        """
        # Try to get existing content to determine if file exists
        file_exists = False
        try:
            await self.get_content(workspace_id=workspace_id, path=path)
            file_exists = True
        except NotFoundError:
            file_exists = False

        # Generate default commit message if not provided
        if not commit_message:
            action = "Update" if file_exists else "Create"
            commit_message = f"{action} {path}"

        # Create or update based on existence
        if file_exists:
            return await self.update_file(
                workspace_id=workspace_id,
                path=path,
                content=content,
                commit_message=commit_message,
            )
        else:
            return await self.create_file(
                workspace_id=workspace_id,
                path=path,
                content=content,
                commit_message=commit_message,
            )

    async def delete_file(
        self,
        workspace_id: str,
        path: str,
        commit_message: str = "Delete wiki file",
    ) -> WikiUpdateResponse:
        """
        Delete a wiki file.

        Args:
            workspace_id: Workspace identifier
            path: Path to the file to delete
            commit_message: Commit message for the Git commit

        Returns:
            Update response with commit ID

        Raises:
            NotFoundError: If file not found
            PermissionDeniedError: If user lacks delete permission
            MoguAPIError: On other API errors
        """
        response = await self._client.delete(
            f"/api/v1/wiki/workspaces/{workspace_id}/content",
            params={"path": path, "commit_message": commit_message},
        )

        data = response.json()
        return WikiUpdateResponse(**data)

    def _extract_snippet(
        self,
        full_content: str,
        match_line_number: int,
        char_offset: int,
        match_length: int,
        snippet_chars: int,
    ) -> tuple[str, int, int]:
        """
        Extract character-based snippet around a match.

        Args:
            full_content: Full content of the file
            match_line_number: Line number of the match (1-indexed)
            char_offset: Character offset within the line
            match_length: Length of the match
            snippet_chars: Total characters to extract around match

        Returns:
            Tuple of (snippet_text, match_start_in_snippet, match_end_in_snippet)
        """
        # Convert line-based position to absolute character position
        lines = full_content.splitlines(keepends=True)
        
        # Calculate absolute character position of the match
        char_position = sum(len(line) for line in lines[: match_line_number - 1])
        char_position += char_offset

        # Calculate snippet boundaries (centered on match)
        half_snippet = snippet_chars // 2
        start_pos = max(0, char_position - half_snippet)
        end_pos = min(
            len(full_content), char_position + match_length + half_snippet
        )

        # Extract raw snippet
        snippet = full_content[start_pos:end_pos]

        # Smart boundary adjustment - don't cut words awkwardly
        # Adjust start boundary
        if start_pos > 0 and snippet:
            # Find first whitespace or newline to start from
            whitespace_chars = {' ', chr(10), chr(9)}  # space, newline, tab
            for i, char in enumerate(snippet[:50]):  # Look within first 50 chars
                if char in whitespace_chars:
                    snippet = snippet[i + 1 :]
                    start_pos += i + 1
                    break

        # Adjust end boundary
        if end_pos < len(full_content) and snippet:
            # Find last whitespace or newline to end at
            whitespace_chars = {' ', chr(10), chr(9)}  # space, newline, tab
            for i in range(len(snippet) - 1, max(0, len(snippet) - 50), -1):
                if snippet[i] in whitespace_chars:
                    snippet = snippet[: i + 1]
                    break

        # Add ellipsis indicators
        leading_ellipsis = ""
        trailing_ellipsis = ""
        
        if start_pos > 0:
            leading_ellipsis = "..."
            snippet = leading_ellipsis + snippet
        
        if end_pos < len(full_content):
            trailing_ellipsis = "..."
            snippet = snippet + trailing_ellipsis

        # Calculate match position within the snippet
        match_start_in_snippet = char_position - start_pos + len(leading_ellipsis)
        match_end_in_snippet = match_start_in_snippet + match_length

        return snippet, match_start_in_snippet, match_end_in_snippet

    async def search(
        self,
        workspace_id: str,
        query: str,
        max_results: int = 50,
        context_lines: int = 3,
        snippet_chars: int = 0,
    ) -> WikiSearchResponse:
        """
        Search wiki content with context extraction.

        Performs full-text search across all markdown files in the wiki.
        Returns matched files with highlighted snippets and configurable context.

        Args:
            workspace_id: Workspace identifier
            query: Search query string
            max_results: Maximum number of results to return (1-100)
            context_lines: Number of lines to fetch before/after each match (0-10)
            snippet_chars: Number of characters to extract around match (0-5000, 0=disabled)
            snippet_chars: Number of characters to extract around match (0-5000, 0=disabled)

        Returns:
            Search response with results and context

        Raises:
            NotFoundError: If workspace not found
            PermissionDeniedError: If user lacks access
            ValidationError: If query is invalid
            MoguAPIError: On other API errors
        """
        # Validate parameters
        if max_results < 1 or max_results > 100:
            raise ValueError("max_results must be between 1 and 100")
        if context_lines < 0 or context_lines > 10:
            raise ValueError("context_lines must be between 0 and 10")
        if snippet_chars < 0 or snippet_chars > 5000:
            raise ValueError("snippet_chars must be between 0 and 5000")
        if snippet_chars < 0 or snippet_chars > 5000:
            raise ValueError("snippet_chars must be between 0 and 5000")

        response = await self._client.get(
            f"/api/v1/wiki/workspaces/{workspace_id}/search",
            params={"query": query, "max_results": max_results},
        )

        data = response.json()

        # Process results and add context extraction
        results = []
        for result_data in data["results"]:
            # Fetch full file content to extract context
            try:
                file_content = await self.get_content(
                    workspace_id=workspace_id,
                    path=result_data["path"],
                )
                content_lines = file_content.content.splitlines()

                # If backend didn't provide matches, search for them in content
                backend_matches = result_data["matches"]
                if not backend_matches:
                    # Search for query in content and create matches
                    query_lower = query.lower()
                    for line_idx, line in enumerate(content_lines):
                        line_lower = line.lower()
                        offset = 0
                        while True:
                            pos = line_lower.find(query_lower, offset)
                            if pos == -1:
                                break
                            
                            # Create a match entry
                            backend_matches.append({
                                "line_number": line_idx + 1,
                                "line_content": line,
                                "char_offset": pos,
                                "length": len(query),
                            })
                            offset = pos + 1

                # Enhance matches with context
                matches = []
                for match_data in backend_matches:
                    line_number = match_data["line_number"]

                    # Extract context lines
                    context_before = []
                    context_after = []

                    if context_lines > 0:
                        # Lines before (line_number is 1-indexed)
                        start_idx = max(0, line_number - 1 - context_lines)
                        context_before = content_lines[start_idx : line_number - 1]

                        # Lines after
                        end_idx = min(len(content_lines), line_number + context_lines)
                        context_after = content_lines[line_number:end_idx]

                    # Extract text snippet if requested
                    text_snippet = None
                    snippet_match_start = None
                    snippet_match_end = None

                    if snippet_chars > 0:
                        text_snippet, snippet_match_start, snippet_match_end = (
                            self._extract_snippet(
                                full_content=file_content.content,
                                match_line_number=match_data["line_number"],
                                char_offset=match_data["char_offset"],
                                match_length=match_data["length"],
                                snippet_chars=snippet_chars,
                            )
                        )

                    match = WikiSearchMatch(
                        line_number=match_data["line_number"],
                        line_content=match_data["line_content"],
                        char_offset=match_data["char_offset"],
                        length=match_data["length"],
                        context_before=context_before if context_before else None,
                        context_after=context_after if context_after else None,
                        text_snippet=text_snippet,
                        snippet_match_start=snippet_match_start,
                        snippet_match_end=snippet_match_end,
                    )
                    matches.append(match)

                result = WikiSearchResult(
                    path=result_data["path"],
                    name=result_data["name"],
                    matches=matches,
                    score=result_data["score"],
                )
                results.append(result)

            except Exception:
                # If context extraction fails, return match without context
                matches = [WikiSearchMatch(**m) for m in result_data["matches"]]
                result = WikiSearchResult(
                    path=result_data["path"],
                    name=result_data["name"],
                    matches=matches,
                    score=result_data["score"],
                )
                results.append(result)

        return WikiSearchResponse(
            results=results,
            total_count=len(results),
            query=query,
        )

    def _transform_query(self, user_query: str) -> Tuple[List[str], List[str]]:
        """
        Transform a natural language query into Azure DevOps search-friendly queries.
        
        Azure DevOps search supports:
        - Keywords: single words
        - Wildcards: * (multiple chars), ? (single char)
        - Boolean: AND, OR, NOT (must be uppercase)
        - Exact phrase: "quoted phrase"
        
        This method generates multiple query variations to maximize search results.
        
        Args:
            user_query: Natural language or keyword query from user
            
        Returns:
            Tuple of (search_queries, raw_keywords):
            - search_queries: List of Azure DevOps search query variations to try
            - raw_keywords: List of raw keywords (without wildcards) for snippet extraction
        """
        queries: List[str] = []
        cleaned = user_query.strip()
        
        # Check if it already looks like an Azure DevOps query (has operators)
        has_operators = any(op in cleaned.upper() for op in [' AND ', ' OR ', ' NOT '])
        # Only consider wildcards for * (asterisk), not ? (question mark)
        # Reason: ? at end of word (like "numeric?") is usually punctuation in natural language
        # But * at end of word (like "avatar*") is almost always intentional wildcard
        has_wildcards = '*' in cleaned
        has_exact_phrase = cleaned.startswith('"') and cleaned.endswith('"')
        
        if has_operators or has_wildcards or has_exact_phrase:
            # Already formatted as Azure DevOps query, use as-is
            raw_keywords = re.findall(r'\b(\w+)\b', cleaned.replace('*', '').replace('?', ''))
            raw_keywords = [kw for kw in raw_keywords if kw.lower() not in _STOP_WORDS and len(kw) >= 2]
            return [cleaned], raw_keywords
        
        # Extract meaningful keywords from natural language
        cleaned = re.sub(r'[^\w\s_]', ' ', cleaned)
        words = cleaned.lower().split()
        keywords: List[str] = []
        
        for word in words:
            if word in _STOP_WORDS:
                continue
            if len(word) < 2 and word not in _ABBREVIATION_EXPANSIONS:
                continue
            keywords.append(word)
        
        if not keywords:
            return [user_query], [user_query]
        
        # Strategy 1: All keywords with wildcards joined by OR
        wildcard_keywords = [f"{kw}*" for kw in keywords]
        if len(wildcard_keywords) > 1:
            queries.append(" OR ".join(wildcard_keywords))
        
        # Strategy 2: All keywords with AND (more restrictive)
        if len(wildcard_keywords) > 1:
            queries.append(" AND ".join(wildcard_keywords))
        
        # Strategy 3: First keyword with wildcard
        if keywords:
            queries.append(f"{keywords[0]}*")
        
        # Strategy 4: Exact keywords joined by OR (no wildcards - for exact matches)
        if len(keywords) > 1:
            queries.append(" OR ".join(keywords))
        elif keywords:
            queries.append(keywords[0])
        
        # Strategy 5: Check for abbreviations and add expanded versions
        expanded_keywords: Set[str] = set()
        for kw in keywords:
            parts = kw.split('_')
            for part in parts:
                if part in _ABBREVIATION_EXPANSIONS:
                    expanded_keywords.add(_ABBREVIATION_EXPANSIONS[part])
                else:
                    expanded_keywords.add(part)
        
        if expanded_keywords and expanded_keywords != set(keywords):
            expanded_list = list(expanded_keywords)
            if len(expanded_list) > 1:
                queries.append(" OR ".join(f"{ew}*" for ew in expanded_list))
            else:
                queries.append(f"{expanded_list[0]}*")
        
        # Strategy 6: Try exact column name if it looks like one (contains underscore)
        for kw in keywords:
            if '_' in kw:
                queries.append(kw)
        
        # Remove duplicates while preserving order
        seen: Set[str] = set()
        unique_queries: List[str] = []
        for q in queries:
            if q not in seen:
                seen.add(q)
                unique_queries.append(q)
        
        # Build raw keywords list for snippet extraction
        raw_keywords_for_snippets = list(keywords)
        raw_keywords_for_snippets.extend(expanded_keywords)
        raw_keywords_for_snippets = list(set(raw_keywords_for_snippets))
        
        return unique_queries if unique_queries else [user_query], raw_keywords_for_snippets

    async def smart_search(
        self,
        workspace_id: str,
        query: str,
        max_results: int = 10,
        context_lines: int = 3,
    ) -> WikiSearchResponse:
        """
        Intelligent wiki search that handles natural language queries.
        
        This method automatically transforms natural language queries into
        Azure DevOps search format and uses a two-phase approach:
        
        1. Phase 1: Use wildcard queries to find matching pages
        2. Phase 2: Use raw keywords to extract meaningful snippets
        
        This solves the problem where wildcards find pages but break snippet
        extraction (since the SDK needs literal text match for snippets).
        
        Examples of queries you can use:
        - "customer_segment" (column name)
        - "what does cust_id mean" (natural language)
        - "patient data schema" (keywords)
        - "transaction type definition" (semantic search)
        
        Args:
            workspace_id: Workspace identifier
            query: Natural language or keyword search query
            max_results: Maximum number of results to return (1-100)
            context_lines: Number of context lines for matches (0-10)
            
        Returns:
            Search response with results and context snippets
            
        Raises:
            NotFoundError: If workspace not found
            PermissionDeniedError: If user lacks access
            MoguAPIError: On other API errors
        """
        # Transform query into search-friendly formats
        search_queries, raw_keywords = self._transform_query(query)
        
        logger.debug(f"Wiki smart_search: query='{query}'")
        logger.debug(f"  -> search_queries={search_queries}")
        logger.debug(f"  -> raw_keywords={raw_keywords}")
        
        found_paths: Set[str] = set()
        all_results: List[WikiSearchResult] = []
        
        # Phase 1: Find pages using wildcard queries (no context extraction needed)
        for search_query in search_queries:
            try:
                response = await self._client.get(
                    f"/api/v1/wiki/workspaces/{workspace_id}/search",
                    params={"query": search_query, "max_results": max_results},
                )
                data = response.json()
                
                for result_data in data.get("results", []):
                    path = result_data.get("path")
                    if path:
                        found_paths.add(path)
                
                # If we have enough pages, stop searching
                if len(found_paths) >= max_results:
                    break
            except Exception as ex:
                logger.warning(f"Wiki smart search phase 1 failed for query '{search_query}': {str(ex)}")
                continue
        
        if not found_paths:
            return WikiSearchResponse(results=[], total_count=0, query=query)
        
        # Phase 2: Use regex/grep to find matches in file content
        # This is more reliable than the search API for snippet extraction
        for path in list(found_paths)[:max_results]:
            
            # Phase 2.1: only check markdown file extensions
            if not path.lower().endswith(('.md', '.markdown', '.mdx')):
                continue

            try:
                # Fetch the full file content
                file_content = await self.get_content(
                    workspace_id=workspace_id,
                    path=path,
                )
                content_lines = file_content.content.splitlines()
                
                # Build regex pattern from raw keywords (case-insensitive)
                # Match any of the keywords
                pattern_parts = [re.escape(kw) for kw in raw_keywords if len(kw) >= 2]
                if not pattern_parts:
                    continue
                
                pattern = re.compile(
                    r'\b(' + '|'.join(pattern_parts) + r')\b',
                    re.IGNORECASE
                )
                
                matches: List[WikiSearchMatch] = []
                for line_idx, line in enumerate(content_lines):
                    line_number = line_idx + 1  # 1-indexed
                    
                    # Find all matches in this line
                    for match_obj in pattern.finditer(line):
                        # Extract context
                        context_before = []
                        context_after = []
                        
                        if context_lines > 0:
                            start_idx = max(0, line_idx - context_lines)
                            context_before = content_lines[start_idx:line_idx]
                            end_idx = min(len(content_lines), line_idx + 1 + context_lines)
                            context_after = content_lines[line_idx + 1:end_idx]
                        
                        match = WikiSearchMatch(
                            line_number=line_number,
                            line_content=line,
                            char_offset=match_obj.start(),
                            length=match_obj.end() - match_obj.start(),
                            context_before=context_before if context_before else None,
                            context_after=context_after if context_after else None,
                        )
                        matches.append(match)
                        
                        # Limit matches per file to avoid too many results
                        if len(matches) >= 10:
                            break
                    
                    if len(matches) >= 10:
                        break
                
                if matches:
                    # Calculate a simple relevance score based on match count
                    score = min(1.0, len(matches) / 5.0)
                    
                    result = WikiSearchResult(
                        path=path,
                        name=path.split('/')[-1],
                        matches=matches,
                        score=score,
                    )
                    all_results.append(result)
                    
            except Exception as ex:
                logger.warning(f"Wiki smart search phase 2 failed for file '{path}': {str(ex)}")
                continue
        
        # Sort results by score (most matches first)
        all_results.sort(key=lambda r: r.score, reverse=True)
        
        return WikiSearchResponse(
            results=all_results[:max_results],
            total_count=len(all_results),
            query=query,
        )
