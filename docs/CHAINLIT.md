# Chainlit Documentation

## Purpose
This document explains how Chainlit is used in the Datacation Chatbot project, specifically focusing on the implementation of the chat interface and UI components. It serves as a project-specific guide and reference for developers working on this codebase.

## References
- [Chainlit Official Documentation](https://docs.chainlit.io/)
- [Chainlit GitHub Repository](https://github.com/chainlit/chainlit)
- [Chainlit Discord Community](https://discord.gg/chainlit)

## Overview
Chainlit is a framework for building conversational AI applications. It provides a modern UI for chat interfaces and integrates well with LangChain and other AI frameworks. This project uses Chainlit version 2.5.5.

## Project Requirements

### Version and Dependencies
```bash
# Update Chainlit and dependencies
uv add -U chainlit
```

### Available UI Components (Chainlit 2.5.5)

1. **Message Components**
   - `cl.Message`: [Main component for displaying chat messages](https://docs.chainlit.io/concepts/message-api)
     - Can contain multiple elements
     - Supports streaming updates
     - Can be referenced and updated
   - `cl.Text`: [For displaying text content](https://docs.chainlit.io/concepts/ui-components#text)
     - Can be used as standalone or within messages
     - Supports markdown formatting
   - `cl.Image`: [For displaying images](https://docs.chainlit.io/concepts/ui-components#image)
   - `cl.File`: [For file attachments](https://docs.chainlit.io/concepts/ui-components#file)
   - `cl.Pdf`: [For PDF documents](https://docs.chainlit.io/concepts/ui-components#pdf)

2. **Interactive Elements**
   - `cl.Action`: [For clickable actions/buttons](https://docs.chainlit.io/concepts/ui-components#action)
   - `cl.Select`: [For dropdown selections](https://docs.chainlit.io/concepts/ui-components#select)
   - `cl.Input`: [For text input fields](https://docs.chainlit.io/concepts/ui-components#input)

3. **Layout Components**
   - `cl.Message`: Can contain elements for structured content
   - `cl.Text`: Can be used for headers and sections
   - No native sidebar component available in 2.5.5

### Component Usage Examples

1. **Multiple Text Elements in a Message**
```python
# Create a message with multiple text elements
msg = cl.Message(
    content="**Analysis Results**",
    author="System",
    elements=[
        cl.Text(content="Input tokens: 100"),
        cl.Text(content="Output tokens: 50"),
        cl.Text(content="Total tokens: 150")
    ]
)
await msg.send()

# Update specific elements
msg.elements[0].content = "Input tokens: 200"
await msg.update()
```

2. **Referencing and Updating Messages**
```python
# Create and store reference to message
thinking_msg = cl.Message(content="**Thinking...**", author="Assistant")
await thinking_msg.send()

# Update the message later
await thinking_msg.update(content="**Thinking...**\nProcessing data...")

# Create multiple messages
status_msg = cl.Message(content="**Status**", author="System")
await status_msg.send()

# Update both messages
await thinking_msg.update(content="**Complete**")
await status_msg.update(content="**Analysis Finished**")
```

3. **Structured Content with Elements**
```python
# Create a message with structured content
await cl.Message(
    content="**Technical Details**",
    author="System",
    elements=[
        cl.Text(content="**Token Usage**"),
        cl.Text(content="Input: 100"),
        cl.Text(content="Output: 50"),
        cl.Text(content="**Tools Used**"),
        cl.Text(content="• pandas_analysis")
    ]
).send()
```

## Best Practices

1. **Message Organization**
   - Use markdown for formatting
   - Group related information in single messages
   - Use author attribution for semantic meaning
   - Keep technical details in separate messages

2. **Interactive Elements**
   - Use actions for common operations
   - Provide clear descriptions
   - Group related actions together
   - Use select dropdowns for multiple choices

3. **Progress Indicators**
   - Show thinking status
   - Update messages with progress
   - Use streaming for real-time updates
   - Clear status indicators

## Version-Specific Notes

### Chainlit 2.5.5
- No native sidebar component available
- Use message elements for structured content
- Actions and selects for interactivity
- Markdown for formatting
- Streaming for real-time updates

### Known Limitations
- No native sidebar component
- Limited styling options
- No native progress bars
- No native tooltips
- Consider future version updates for additional features

## Alternative Approaches

### For Technical Details
Instead of a sidebar, use:
1. Collapsible sections in messages
2. Separate messages for different types of information
3. Message elements for structured content

### For Progress Indicators
Use:
1. Message updates
2. Streaming content
3. Status messages
4. Clear section headers

### For Interactive Elements
Use:
1. Action buttons for common operations
2. Select dropdowns for choices
3. Input fields for user data
4. Message elements for structured content 