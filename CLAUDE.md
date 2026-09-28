# Project Rules

1. Keep the GUI in Python using CustomTkinter. Do not introduce React, JavaScript, web frameworks, or new external dependencies for GUI features.

2. Preserve the existing inference rules and knowledge base when adding GUI features. New settings should be passed through the existing `user_input` flow instead of rewriting the rules.

3. Validate user-entered numeric values in the GUI before sending them to the inference engine. Invalid input should show a clear message instead of causing the application to crash.

4. New optional settings should preserve the old behavior when the user leaves them empty or does not provide them.

5. When adding a new GUI setting, test the normal case, invalid input, empty input, and each supported option before considering the feature complete.
