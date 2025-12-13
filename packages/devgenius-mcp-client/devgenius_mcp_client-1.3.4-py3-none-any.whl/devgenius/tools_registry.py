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
                "name": "create_milestone",
                "description": """Create a milestone with optional tasks in one operation. **RECOMMENDED** to create milestone with tasks together for better efficiency.

Use cases:
- Create milestone with planned tasks (RECOMMENDED): Provide both name and tasks
- Create milestone only: Provide just name, add tasks later using create_milestone_tasks

**IMPORTANT for tasks[].acceptance_criteria**:
- Use a SINGLE STRING (not array)
- System will automatically convert to list
- Use newlines (\\n) to separate multiple criteria

Example with tasks:
{
    "name": "Phase 1: Requirements",
    "description": "Requirement analysis phase",
    "tasks": [
        {
            "title": "User interviews",
            "description": "Conduct user research",
            "priority": "high",
            "acceptance_criteria": "Complete 10 interviews\\nCreate requirement doc"
        },
        {
            "title": "Competitor analysis",
            "priority": "medium"
        }
    ]
}

Returns milestone info and created tasks list.""",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Milestone name (required)"},
                        "description": {"type": "string", "description": "Milestone description (optional)"},
                        "tasks": {
                            "type": "array",
                            "description": "List of tasks to create with milestone (optional)",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string", "description": "Task title (required)"},
                                    "description": {"type": "string", "description": "Task description (optional)"},
                                    "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "Priority (optional, default: medium)"},
                                    "acceptance_criteria": {
                                        "type": "string",
                                        "description": "Acceptance criteria as a SINGLE STRING (optional). System will auto-convert to list. Use \\n to separate multiple criteria."
                                    }
                                },
                                "required": ["title"]
                            }
                        }
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "create_milestone_tasks",
                "description": """Batch create multiple tasks for a milestone. This is the RECOMMENDED way to create tasks.

**IMPORTANT**: This tool is designed for batch creation. Always create ALL tasks at once instead of one by one.

Use this to:
- Create all milestone tasks in one operation
- Automatically generate task IDs (M1-T1, M1-T2, etc.)
- Efficiently set up project tasks

Best practice:
- Analyze requirements and create a complete task list
- Submit all tasks in a single call
- System will auto-update milestone status

Returns list of created tasks with their IDs.""",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "milestone_id": {"type": "integer", "description": "Milestone ID"},
                        "tasks": {
                            "type": "array",
                            "description": "List of tasks to create",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string", "description": "Task title (required)"},
                                    "description": {"type": "string", "description": "Task description (optional)"},
                                    "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "Priority (optional, default: medium)"},
                                    "acceptance_criteria": {
                                        "type": "string", 
                                        "description": "Acceptance criteria as a single string (optional). System will automatically convert it to a list. Use newlines to separate multiple criteria if needed."
                                    }
                                },
                                "required": ["title"]
                            }
                        }
                    },
                    "required": ["milestone_id", "tasks"]
                }
            },
            {
                "name": "delete_milestone_task",
                "description": """Delete a milestone task. This will cascade delete all subtasks.

Use this to:
- Remove obsolete or incorrect tasks
- Clean up task list
- System will auto-update milestone status

**WARNING**: This action cannot be undone. All subtasks will also be deleted.

Returns success message.""",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "Task ID to delete"}
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "delete_milestone",
                "description": """Delete a milestone. This will cascade delete ALL tasks and subtasks in the milestone.

Use this to:
- Remove obsolete milestones
- Restructure project phases

**WARNING**: This action cannot be undone. All tasks and subtasks in this milestone will be permanently deleted.

Returns success message with deletion count.""",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "milestone_id": {"type": "integer", "description": "Milestone ID to delete"}
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
                "name": "list_project_tasks",
                "description": """List all project tasks with subtasks and technical implementation details. Perfect for learning from historical implementations and avoiding duplicate work.

Use cases:
- View completed tasks to learn implementations: {"status": "completed"}
- View tasks in a milestone: {"milestone_id": 1}
- Search for specific feature implementations: {"title_keyword": "authentication", "status": "completed"}
- Understand current work: {"status": "in_progress"}

Returns tasks with notes field containing technical details, subtasks, and implementation approaches.""",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["pending", "in_progress", "completed", "cancelled"],
                            "description": "Filter by task status (optional)"
                        },
                        "milestone_id": {
                            "type": "integer",
                            "description": "Filter by milestone ID (optional)"
                        },
                        "title_keyword": {
                            "type": "string",
                            "description": "Filter by title keyword (optional, supports fuzzy search)"
                        },
                        "include_subtasks": {
                            "type": "boolean",
                            "description": "Include subtask details (default: true)",
                            "default": True
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of tasks to return (default: 50, max: 100)",
                            "default": 50
                        }
                    }
                }
            },
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
                        "status": {"type": "string", "description": "New status", "enum": ["pending", "in_progress", "completed", "cancelled", "postponed"]},
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
                "description": "List documents in the project. Supports filtering by title keyword and category. Returns the latest 20 documents by default to avoid large responses.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title_keyword": {
                            "type": "string", 
                            "description": "Filter by title keyword (optional, supports fuzzy search). Example: 'API' will match 'API Documentation', 'User API Guide', etc."
                        },
                        "category": {
                            "type": "string", 
                            "description": "Filter by category code (optional). Use get_document_categories to see available categories."
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of documents to return (default: 20, max: 100)",
                            "default": 20
                        }
                    }
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
                "description": """Create a new document.

**IMPORTANT for filling required documents**:
- When creating documents to fill missing required documents (from get_project_context.document_completeness.missing_required), 
  you MUST pass the `template_id` parameter to properly mark the document as fulfilling the requirement.
- Get template_id from: missing_required[].template_id

Example for filling a required document:
{
    "title": "Product Requirements Document",
    "content": "# PRD\\n\\n## Overview\\n...",
    "category": "requirement",
    "template_id": 5  // from missing_required.template_id
}

Example for creating a regular document:
{
    "title": "API Design Notes",
    "content": "# API Notes\\n...",
    "category": "design"
}""",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Document title"},
                        "content": {"type": "string", "description": "Document content (Markdown format)"},
                        "category": {"type": "string", "description": "Category code (get from get_document_categories)"},
                        "template_id": {"type": "integer", "description": "Template ID - ONLY pass this when filling a MISSING required document. Get from missing_required[].template_id in get_project_context response. Do NOT pass for regular documents or if all required documents are complete."}
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
                "name": "delete_document_by_id",
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
