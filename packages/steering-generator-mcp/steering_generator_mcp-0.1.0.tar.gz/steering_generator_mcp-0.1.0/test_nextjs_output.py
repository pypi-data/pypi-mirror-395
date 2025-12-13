"""Test script to show generated steering docs with simulated Next.js data."""
from steering_generator.generator import generate_steering_docs_deep
import os

# Simulated deep analysis data (seperti hasil dari Next.js project)
mock_deep_analysis = {
    "framework": "nextjs",
    "projectPath": "D:/projects/my-nextjs-app",
    
    # Scripts
    "scripts": {
        "dev": "next dev",
        "build": "next build",
        "start": "next start",
        "lint": "next lint",
        "test": "vitest"
    },
    
    # Env vars
    "envVars": [
        "NEXT_PUBLIC_SUPABASE_URL",
        "NEXT_PUBLIC_SUPABASE_ANON_KEY",
        "SUPABASE_SERVICE_ROLE_KEY",
        "NEXT_PUBLIC_APP_URL",
    ],
    
    # Components
    "components": [
        "Button", "Card", "Dialog", "Input", "Select",
        "UserProfile", "Dashboard", "Sidebar", "Header"
    ],
    
    # Categorized dependencies
    "categorizedDependencies": {
        "Framework": [
            {"name": "next", "purpose": "Next.js - React framework with SSR/SSG"},
            {"name": "react", "purpose": "React - UI library"},
            {"name": "next-themes", "purpose": "next-themes - Theme management"},
        ],
        "Database": [
            {"name": "@supabase/supabase-js", "purpose": "Supabase - PostgreSQL backend"},
            {"name": "@supabase/ssr", "purpose": "Supabase SSR helpers"},
        ],
        "UI & Styling": [
            {"name": "tailwindcss", "purpose": "Tailwind CSS - Utility-first CSS"},
            {"name": "@radix-ui/react-dialog", "purpose": "Radix UI component"},
            {"name": "@radix-ui/react-dropdown-menu", "purpose": "Radix UI component"},
            {"name": "@radix-ui/react-select", "purpose": "Radix UI component"},
            {"name": "@radix-ui/react-tabs", "purpose": "Radix UI component"},
            {"name": "@radix-ui/react-tooltip", "purpose": "Radix UI component"},
            {"name": "@radix-ui/react-popover", "purpose": "Radix UI component"},
            {"name": "lucide-react", "purpose": "Lucide - Icon library"},
        ],
        "Forms": [
            {"name": "react-hook-form", "purpose": "React Hook Form - Form handling"},
            {"name": "zod", "purpose": "Zod - Schema validation"},
            {"name": "@hookform/resolvers", "purpose": "Form validation resolvers"},
        ],
        "State": [
            {"name": "zustand", "purpose": "Zustand - Lightweight state"},
        ],
        "Data Fetching": [
            {"name": "@tanstack/react-query", "purpose": "TanStack Query - Server state"},
        ],
        "Utilities": [
            {"name": "date-fns", "purpose": "date-fns - Date utilities"},
            {"name": "clsx", "purpose": "clsx - Class name utility"},
        ],
        "Notifications": [
            {"name": "sonner", "purpose": "Sonner - Toast notifications"},
        ],
        "Charts": [
            {"name": "recharts", "purpose": "Recharts - Chart library"},
        ],
        "Other": [
            {"name": "geist", "purpose": ""},
        ]
    },
    
    # README info
    "readme": {
        "hasReadme": True,
        "title": "TaskFlow - Project Management App",
        "description": "A modern project management application built with Next.js and Supabase. Manage tasks, track progress, and collaborate with your team in real-time.",
        "features": [
            "Real-time task updates",
            "Kanban board view",
            "Team collaboration",
            "File attachments",
            "Activity timeline",
            "Dashboard analytics",
        ]
    },
    
    # Architecture patterns
    "architecturePatterns": {
        "stateManagement": "Zustand (lightweight stores)",
        "dataFetching": "TanStack Query (server state)",
        "authentication": "Supabase Auth",
        "styling": "Tailwind CSS (utility-first) + Radix UI primitives",
        "apiPattern": "Next.js Route Handlers (App Router)",
        "componentPattern": "React Context for state sharing + Custom hooks",
    },
    
    # Entities
    "entities": [
        {
            "name": "User",
            "extends": None,
            "fields": [
                {"name": "id", "type": "string", "optional": False},
                {"name": "email", "type": "string", "optional": False},
                {"name": "name", "type": "string", "optional": False},
                {"name": "avatar", "type": "string", "optional": True},
                {"name": "role", "type": "UserRole", "optional": False},
            ]
        },
        {
            "name": "Project",
            "extends": None,
            "fields": [
                {"name": "id", "type": "string", "optional": False},
                {"name": "name", "type": "string", "optional": False},
                {"name": "description", "type": "string", "optional": True},
                {"name": "status", "type": "ProjectStatus", "optional": False},
                {"name": "ownerId", "type": "string", "optional": False},
                {"name": "createdAt", "type": "Date", "optional": False},
            ]
        },
        {
            "name": "Task",
            "extends": None,
            "fields": [
                {"name": "id", "type": "string", "optional": False},
                {"name": "title", "type": "string", "optional": False},
                {"name": "description", "type": "string", "optional": True},
                {"name": "status", "type": "TaskStatus", "optional": False},
                {"name": "priority", "type": "Priority", "optional": False},
                {"name": "assigneeId", "type": "string", "optional": True},
                {"name": "projectId", "type": "string", "optional": False},
                {"name": "dueDate", "type": "Date", "optional": True},
            ]
        },
    ],
    
    # Status enums
    "statusEnums": [
        {"name": "TaskStatus", "values": ["backlog", "todo", "in_progress", "review", "done"]},
        {"name": "ProjectStatus", "values": ["active", "archived", "completed"]},
        {"name": "Priority", "values": ["low", "medium", "high", "urgent"]},
        {"name": "UserRole", "values": ["admin", "member", "viewer"]},
    ],
}

# Generate docs
docs = generate_steering_docs_deep(mock_deep_analysis, "kiro")

print(f"=== Generated {len(docs)} files ===\n")

# Save to output folder
os.makedirs("output", exist_ok=True)

for path, content in docs.items():
    filename = path.split("/")[-1]
    output_path = f"output/NEXTJS-{filename}"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"{'='*60}")
    print(f"FILE: {path}")
    print(f"{'='*60}")
    print(content)
    print("\n")

print("Files saved to output/ folder")
