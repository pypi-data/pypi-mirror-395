"""
MCP 工具注册表

负责：
- 工具定义
- 工具列表管理
"""

from typing import Dict, Any, List


class ToolsRegistry:
    """MCP 工具注册表"""
    
    @staticmethod
    def get_all_tools() -> List[Dict[str, Any]]:
        """获取所有工具定义"""
        return [
            # 项目上下文
            {
                "name": "get_project_context",
                "description": "Get project context including basic info and current tasks",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "include_tasks": {
                            "type": "boolean",
                            "description": "Whether to include task list",
                            "default": True
                        }
                    }
                }
            },
            
            # 里程碑管理
            {
                "name": "list_project_milestones",
                "description": """Get project milestones list to understand project progress and current phase.

Use cases:
- View all milestones: {} (no parameters)
- View pending milestones: {"status": "pending"}
- View in-progress milestones: {"status": "in_progress"}
- View completed milestones: {"status": "completed"}

Returns milestone list with task statistics and progress.""",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["pending", "in_progress", "completed"],
                            "description": "Filter milestones by status. Leave empty to get all milestones."
                        }
                    }
                }
            },
            {
                "name": "get_milestone_detail",
                "description": """Get detailed information about a specific milestone, including all tasks.

Use this to:
- View milestone progress
- See all tasks in the milestone
- Choose tasks to claim

Returns milestone details with task list.""",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "milestone_id": {"type": "integer", "description": "Milestone ID"},
                        "include_tasks": {"type": "boolean", "description": "Include task list (default: true)", "default": True}
                    },
                    "required": ["milestone_id"]
                }
            },
            {
                "name": "get_task_detail",
                "description": """Get complete task information including subtasks and acceptance criteria.

Use this to:
- View full task details before claiming
- Check acceptance criteria
- See task dependencies and subtasks
- Understand task requirements

Returns comprehensive task information.""",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "Task ID (database primary key)"}
                    },
                    "required": ["task_id"]
                }
            },
            
            # 任务管理
            {
                "name": "get_my_tasks",
                "description": """Get my task list with optional status filter. Automatically filters tasks based on your role and assignment.

Use cases:
- Get all my tasks: {} (no parameters)
- Get my TODO/pending tasks: {"status_filter": "pending"}
- Get what I'm currently working on: {"status_filter": "in_progress"}
- Get my completed tasks: {"status_filter": "completed"}

The tool intelligently returns:
1. Tasks directly assigned to me
2. Tasks assigned to my role category
3. Full-stack tasks (if applicable)
4. Unassigned tasks (available to claim)""",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "status_filter": {
                            "type": "string",
                            "enum": ["pending", "in_progress", "completed", "cancelled"],
                            "description": "Filter tasks by status. Options: 'pending' (TODO), 'in_progress' (currently working on), 'completed', 'cancelled'. Leave empty to get all tasks."
                        }
                    }
                }
            },
            {
                "name": "claim_task",
                "description": "Claim a task and acquire lock (default 120 minutes)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "Task ID"},
                        "lock_duration_minutes": {"type": "integer", "description": "Lock duration in minutes", "default": 120}
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "update_task_status",
                "description": """Update task status with optimistic locking.

**IMPORTANT**: When updating status to 'completed', you **MUST** provide a brief summary report in the 'notes' parameter.

The summary should include:
- Main accomplishments
- Key changes made (files modified, features added)
- Problems encountered and solutions (if any)
- Testing status

Example: "Completed user login feature, including password authentication, JWT tokens, and remember-me functionality. Modified auth.py and login.vue. All tests passed."

This helps team members understand what was accomplished and provides valuable documentation.""",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "Task ID"},
                        "status": {"type": "string", "description": "New status", "enum": ["pending", "in_progress", "completed", "cancelled"]},
                        "version": {"type": "integer", "description": "Version number for optimistic locking"},
                        "notes": {"type": "string", "description": "Task notes. **REQUIRED when status='completed'** - provide a summary report of what was accomplished"}
                    },
                    "required": ["task_id", "status", "version"]
                }
            },
            {
                "name": "split_task_into_subtasks",
                "description": "Split a main task into multiple subtasks",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "Main task ID"},
                        "subtasks": {
                            "type": "array",
                            "description": "List of subtasks",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string", "description": "Subtask title"},
                                    "description": {"type": "string", "description": "Subtask description"},
                                    "estimated_hours": {"type": "number", "description": "Estimated hours"}
                                },
                                "required": ["title"]
                            }
                        }
                    },
                    "required": ["task_id", "subtasks"]
                }
            },
            
            # 子任务管理
            {
                "name": "get_task_subtasks",
                "description": "Get all subtasks of a task",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "Parent task ID"}
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "update_subtask_status",
                "description": """Update subtask status.

**IMPORTANT**: When updating status to 'completed', you **MUST** provide a brief summary report in the 'notes' parameter.

The summary should include:
- Main accomplishments
- Key changes made

Example: "Completed database table design, created users and sessions tables, added relevant indexes."

This helps track progress and provides documentation for the work done.""",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "subtask_id": {"type": "integer", "description": "Subtask ID"},
                        "status": {"type": "string", "description": "New status", "enum": ["pending", "in_progress", "completed", "cancelled"]},
                        "notes": {"type": "string", "description": "Subtask notes. **REQUIRED when status='completed'** - provide a summary report of what was accomplished"}
                    },
                    "required": ["subtask_id", "status"]
                }
            },
            
            # 文档管理
            {
                "name": "get_document_categories",
                "description": "Get all available document categories. Use this before creating a document to know which categories are available.",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "create_document_category",
                "description": "Create a new document category. Use this when system predefined categories don't meet your needs. Category code must be unique and use lowercase letters with underscores (e.g., 'custom_api').",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "Category code (unique identifier, e.g., 'custom_api')"
                        },
                        "name": {
                            "type": "string",
                            "description": "Category name (e.g., 'Custom API Documentation')"
                        },
                        "description": {
                            "type": "string",
                            "description": "Category description (optional)"
                        },
                        "icon": {
                            "type": "string",
                            "description": "Icon (emoji or icon class name, optional)"
                        },
                        "color": {
                            "type": "string",
                            "description": "Color for tag display (optional)"
                        },
                        "sort_order": {
                            "type": "integer",
                            "description": "Sort order (smaller number appears first, default: 0)"
                        }
                    },
                    "required": ["code", "name"]
                }
            },
            {
                "name": "list_documents",
                "description": "List all documents in the project",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "category_code": {"type": "string", "description": "Filter by category code (optional)"}
                    }
                }
            },
            {
                "name": "get_document_by_title",
                "description": "Get a document by its title",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Document title"}
                    },
                    "required": ["title"]
                }
            },
            {
                "name": "search_documents",
                "description": "Search documents by keyword",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search keyword"},
                        "category": {"type": "string", "description": "Category filter (optional)"},
                        "limit": {"type": "integer", "description": "Result limit (default: 10)"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "create_document",
                "description": "Create a new document. IMPORTANT: Use get_document_categories first to see available categories.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Document title"},
                        "content": {"type": "string", "description": "Document content (Markdown format)"},
                        "category": {"type": "string", "description": "Category code (get from get_document_categories)"},
                        "tags": {"type": "array", "items": {"type": "string"}, "description": "Document tags (optional)"}
                    },
                    "required": ["title", "content", "category"]
                }
            },
            {
                "name": "get_document_by_id",
                "description": "Get a document by ID (RECOMMENDED: avoids title duplication issues)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "document_id": {"type": "integer", "description": "Document ID (from list_documents)"}
                    },
                    "required": ["document_id"]
                }
            },
            {
                "name": "update_document",
                "description": "Update a document by title (creates new version)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Document title"},
                        "content": {"type": "string", "description": "New content"},
                        "change_summary": {"type": "string", "description": "Change summary (optional)"}
                    },
                    "required": ["title", "content"]
                }
            },
            {
                "name": "update_document_by_id",
                "description": "Update a document by ID (RECOMMENDED: avoids title duplication issues, creates new version)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "document_id": {"type": "integer", "description": "Document ID (from list_documents)"},
                        "content": {"type": "string", "description": "New content"},
                        "change_summary": {"type": "string", "description": "Change summary (optional)"}
                    },
                    "required": ["document_id", "content"]
                }
            },
            {
                "name": "delete_document",
                "description": "Delete a document by ID (RECOMMENDED: avoids title duplication issues)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "document_id": {"type": "integer", "description": "Document ID (from list_documents)"}
                    },
                    "required": ["document_id"]
                }
            },
            {
                "name": "get_document_versions",
                "description": "Get all versions of a document by title",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Document title"}
                    },
                    "required": ["title"]
                }
            },
            
            # Rules 管理
            {
                "name": "get_project_rules",
                "description": "Get project Rules configuration (auto-rendered with variables). Used by MCP Client for automatic synchronization.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "ide_type": {
                            "type": "string",
                            "description": "IDE type",
                            "enum": ["cursor", "windsurf", "vscode", "trae"],
                            "default": "cursor"
                        }
                    }
                }
            },
            {
                "name": "get_rules_content",
                "description": "Get project Rules content for AI to handle. Returns rendered Rules content without file writing. AI can decide how to use the content based on their own IDE specifications. Supports any IDE - no predefined list required.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "ide_type": {
                            "type": "string",
                            "description": "IDE type identifier (optional, e.g., 'cursor', 'windsurf', 'vscode', 'trae', or any custom IDE name). If not specified, returns generic Rules content."
                        }
                    }
                }
            }
        ]
