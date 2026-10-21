# Web Navigation Skill

Guidance for navigating and interacting with web forms and elements in the NaijaMarketAgent marketplace.

## Rules
1. One tool call per turn. Always wait for the result before acting again.
2. After searching for anything, ensure you click the associated search button to complete the user request.
3. Always identify the correct `data-agent` id for each element before clicking or typing.
4. For form submissions, click the submit button when all fields are filled.

## Standard flow
1. `get_page_elements()` — reads current `data-agent` elements on screen.
2. `click_element(id)` — click a specific button or link by id.
3. `type_into(id, text)` — type text into an input field by id.
4. `press_key(id, key)` — press a keyboard key (e.g., "Enter") on a focused element.
5. `clear_input(id)` — clear an input field by id.

## Tips
- Wait for page state to settle after each action before proceeding.
- Always verify the element exists with its `data-agent` id before interacting.
- Read the page carefully to identify search buttons vs. submit buttons.
