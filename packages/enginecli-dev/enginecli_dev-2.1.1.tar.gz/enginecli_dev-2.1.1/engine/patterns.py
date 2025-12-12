"""
Pattern Manager - Manages team-shared code patterns.

Patterns are architectural templates that ensure team consistency:
- Stored centrally on the API (namespaced by team)
- Cached locally for fast access
- Integrated with RAG for semantic retrieval
- Injected into prompts during generation
"""
import json
import hashlib
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


@dataclass
class PatternRule:
    """A rule that must be followed when using a pattern."""
    description: str
    severity: str = "required"  # required, recommended, optional
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "PatternRule":
        return cls(**data)


@dataclass
class Pattern:
    """
    A code pattern definition.
    
    Patterns consist of:
    - Metadata (name, description, language)
    - Template code (the actual pattern implementation)
    - Rules (requirements for using the pattern)
    """
    id: str
    name: str
    description: str
    language: str
    template: str  # The actual code template
    rules: List[PatternRule] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    created_by: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    version: int = 1
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "language": self.language,
            "template": self.template,
            "rules": [r.to_dict() for r in self.rules],
            "tags": self.tags,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "version": self.version,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Pattern":
        rules = [PatternRule.from_dict(r) for r in data.get("rules", [])]
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            language=data["language"],
            template=data["template"],
            rules=rules,
            tags=data.get("tags", []),
            created_by=data.get("created_by"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            version=data.get("version", 1),
        )
    
    def content_hash(self) -> str:
        """Generate hash of pattern content for versioning."""
        content = f"{self.template}{json.dumps([r.to_dict() for r in self.rules])}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def format_for_prompt(self) -> str:
        """Format pattern for injection into LLM prompt."""
        rules_text = "\n".join(
            f"  - [{r.severity.upper()}] {r.description}"
            for r in self.rules
        )
        
        return f"""### Pattern: {self.name}
**Description:** {self.description}
**Language:** {self.language}

**Rules:**
{rules_text}

**Template:**
```{self.language}
{self.template}
```
"""


@dataclass
class PatternLibrary:
    """
    Collection of patterns for a team.
    """
    team_id: Optional[str] = None
    patterns: List[Pattern] = field(default_factory=list)
    version_hash: str = ""
    last_synced: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "team_id": self.team_id,
            "patterns": [p.to_dict() for p in self.patterns],
            "version_hash": self.version_hash,
            "last_synced": self.last_synced,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "PatternLibrary":
        patterns = [Pattern.from_dict(p) for p in data.get("patterns", [])]
        return cls(
            team_id=data.get("team_id"),
            patterns=patterns,
            version_hash=data.get("version_hash", ""),
            last_synced=data.get("last_synced"),
        )
    
    def compute_version_hash(self) -> str:
        """Compute hash of all patterns for sync checking."""
        content = json.dumps(
            sorted([p.content_hash() for p in self.patterns])
        )
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def get_pattern(self, pattern_id: str) -> Optional[Pattern]:
        """Get pattern by ID."""
        for p in self.patterns:
            if p.id == pattern_id:
                return p
        return None
    
    def get_patterns_by_language(self, language: str) -> List[Pattern]:
        """Get all patterns for a language."""
        return [p for p in self.patterns if p.language == language]
    
    def get_patterns_by_tag(self, tag: str) -> List[Pattern]:
        """Get all patterns with a specific tag."""
        return [p for p in self.patterns if tag in p.tags]
    
    def search_patterns(self, query: str) -> List[Pattern]:
        """Search patterns by name, description, or tags."""
        query_lower = query.lower()
        results = []
        
        for p in self.patterns:
            score = 0
            if query_lower in p.name.lower():
                score += 3
            if query_lower in p.description.lower():
                score += 2
            if any(query_lower in tag.lower() for tag in p.tags):
                score += 1
            
            if score > 0:
                results.append((score, p))
        
        # Sort by score descending
        results.sort(key=lambda x: x[0], reverse=True)
        return [p for _, p in results]


class PatternManager:
    """
    Manages pattern storage, sync, and retrieval.
    """
    
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.patterns_dir = project_dir / ".engine" / "patterns"
        self.library_file = self.patterns_dir / "library.json"
        self.local_patterns_file = self.patterns_dir / "local.json"
        
        # Ensure directories exist
        self.patterns_dir.mkdir(parents=True, exist_ok=True)
    
    def load_library(self) -> PatternLibrary:
        """Load pattern library from cache."""
        if not self.library_file.exists():
            return PatternLibrary()
        
        try:
            with open(self.library_file) as f:
                data = json.load(f)
            return PatternLibrary.from_dict(data)
        except (json.JSONDecodeError, IOError):
            return PatternLibrary()
    
    def save_library(self, library: PatternLibrary):
        """Save pattern library to cache."""
        library.version_hash = library.compute_version_hash()
        library.last_synced = datetime.utcnow().isoformat()
        
        with open(self.library_file, "w") as f:
            json.dump(library.to_dict(), f, indent=2)
    
    def load_local_patterns(self) -> List[Pattern]:
        """Load local (non-synced) patterns."""
        if not self.local_patterns_file.exists():
            return []
        
        try:
            with open(self.local_patterns_file) as f:
                data = json.load(f)
            return [Pattern.from_dict(p) for p in data.get("patterns", [])]
        except (json.JSONDecodeError, IOError):
            return []
    
    def save_local_pattern(self, pattern: Pattern):
        """Save a local pattern."""
        patterns = self.load_local_patterns()
        
        # Update or add
        existing_idx = None
        for i, p in enumerate(patterns):
            if p.id == pattern.id:
                existing_idx = i
                break
        
        if existing_idx is not None:
            patterns[existing_idx] = pattern
        else:
            patterns.append(pattern)
        
        with open(self.local_patterns_file, "w") as f:
            json.dump({"patterns": [p.to_dict() for p in patterns]}, f, indent=2)
    
    def delete_local_pattern(self, pattern_id: str) -> bool:
        """Delete a local pattern."""
        patterns = self.load_local_patterns()
        new_patterns = [p for p in patterns if p.id != pattern_id]
        
        if len(new_patterns) == len(patterns):
            return False
        
        with open(self.local_patterns_file, "w") as f:
            json.dump({"patterns": [p.to_dict() for p in new_patterns]}, f, indent=2)
        
        return True
    
    def get_all_patterns(self, language: Optional[str] = None) -> List[Pattern]:
        """Get all patterns (library + local), optionally filtered by language."""
        library = self.load_library()
        local = self.load_local_patterns()
        
        all_patterns = library.patterns + local
        
        if language:
            all_patterns = [p for p in all_patterns if p.language == language]
        
        return all_patterns
    
    def find_relevant_patterns(
        self,
        task: str,
        language: str,
        max_patterns: int = 3,
    ) -> List[Pattern]:
        """
        Find patterns relevant to a task.
        
        Uses keyword matching for now; can be enhanced with RAG.
        """
        patterns = self.get_all_patterns(language)
        
        if not patterns:
            return []
        
        # Score each pattern by relevance
        task_lower = task.lower()
        scored = []
        
        for pattern in patterns:
            score = 0
            
            # Check name
            for word in pattern.name.lower().split():
                if word in task_lower:
                    score += 3
            
            # Check description
            for word in pattern.description.lower().split():
                if len(word) > 3 and word in task_lower:
                    score += 1
            
            # Check tags
            for tag in pattern.tags:
                if tag.lower() in task_lower:
                    score += 2
            
            if score > 0:
                scored.append((score, pattern))
        
        # Sort by score and return top N
        scored.sort(key=lambda x: x[0], reverse=True)
        return [p for _, p in scored[:max_patterns]]
    
    def format_patterns_for_prompt(
        self,
        patterns: List[Pattern],
    ) -> str:
        """Format patterns for injection into system prompt."""
        if not patterns:
            return ""
        
        sections = [
            "## TEAM ARCHITECTURAL PATTERNS",
            "",
            "You MUST follow these team-defined patterns when generating code.",
            "If a pattern is relevant to the task, use it as the foundation.",
            "Always add a comment indicating which pattern was used.",
            "",
        ]
        
        for pattern in patterns:
            sections.append(pattern.format_for_prompt())
            sections.append("")
        
        return "\n".join(sections)


# ============================================================
# Built-in Pattern Templates
# ============================================================

BUILTIN_PATTERNS = {
    "fastapi-endpoint": Pattern(
        id="builtin-fastapi-endpoint",
        name="FastAPI Endpoint",
        description="Standard FastAPI endpoint with error handling and OpenAPI docs",
        language="python",
        template='''from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class ItemCreate(BaseModel):
    """Request model for creating an item."""
    name: str
    description: Optional[str] = None


class ItemResponse(BaseModel):
    """Response model for an item."""
    id: int
    name: str
    description: Optional[str]


@router.post("/items", response_model=ItemResponse, status_code=201)
async def create_item(
    item: ItemCreate,
    # db: AsyncSession = Depends(get_db),  # Uncomment for DB
):
    """
    Create a new item.
    
    - **name**: The item name (required)
    - **description**: Optional description
    """
    try:
        # Implementation here
        return ItemResponse(id=1, name=item.name, description=item.description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
''',
        rules=[
            PatternRule("Use Pydantic models for request/response validation", "required"),
            PatternRule("Include OpenAPI docstrings with parameter descriptions", "required"),
            PatternRule("Use HTTPException for error responses", "required"),
            PatternRule("Return appropriate status codes (201 for create, 200 for get)", "required"),
            PatternRule("Use async def for all endpoints", "recommended"),
        ],
        tags=["api", "endpoint", "rest", "crud"],
    ),
    
    "react-component": Pattern(
        id="builtin-react-component",
        name="React Functional Component",
        description="Standard React component with TypeScript, hooks, and proper typing",
        language="typescript",
        template='''import React, { useState, useEffect } from 'react';

interface ComponentNameProps {
  /** Required prop description */
  title: string;
  /** Optional prop with default */
  variant?: 'primary' | 'secondary';
  /** Callback function */
  onAction?: () => void;
}

/**
 * ComponentName - Brief description of what this component does.
 * 
 * @example
 * <ComponentName title="Hello" variant="primary" />
 */
export const ComponentName: React.FC<ComponentNameProps> = ({
  title,
  variant = 'primary',
  onAction,
}) => {
  const [state, setState] = useState<string>('');

  useEffect(() => {
    // Effect logic here
  }, []);

  const handleClick = () => {
    onAction?.();
  };

  return (
    <div className={`component-name component-name--${variant}`}>
      <h2>{title}</h2>
      <button onClick={handleClick}>
        Action
      </button>
    </div>
  );
};

export default ComponentName;
''',
        rules=[
            PatternRule("Use TypeScript interfaces for props", "required"),
            PatternRule("Include JSDoc comments with @example", "required"),
            PatternRule("Use React.FC for type annotation", "required"),
            PatternRule("Provide default values for optional props", "recommended"),
            PatternRule("Use semantic HTML elements", "recommended"),
            PatternRule("Export both named and default exports", "optional"),
        ],
        tags=["react", "component", "typescript", "frontend"],
    ),
    
    "service-class": Pattern(
        id="builtin-service-class",
        name="Service Class",
        description="Python service class with dependency injection and error handling",
        language="python",
        template='''"""
Service module for handling business logic.
"""
from typing import Optional, List
from dataclasses import dataclass

from app.db.models import Entity
from app.core.exceptions import NotFoundError, ValidationError


@dataclass
class EntityDTO:
    """Data transfer object for Entity."""
    id: int
    name: str
    status: str


class EntityService:
    """
    Service for managing Entity operations.
    
    Handles business logic separate from API layer.
    """
    
    def __init__(self, db_session, cache=None):
        """
        Initialize service with dependencies.
        
        Args:
            db_session: Database session for persistence
            cache: Optional cache client for performance
        """
        self.db = db_session
        self.cache = cache
    
    async def get_by_id(self, entity_id: int) -> EntityDTO:
        """
        Get entity by ID.
        
        Args:
            entity_id: The entity identifier
            
        Returns:
            EntityDTO with entity data
            
        Raises:
            NotFoundError: If entity doesn't exist
        """
        # Check cache first
        if self.cache:
            cached = await self.cache.get(f"entity:{entity_id}")
            if cached:
                return EntityDTO(**cached)
        
        entity = await self.db.get(Entity, entity_id)
        if not entity:
            raise NotFoundError(f"Entity {entity_id} not found")
        
        return EntityDTO(
            id=entity.id,
            name=entity.name,
            status=entity.status,
        )
    
    async def create(self, name: str, **kwargs) -> EntityDTO:
        """
        Create a new entity.
        
        Args:
            name: Entity name
            **kwargs: Additional entity attributes
            
        Returns:
            EntityDTO of created entity
            
        Raises:
            ValidationError: If validation fails
        """
        if not name or len(name) < 2:
            raise ValidationError("Name must be at least 2 characters")
        
        entity = Entity(name=name, **kwargs)
        self.db.add(entity)
        await self.db.flush()
        
        return EntityDTO(
            id=entity.id,
            name=entity.name,
            status=entity.status,
        )
''',
        rules=[
            PatternRule("Use dependency injection for db_session and external services", "required"),
            PatternRule("Define DTOs for data transfer between layers", "required"),
            PatternRule("Raise domain-specific exceptions (NotFoundError, ValidationError)", "required"),
            PatternRule("Include comprehensive docstrings with Args, Returns, Raises", "required"),
            PatternRule("Implement caching for frequently accessed data", "recommended"),
            PatternRule("Keep business logic in service layer, not in API routes", "required"),
        ],
        tags=["service", "business-logic", "backend", "crud"],
    ),
    
    "custom-hook": Pattern(
        id="builtin-custom-hook",
        name="React Custom Hook",
        description="Custom React hook with TypeScript, loading states, and error handling",
        language="typescript",
        template='''import { useState, useEffect, useCallback } from 'react';

interface UseDataOptions {
  /** Enable automatic fetching on mount */
  autoFetch?: boolean;
  /** Refetch interval in milliseconds */
  refetchInterval?: number;
}

interface UseDataResult<T> {
  data: T | null;
  isLoading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

/**
 * useData - Custom hook for fetching and managing data.
 * 
 * @param fetchFn - Async function that returns data
 * @param options - Hook configuration options
 * @returns Object with data, loading state, error, and refetch function
 * 
 * @example
 * const { data, isLoading, error, refetch } = useData(
 *   () => api.getUsers(),
 *   { autoFetch: true }
 * );
 */
export function useData<T>(
  fetchFn: () => Promise<T>,
  options: UseDataOptions = {}
): UseDataResult<T> {
  const { autoFetch = true, refetchInterval } = options;
  
  const [data, setData] = useState<T | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const refetch = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const result = await fetchFn();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setIsLoading(false);
    }
  }, [fetchFn]);

  useEffect(() => {
    if (autoFetch) {
      refetch();
    }
  }, [autoFetch, refetch]);

  useEffect(() => {
    if (!refetchInterval) return;
    
    const interval = setInterval(refetch, refetchInterval);
    return () => clearInterval(interval);
  }, [refetchInterval, refetch]);

  return { data, isLoading, error, refetch };
}
''',
        rules=[
            PatternRule("Use TypeScript generics for type-safe data handling", "required"),
            PatternRule("Return loading, error, and data states", "required"),
            PatternRule("Include a refetch function for manual refresh", "required"),
            PatternRule("Use useCallback for stable function references", "required"),
            PatternRule("Clean up side effects (intervals, subscriptions) in useEffect", "required"),
            PatternRule("Include JSDoc with @example for usage documentation", "recommended"),
        ],
        tags=["react", "hook", "typescript", "data-fetching"],
    ),
}


def get_builtin_patterns() -> List[Pattern]:
    """Get all built-in patterns."""
    return list(BUILTIN_PATTERNS.values())


def get_builtin_pattern(pattern_id: str) -> Optional[Pattern]:
    """Get a specific built-in pattern."""
    return BUILTIN_PATTERNS.get(pattern_id.replace("builtin-", ""))
