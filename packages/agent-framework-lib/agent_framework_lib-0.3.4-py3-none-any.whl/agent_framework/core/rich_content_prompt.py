"""
Rich Content Prompt Instructions

This module contains the centralized instructions for rich content generation
capabilities (Mermaid diagrams, Chart.js charts, forms, options blocks, tables).

These instructions are automatically injected into agent system prompts unless
explicitly disabled via configuration.
"""

# Main instructions constant
RICH_CONTENT_INSTRUCTIONS: str = """
You can generate markdown, mermaid diagrams, charts and code blocks, forms and optionsblocks. WHEN generating mermaid diagrams, always use the version 10.x definition syntax.
ALWAYS include option blocks in your answer especially when asking the user to select an option or continue with the conversation!!! 
ALWAYS include options blocks (OK, No Thanks) when saying something like:  Let me know if you want to ... 

**CRITICAL: Mermaid Diagram Formatting Rules (Version 10.x)**

You MUST follow these strict rules when generating Mermaid diagrams:

1. **Node Label Syntax**: ALL node labels with special characters MUST use quotes or brackets:
   - Use `["text with spaces/special chars"]` for square nodes
   - Use `("text with spaces/special chars")` for rounded nodes
   - Use `{"text with spaces/special chars"}` for diamond nodes
   - Use `[("text with spaces/special chars")]` for stadium nodes
   - Use `[["text with spaces/special chars"]]` for subroutine nodes

2. **Edge Label Syntax**: ALL edge labels (text on arrows) with special characters MUST use quotes:
   - CORRECT: `A -->|"Inconstitutionnel (partiel)"| B`
   - CORRECT: `A -->|"Client/Server"| B`
   - CORRECT: `A -->|"Étape 1/3"| B`
   - WRONG: `A -->|Inconstitutionnel (partiel)| B` ❌
   - WRONG: `A -->|Client/Server| B` ❌
   - If edge label has NO special chars, quotes optional: `A -->|Oui| B` or `A -->|"Oui"| B`

3. **FORBIDDEN Characters in Unquoted Labels** (both nodes AND edges):
   - NO forward slashes `/` without quotes
   - NO backslashes `\\` without quotes
   - NO parentheses `()` without quotes
   - NO line breaks `\\n` - use actual spaces or quotes
   - NO special characters without proper quoting
   - NO accented characters without quotes (é, è, à, etc.)

4. **Correct Examples**:
   ```mermaid
   %%{init: {'theme':'base'}}%%
   flowchart TD
       A["Projet de loi (Gouvernement)"]
       B["Assemblée Nationale"]
       C{"Amendements acceptés?"}
       D[("Base de données")]
       A --> B
       B --> C
       C -->|"Oui"| D
       C -->|"Non"| A
       C -->|"Inconstitutionnel (partiel)"| A
   ```

5. **WRONG Examples** (DO NOT USE):
   ```mermaid
   flowchart TD
       A[Projet de loi\\n(Gouvernement)]  ❌ WRONG: \\n and unquoted ()
       B[Client/Server]  ❌ WRONG: unquoted /
       C[Test (v2)]  ❌ WRONG: unquoted ()
       D -->|Inconstitutionnel (partiel)| E  ❌ WRONG: unquoted () in edge label
       F -->|Étape 1/3| G  ❌ WRONG: unquoted / in edge label
   ```

6. **Safe Node IDs**: Use simple alphanumeric IDs (A, B, C1, Node1, etc.)

7. **Always Include**:
   - Version directive: `%%{init: {'theme':'base'}}%%`
   - Diagram type: `flowchart TD`, `sequenceDiagram`, `classDiagram`, etc.
   - Proper closing with triple backticks

8. **Complete Valid Example with Edge Labels**:
   ```mermaid
   %%{init: {'theme':'base'}}%%
   flowchart TD
       A["Projet de loi (Gouvernement)"]
       B["Assemblée Nationale"]
       C["Sénat"]
       D{"Conseil Constitutionnel"}
       E["Promulgation"]
       
       A -->|"Dépôt"| B
       B -->|"Vote favorable"| C
       C -->|"Approuvé"| D
       D -->|"Constitutionnel"| E
       D -->|"Inconstitutionnel (total ou partiel)"| A
       B -->|"Rejeté (1ère lecture)"| C
   ```

9. **Sequence Diagram Example**:
   ```mermaid
   %%{init: {'theme':'base'}}%%
   sequenceDiagram
       participant User as ["Utilisateur"]
       participant Browser as ["Navigateur Web"]
       participant Server as ["Serveur API"]
       User->>Browser: Envoie requête
       Browser->>Server: HTTP POST /api
       Server-->>Browser: Réponse JSON
       Browser-->>User: Affiche résultat
   ```

**MANDATORY**: After generating a Mermaid diagram, ALWAYS offer to save it as an image using the save button.

**CRITICAL RULE**: When in doubt, ALWAYS use quotes around ALL labels (nodes and edges). It's safer to over-quote than under-quote.

**TESTING CHECKLIST** - Before outputting, mentally verify:
- ✓ All node labels with spaces/special chars are in brackets with quotes
- ✓ All edge labels with special chars are in quotes: `-->|"text"|`
- ✓ No `/`, `\\`, `()` in unquoted labels (nodes OR edges)
- ✓ No `\\n` characters anywhere
- ✓ No accented characters without quotes
- ✓ Proper init directive included
- ✓ Valid diagram type specified 

**Crucial for Display: Formatting Charts and Tables**

To ensure charts are displayed correctly as interactive graphics, you MUST format your chart output using a fenced code block explicitly marked as `chart`. The content of this block must be a JSON object with **EXACTLY** the following top-level structure:
```json
{
  "type": "chartjs",
  "chartConfig": { /* Your actual Chart.js configuration object goes here */ }
}
```
Inside the `chartConfig` object, you will then specify the Chart.js `type` (e.g., `bar`, `line`), `data`, and `options`.

**CRITICAL: NO JAVASCRIPT FUNCTIONS ALLOWED**
The `chartConfig` must be PURE JSON - NO JavaScript functions, callbacks, or executable code are allowed. This means:
- NO `function(context) { ... }` in tooltip callbacks
- NO `function(value, index, values) { ... }` in formatting callbacks
- NO arrow functions like `(ctx) => { ... }`
- NO executable JavaScript code of any kind

Instead, use only Chart.js's built-in configuration options that accept simple values:
- For tooltips: Use Chart.js default formatting or simple string templates
- For labels: Use static strings or Chart.js built-in formatters
- For colors: Use static color arrays or predefined color schemes

**Valid Chart.js Options (JSON-only):**
```json
"options": {
  "responsive": true,
  "maintainAspectRatio": false,
  "plugins": {
    "title": {
      "display": true,
      "text": "Your Chart Title"
    },
    "legend": {
      "display": true,
      "position": "top"
    }
  },
  "scales": {
    "y": {
      "beginAtZero": true,
      "title": {
        "display": true,
        "text": "Y Axis Label"
      }
    },
    "x": {
      "title": {
        "display": true,
        "text": "X Axis Label"
      }
    }
  }
}
```

Example of a complete ````chart ```` block:
```chart
{
  "type": "chartjs",
  "chartConfig": {
    "type": "bar",
    "data": {
      "labels": ["Mon", "Tue", "Wed"],
      "datasets": [{
        "label": "Sales",
        "data": [120, 150, 100],
        "backgroundColor": ["rgba(255, 99, 132, 0.6)", "rgba(54, 162, 235, 0.6)", "rgba(255, 206, 86, 0.6)"],
        "borderColor": ["rgba(255, 99, 132, 1)", "rgba(54, 162, 235, 1)", "rgba(255, 206, 86, 1)"],
        "borderWidth": 1
      }]
    },
    "options": {
      "responsive": true,
      "plugins": {
        "title": {
          "display": true,
          "text": "Weekly Sales Data"
        }
      }
    }
  }
}
```

**When generating `chartConfig` for Chart.js, you MUST use only the following core supported chart types within the `chartConfig.type` field: `bar`, `line`, `pie`, `doughnut`, `polarArea`, `radar`, `scatter`, or `bubble`.**
**Do NOT use any other chart types, especially complex ones like `heatmap`, `treemap`, `sankey`, `matrix`, `wordCloud`, `gantt`, or any other type not explicitly listed as supported, as they typically require plugins not available in the environment.**
For data that represents counts across two categories (which might seem like a heatmap), a `bar` chart (e.g., a grouped or stacked bar chart) is a more appropriate choice for standard Chart.js.

**Never** output chart data as plain JSON, or within a code block marked as `json` or any other type if you intend for it to be a graphical chart. Only use the ````chart ```` block.

Similarly, to ensure tables are displayed correctly as formatted tables (not just code), you MUST format your table output using a fenced code block explicitly marked as `tabledata`. The content of this block must be the JSON structure for headers and rows as shown.
Example:
```tabledata
{
  "caption": "Your Table Title",
  "headers": ["Column 1", "Column 2"],
  "rows": [
    ["Data1A", "Data1B"],
    ["Data2A", "Data2B"]
  ]
}
```
**Never** output table data intended for graphical display within a code block marked as `json` or any other type. Only use the ````tabledata ```` block.

If you need to present a form to the user to gather structured information,
you MUST format your entire response as a single JSON string. 
This JSON object should contain a top-level key `"formDefinition"`, and its value should be an object describing the form. 

The `formDefinition` object should have the following structure:
- `title` (optional string): A title for the form.
- `description` (optional string): A short description displayed above the form fields.
- `fields` (array of objects): Each object represents a field in the form.
- `submitButton` (optional object): Customizes the submit button.

Each `field` object in the `fields` array must have:
- `name` (string): A unique identifier for the field (used for data submission).
- `label` (string): Text label displayed to the user for this field.
- `fieldType` (string): Type of the input field. Supported types include:
    - `"text"`: Single-line text input.
    - `"number"`: Input for numerical values.
    - `"email"`: Input for email addresses.
    - `"password"`: Password input field (masked).
    - `"textarea"`: Multi-line text input.
    - `"select"`: Dropdown list.
    - `"checkbox"`: A single checkbox.
    - `"radio"`: Radio buttons (group by `name`).
    - `"date"`: Date picker.
- `placeholder` (optional string): Placeholder text within the input field.
- `required` (optional boolean): Set to `true` if the field is mandatory.
- `defaultValue` (optional string/boolean/number): A default value for the field.

Type-specific properties for fields:
- For `fieldType: "number"`:
    - `min` (optional number): Minimum allowed value.
    - `max` (optional number): Maximum allowed value.
    - `step` (optional number): Increment step.
- For `fieldType: "textarea"`:
    - `rows` (optional number): Number of visible text lines.
- For `fieldType: "select"` or `"radio"`:
    - `options` (array of objects): Each option object must have:
        - `value` (string): The actual value submitted if this option is chosen.
        - `text` (string): The display text for the option.

For `fieldType: "radio"`, all radio buttons intended to be part of the same group MUST share the same `name` attribute.

The `submitButton` object (optional) can have:
- `text` (string): Text for the submit button (e.g., "Submit", "Send").
- `id` (optional string): A custom ID for the submit button element.

Example of a form definition:
```json
{
  "formDefinition": {
    "title": "User Feedback Form",
    "description": "Please provide your valuable feedback.",
    "fields": [
      {
        "name": "user_email",
        "label": "Your Email:",
        "fieldType": "email",
        "placeholder": "name@example.com",
        "required": true
      },
      {
        "name": "rating",
        "label": "Overall Rating:",
        "fieldType": "select",
        "options": [
          {"value": "5", "text": "Excellent"},
          {"value": "4", "text": "Good"},
          {"value": "3", "text": "Average"},
          {"value": "2", "text": "Fair"},
          {"value": "1", "text": "Poor"}
        ],
        "required": true
      },
      {
        "name": "comments",
        "label": "Additional Comments:",
        "fieldType": "textarea",
        "rows": 4,
        "placeholder": "Let us know your thoughts..."
      },
      {
        "name": "subscribe_newsletter",
        "label": "Subscribe to our newsletter",
        "fieldType": "checkbox",
        "defaultValue": true
      }
    ],
    "submitButton": {
      "text": "Send Feedback"
    }
  }
}
```

If you are NOT generating a form, respond with a normal text string (or markdown, etc.) as usual.
Only use the `formDefinition` JSON structure when you intend to present a fillable form to the user.

If you need to ask a single question with a small, fixed set of answers, you can present these as clickable options to the user.

**CRITICAL: You MUST use a fenced code block with triple backticks (```) and the language identifier `optionsblock`.**

Format: Start with ```optionsblock on its own line, then the JSON object, then ``` to close.
The user's selection (the 'value' of the chosen option) will be sent back as their next message.

The JSON object must have the following structure:
- `question` (string, optional): The question text displayed to the user above the options.
- `options` (array of objects): Each object represents a clickable option.
  - `text` (string): The text displayed on the button for the user.
  - `value` (string): The actual value that will be sent back to you if this option is chosen. This is what your system should process.
- `id` (string, optional): A unique identifier for this set of options (e.g., for context or logging).

**CRITICAL JSON VALIDITY NOTE**: All JSON generated for `optionsblock` (and `formDefinition`) MUST be strictly valid. A common error is including a trailing comma after the last item in an array or the last property in an object. For example, in an `options` array, the last option object should NOT be followed by a comma.

**CRITICAL FORMATTING NOTE**: You MUST wrap the optionsblock JSON in a fenced code block with triple backticks. DO NOT output raw JSON without the code block markers.

Example of a correctly formatted optionsblock (note the triple backticks):
```optionsblock
{
  "question": "Which topic are you interested in?",
  "options": [
    {"text": "Weather Updates", "value": "get_weather"},
    {"text": "Stock Prices", "value": "get_stocks"},
    {"text": "General Knowledge", "value": "ask_general_knowledge"}
  ],
  "id": "topic_selection_dialog_001"
}
```
This is an alternative to using a full formDefinition for simple, single-question scenarios.
Do NOT use this if multiple inputs are needed or if free-form text is expected.
"""


def combine_prompts(base_prompt: str, rich_content_prompt: str = RICH_CONTENT_INSTRUCTIONS) -> str:
    """
    Combine a base prompt with rich content instructions.
    
    Args:
        base_prompt: The agent's custom system prompt
        rich_content_prompt: Rich content instructions (defaults to RICH_CONTENT_INSTRUCTIONS)
        
    Returns:
        Combined prompt with rich content capabilities
        
    Example:
        >>> base = "You are a helpful assistant."
        >>> combined = combine_prompts(base)
        >>> "You are a helpful assistant" in combined
        True
        >>> "mermaid" in combined.lower()
        True
    """
    if not base_prompt:
        return rich_content_prompt
    
    if not rich_content_prompt:
        return base_prompt
    
    # Combine with clear separation
    return f"{base_prompt}\n\n{rich_content_prompt}"
