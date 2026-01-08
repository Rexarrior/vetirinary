# AI Admin Agent Architecture

## 1. Overview
The AI Admin Agent is a specialized module designed to perform database administration tasks and answer user queries by interacting with the project's data models. It operates as an autonomous agent capable of analyzing tasks, executing changes, verifying results, and reporting back to the user.

## 2. Core Architecture
The system is built on an asynchronous task execution model using **Celery**.
- **Single Task Execution**: Only one administrative task can be running at a time to prevent race conditions and ensure data integrity. New task requests while a task is running will be rejected.
- **Async Workflow**: All agent operations are encapsulated in Celery tasks.

## 3. Agent Workflow
The workflow consists of a chain of specialized agents, each responsible for a specific stage of the task.

### Workflow Stages:
1.  **Task Analysis** (`AnalysisAgent`)
2.  **Execution** (`AdminAgent`)
3.  **Control & Verification** (`ControlAgent`)
4.  **Reporting** (`DescriptionAgent`)
5.  **Response** (`ResponseAgent`)

### Data Flow
Control is passed between agents via Celery tasks. Each agent receives the current state (context) and the output of the previous agent.

## 4. Component Details

### 4.1. Task Analysis Agent (`AnalysisAgent`)
**Responsibilities:**
- Analyzes the incoming user request.
- Determines if the task is clear and actionable.
- Checks if sufficient data is available.
- **Tools/Access:**
    - **User History**: Access to chat history (paginated).
    - **Task Index**: Access to previous tasks (status, reports).
- **Decisions:**
    - **Clarification Needed**: Terminates flow, asks user for more info.
    - **Dialog Only**: Handles simple queries without DB changes.
    - **Proceed**: Formulates a structured task for the Admin Agent.

### 4.2. AI Admin Agent (`AdminAgent`)
**Responsibilities:**
- Executes the actual work on the database.
- **Tools/Access:**
    - **Model Introspection**: Access to all Django models and their schemas.
    - **CRUD Operations**: Tools to Create, Read, Update, Delete records.
    - **Web Search**: Ability to search the internet for external information if needed.
- **Constraints:**
    - No access to user chat history (privacy/separation of concerns).
    - Operates solely on the structured task from the Analysis Agent.
- **Outcomes:**
    - **Success**: Changes made and logged.
    - **Failure**: "Structure modification required" or "Conceptually impossible".

### 4.3. Control Agent (`ControlAgent`)
**Responsibilities:**
- Verifies the work done by the Admin Agent.
- **Decisions:**
    - **Approved**: Passes control to the Description Agent.
    - **Rejected**: Returns control to the Admin Agent with a list of fixes/refinements.

### 4.4. Description Agent (`DescriptionAgent`)
**Responsibilities:**
- Generates a detailed HTML report of the operation.
- **Tools/Access:**
    - **HTML Templates**: Uses Bootstrap 5 templates for consistent styling.
- **Output:**
    - Saves the report to a dedicated `TaskReport` model.
    - Generates a unique slug for the report (e.g., `task_name_date_time`).

### 4.5. Response Agent (`ResponseAgent`)
**Responsibilities:**
- Formulates the final text response to the user.
- **Tools/Access:**
    - **User History**: To maintain conversational context.
    - **Task Context**: Knows the task result and report link.
- **Output:**
    - A summary message to the user including a link to the detailed HTML report.

## 5. Security
- **Access Control**: All API endpoints for triggering or managing these agents must be protected.
    - Superuser authentication required.
    - Or valid API Key verification.

## 6. Data Models (New)
- **TaskLog**: Stores the lifecycle of a task (User request, Status, Current Agent).
- **TaskReport**: Stores the generated HTML reports.
