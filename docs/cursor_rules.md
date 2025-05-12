# Cursor Rules in this project

This project uses [Cursor rules](https://docs.cursor.com/context/rules) to ensure consistent AI behavior
guidelines and workflow automation.

## How Cursor Rules Work
- Cursor rules are picked up and applied with each prompt, even during the same chat session. This means 
  that any changes to rule files will take effect immediately for subsequent prompts, without needing to 
  refresh or restart the chat.
- If you change or add `.mdc` rule files, you do **not** need to refresh your chat; the new or updated 
  rules will be respected on the next prompt.

## Rule Configuration and Usage

### Referencing Rules in Chat
- You can reference rules in chat by mentioning their purpose or topic
- For example: "Please follow our git commit message rules" or "Use our language preference rules"
- Rules are automatically applied based on context, even without explicit mention

### Automatic Rule Detection
- Rules can be automatically detected and applied based on the conversation context
- For example, when discussing git commits, the git commit message rules will be applied
- This works for any rule that matches the current topic or task

### Rule File Configuration
Each rule file (`.mdc`) should include a YAML frontmatter with these fields:

```yaml
---
description: A clear, concise explanation of what the rule does
globs: [optional] List of file patterns this rule applies to
alwaysApply: [optional] Set to true if the rule should always be active
---
```

Additional optional fields:
- `priority`: Number indicating rule importance (higher numbers = higher priority)
- `tags`: List of keywords for automatic rule detection
- `scope`: Can be "project", "directory", or "global"

Example:
```yaml
---
description: Guidelines for writing clear and consistent git commit messages
globs: ["*.md", "docs/**"]
alwaysApply: false
priority: 1
tags: ["git", "commit", "message"]
scope: "project"
---
```

## Location
- Project-wide rules are located in `.cursor/rules/`.
- Subdirectory-specific rules can be added in a `.cursor/rules/` folder within an existing subdirectory 
  (for example, `data_pipeline/.cursor/rules/`).

## Example of a project-wide rule
File: `.cursor/rules/english-only.mdc`
```mdc
---
description: Always answer in English and write code and code comments in English
globs: 
alwaysApply: true
---

- All answers must be in English.
- All code and code comments must be in English.
```

## Subdirectory-specific rules
If you want to add rules that only apply to a specific subdirectory, create a `.cursor/rules/` folder in 
that subdirectory and place your `.mdc` rule file there. This is only necessary if you want specific 
behavioral rules for that directory.

## Additional useful rules

### Markdown Documentation
- All markdown documentation must be clear, concise, and use proper formatting.
- Use headings, bullet points, and code blocks where appropriate.
- Always include a table of contents for documents longer than 100 lines.
- Use English for all documentation.

### Git Commit Messages
- Commit messages must be written in English.
- Use the imperative mood (e.g., "Add feature", "Fix bug").
- The first line should be a concise summary (max 120 characters).
- Optionally, add a blank line followed by a more detailed description.

### Thought Processes
- Clearly explain the reasoning behind decisions in comments or documentation.
- When suggesting changes, always provide a brief rationale.
- Document any assumptions or limitations relevant to the implementation.

### Insights from Responses
- Any insights, explanations, or important information from AI responses should be documented as project 
  documentation in the `docs/` folder or as inline comments in the relevant code files.

## More information
See the [official Cursor documentation](https://docs.cursor.com/context/rules) for more details and best 
practices.

## Editing Rules via Chat Settings
You can easily edit Cursor rules via the Chat Settings. Click on the three dots (...) in the top right of
the chat window, then select "Chat Settings". This allows you to modify or add rules without directly
editing the rule files.

## Different Rule Types in Markdown
Cursor rules can be defined in different ways:

- **Project-wide rules**: Located in `.cursor/rules/` and apply to the entire project.
- **Subdirectory-specific rules**: Located in a `.cursor/rules/` folder within a specific subdirectory and 
  apply only to that directory.
- **Global rules**: Applied across all projects and can be configured in the global Cursor settings.

## Language Preference Rule

File: `.cursor/rules/language-preference.mdc`

```mdc
---
description: Use Level B2 English for easy readability, with exceptions for jargon and technical terms,
and when explicitly asked to respond in a different language.
globs:
alwaysApply: true
---

- Use Level B2 English for easy readability, especially for non-native English speakers.
- Exceptions:
  * Jargon and technical terms with specific definitions and meaning.
  * When explicitly asked to respond in a different language.
- Apply the language preference in chat, documentation, generated code, and code comments.
- Prefer to store insights in project documentation and inline code comments over chat responses. If you 
  explain a piece of code, write this as inline code comments near the code, instead of in the chat. The 
  chat can then mention with a concise message that this edit will be made in code comments or project 
  documentation.
```
