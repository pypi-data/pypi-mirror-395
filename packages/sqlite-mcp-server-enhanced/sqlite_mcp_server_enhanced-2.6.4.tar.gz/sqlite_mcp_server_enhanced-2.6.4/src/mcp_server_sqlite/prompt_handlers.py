"""
MCP Prompt Handlers for SQLite MCP Server

This module contains the implementation of all MCP prompt handlers.
Separated from server.py to improve maintainability and organization.
"""

from mcp import types
import logging

logger = logging.getLogger(__name__)


def handle_semantic_query_prompt(arguments: dict[str, str] | None) -> types.GetPromptResult:
    """Handle the semantic_query prompt - Natural language → semantic search + SQL"""
    
    if not arguments or "user_question" not in arguments:
        logger.error("Missing required argument: user_question")
        raise ValueError("Missing required argument: user_question")
    
    user_question = arguments["user_question"]
    search_type = arguments.get("search_type", "hybrid")
    
    prompt_text = f"""# Semantic Query Workflow: "{user_question}"

I'll help you translate this natural language query into effective semantic search and SQL operations using the SQLite MCP server.

## Step-by-Step Approach

### 1. **Analyze the Question**
Let's break down your question: "{user_question}"

First, let me understand your database structure:
- Use the `list_tables` tool to see available tables
- Use `describe_table` for relevant tables to understand their schema
- Use `read_query` to examine sample data if needed

### 2. **Choose Search Strategy: {search_type.title()}**

**Search Approach:**
- **Keyword Search**: Fast, precise matching of specific terms
- **Semantic Search**: Contextual understanding, finds related concepts  
- **Hybrid**: Combines both approaches for comprehensive results

### 3. **Execute the Search**

Based on the question type, I'll help you:

**For Factual Queries:**
- Use `read_query` with precise SQL to find exact matches
- Filter and sort results based on your criteria

**For Semantic/Conceptual Queries:**
- Use `read_query` with LIKE patterns for text matching
- Consider using JSON operations if your data has JSON fields
- Look for related concepts and synonyms

### 4. **Refine and Validate**

- Review results for relevance and accuracy
- Adjust search terms or SQL conditions if needed
- Consider alternative approaches if results are insufficient

## Ready to Start?

Let's begin by examining your database structure. Please use the `list_tables` tool first, then we'll dive deeper into your specific question.
"""

    return types.GetPromptResult(
        description=f"Semantic query workflow for: {user_question}",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=prompt_text.strip())
            )
        ]
    )


def handle_summarize_table_prompt(arguments: dict[str, str] | None) -> types.GetPromptResult:
    """Handle the summarize_table prompt - Intelligent table analysis with statistics"""
    
    if not arguments or "table_name" not in arguments:
        logger.error("Missing required argument: table_name")
        raise ValueError("Missing required argument: table_name")
    
    table_name = arguments["table_name"]
    analysis_depth = arguments.get("analysis_depth", "basic")
    
    prompt_text = f"""# Table Analysis: {table_name}

Let's perform a {analysis_depth} analysis of the '{table_name}' table to understand its structure, content, and key characteristics.

## Analysis Workflow

### 1. **Schema Analysis**
First, let's examine the table structure:
```
Use the `describe_table` tool with table_name: {table_name}
```

### 2. **Basic Statistics**
Let's gather fundamental metrics:
```sql
-- Use read_query tool with these queries:
SELECT COUNT(*) as total_rows FROM {table_name};
```

### 3. **Data Profile Analysis**
Depending on the analysis depth ({analysis_depth}), we'll examine:
- **Basic**: Row counts, column types, sample data
- **Detailed**: Data distributions, null counts, unique values
- **Comprehensive**: Full statistical profiles, patterns, correlations

### 4. **Data Quality Assessment**
Let's check for data quality issues:
- NULL values in each column
- Duplicate records
- Outliers or unusual patterns

### 5. **Generate Summary Report**
Based on our analysis, I'll create a comprehensive summary with key insights and recommendations.

## Let's Begin!

Start by using the `describe_table` tool to examine the schema of '{table_name}'. Then we'll proceed with the statistical analysis based on what we discover.
"""

    return types.GetPromptResult(
        description=f"Table analysis workflow for {table_name} ({analysis_depth} depth)",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=prompt_text.strip())
            )
        ]
    )


def handle_optimize_database_prompt(arguments: dict[str, str] | None) -> types.GetPromptResult:
    """Handle the optimize_database prompt - Database optimization workflow"""
    
    optimization_focus = arguments.get("optimization_focus", "all") if arguments else "all"
    
    prompt_text = f"""# Database Optimization Workflow

Let's analyze and optimize your SQLite database with a focus on: **{optimization_focus}**

## Optimization Strategy

### 1. **Database Assessment**
First, let's understand your current database state:

```sql
-- Use read_query tool for these diagnostic queries:
PRAGMA page_size;
PRAGMA page_count;
PRAGMA freelist_count;

-- Analyze table statistics
SELECT name, sql FROM sqlite_master WHERE type='table';
```

### 2. **Performance Analysis**
Focus areas based on your selection ({optimization_focus}):
- **Performance**: Query execution times, index effectiveness
- **Storage**: Database size, page utilization, compression opportunities
- **Indexes**: Current indexes, missing indexes, redundant indexes
- **All**: Comprehensive analysis of all areas

### 3. **Index Optimization**
Let's examine and optimize indexes:
```sql
-- Current indexes
SELECT name, tbl_name, sql FROM sqlite_master WHERE type='index';
```

### 4. **Storage Optimization**
Identify space-saving opportunities:
```sql
-- Check table sizes
SELECT name, COUNT(*) as row_count FROM sqlite_master 
WHERE type='table' GROUP BY name;
```

### 5. **Maintenance Tasks**
Essential maintenance operations:
```sql
-- Vacuum to reclaim space
VACUUM;

-- Analyze statistics for query planner
ANALYZE;

-- Integrity check
PRAGMA integrity_check;
```

## Ready to Start?

Let's begin with the database assessment. Use the `read_query` tool to run the diagnostic queries above, and I'll analyze the results to provide targeted optimization recommendations.
"""

    return types.GetPromptResult(
        description=f"Database optimization workflow (focus: {optimization_focus})",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=prompt_text.strip())
            )
        ]
    )


def handle_setup_semantic_search_prompt(arguments: dict[str, str] | None) -> types.GetPromptResult:
    """Handle the setup_semantic_search prompt - Complete semantic search setup guide"""
    
    if not arguments or "content_type" not in arguments:
        logger.error("Missing required argument: content_type")
        raise ValueError("Missing required argument: content_type")
    
    content_type = arguments["content_type"]
    embedding_provider = arguments.get("embedding_provider", "openai")
    
    prompt_text = f"""# Semantic Search Setup Guide

Let's set up semantic search for your **{content_type}** content using **{embedding_provider}** embeddings.

## Setup Overview

Semantic search enables you to find content based on meaning rather than just keywords. We'll implement this using vector embeddings stored alongside your data.

### 1. **Database Schema Setup**

First, let's prepare your database for semantic search:

```sql
-- Use the write_query tool to create the necessary tables:

-- Create semantic search table:
CREATE TABLE IF NOT EXISTS {content_type}_embeddings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_id INTEGER,
    content_text TEXT NOT NULL,
    embedding_vector TEXT NOT NULL, -- JSON array of floats
    embedding_model TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster searches
CREATE INDEX IF NOT EXISTS idx_{content_type}_embeddings_content 
ON {content_type}_embeddings(content_text);
```

### 2. **Embedding Generation Strategy**

**{embedding_provider.title()} Setup:**
- Choose appropriate embedding model for your use case
- Consider dimensions vs. performance trade-offs
- Plan for consistent embedding generation
- Set up API credentials and rate limiting

### 3. **Content Preparation**

For **{content_type}** content, we need to:
- Extract and clean text content
- Split long content into appropriate chunks
- Preserve important metadata
- Ensure consistent text preprocessing

### 4. **Similarity Search Implementation**

```sql
-- Basic similarity search framework
-- (You'll need to implement vector similarity calculations)
SELECT 
    id,
    content_text,
    embedding_vector,
    -- Similarity calculation will go here
    1.0 as similarity_score
FROM {content_type}_embeddings
ORDER BY similarity_score DESC 
LIMIT 10;
```

### 5. **Integration with Existing Data**

Let's connect semantic search with your current database:
- Use `list_tables` tool to see current structure
- Use `describe_table` for your main content table
- Plan the integration strategy

### 6. **Testing and Validation**

We'll test the semantic search with:
- Exact match queries
- Conceptual queries
- Edge cases and performance testing

## Implementation Steps

**Ready to implement? Here's our action plan:**

1. **Examine Current Schema**: Use `list_tables` and `describe_table` tools
2. **Create Embedding Tables**: Use `write_query` to set up the schema
3. **Prepare Sample Data**: Identify content to embed first
4. **Set Up Embedding Pipeline**: Configure {embedding_provider} integration
5. **Test Semantic Queries**: Validate the search functionality

Let's start by examining your current database structure. Use the `list_tables` tool to see what we're working with!
"""

    return types.GetPromptResult(
        description=f"Semantic search setup for {content_type} using {embedding_provider}",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=prompt_text.strip())
            )
        ]
    )


def handle_hybrid_search_workflow_prompt(arguments: dict[str, str] | None) -> types.GetPromptResult:
    """Handle the hybrid_search_workflow prompt - Hybrid keyword + semantic search"""
    
    if not arguments or "use_case" not in arguments:
        logger.error("Missing required argument: use_case")
        raise ValueError("Missing required argument: use_case")
    
    use_case = arguments["use_case"]
    
    prompt_text = f"""# Hybrid Search Implementation: {use_case.replace('_', ' ').title()}

Let's implement a powerful hybrid search system that combines the precision of keyword search with the intelligence of semantic search for your **{use_case.replace('_', ' ')}** use case.

## Hybrid Search Architecture

### 1. **Understanding Hybrid Search**

Hybrid search combines two complementary approaches:
- **Keyword Search (FTS5)**: Fast, exact matches, good for specific terms
- **Semantic Search**: Contextual understanding, finds related concepts
- **Smart Ranking**: Combines and weights results from both methods

### 2. **Database Schema Setup**

Let's set up the optimal schema for hybrid search:

```sql
-- Use write_query tool for these schema changes:

-- Enable FTS5 for keyword search
CREATE VIRTUAL TABLE IF NOT EXISTS {use_case}_fts USING fts5(
    content_id,
    title,
    content,
    tags,
    metadata
);

-- Semantic embeddings table
CREATE TABLE IF NOT EXISTS {use_case}_embeddings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_id INTEGER NOT NULL,
    embedding_vector TEXT NOT NULL, -- JSON array
    embedding_model TEXT NOT NULL,
    chunk_text TEXT NOT NULL,
    chunk_index INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Main content table (if not exists)
CREATE TABLE IF NOT EXISTS {use_case}_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT,
    tags TEXT, -- JSON array
    metadata TEXT, -- JSON object
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 3. **Use Case Specific Implementation**

**{use_case.replace('_', ' ').title()} Optimization:**
- Tailored ranking factors for your specific use case
- Optimized search strategies
- Performance considerations
- User experience enhancements

### 4. **Hybrid Search Algorithm**

```sql
-- Step 1: Keyword Search (FTS5)
WITH keyword_results AS (
    SELECT 
        content_id,
        title,
        content,
        bm25({use_case}_fts) as keyword_score
    FROM {use_case}_fts 
    WHERE {use_case}_fts MATCH ?  -- Your search query
    ORDER BY keyword_score
    LIMIT 20
),

-- Step 2: Semantic Search Results  
semantic_results AS (
    SELECT 
        e.content_id,
        c.title,
        c.content,
        1.0 as semantic_score  -- Calculated similarity score
    FROM {use_case}_embeddings e
    JOIN {use_case}_content c ON e.content_id = c.id
    ORDER BY semantic_score DESC
    LIMIT 20
),

-- Step 3: Combine and Rank Results
combined_results AS (
    SELECT *, keyword_score * 0.6 + 0.0 * 0.4 as final_score FROM keyword_results
    UNION ALL
    SELECT *, 0.0 * 0.6 + semantic_score * 0.4 as final_score FROM semantic_results
)

-- Step 4: Final Ranking with Deduplication
SELECT 
    content_id,
    title,
    content,
    MAX(final_score) as relevance_score
FROM combined_results
GROUP BY content_id
ORDER BY relevance_score DESC
LIMIT 10;
```

### 5. **Implementation Workflow**

**Let's implement this step by step:**

1. **Database Assessment**: Use `list_tables` to see current structure
2. **Schema Migration**: Create FTS5 virtual table and embeddings table
3. **Data Population**: Populate with existing content
4. **Search Function Testing**: Test keyword, semantic, and hybrid searches
5. **Performance Optimization**: Add indexes and optimize queries

## Ready to Build?

Let's start by examining your current database structure and content. Use the `list_tables` tool first, then we'll proceed with the hybrid search implementation tailored to your {use_case.replace('_', ' ')} needs.

The hybrid approach will give you the best of both worlds: the speed and precision of keyword search combined with the intelligence of semantic understanding!
"""

    return types.GetPromptResult(
        description=f"Hybrid search workflow for {use_case.replace('_', ' ')} use case",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=prompt_text.strip())
            )
        ]
    )
