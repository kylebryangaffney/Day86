from screen import TypingSpeedApp
from text import long_text, short_text

# Create an instance of TypingSpeedApp
type_speed_app = TypingSpeedApp()

# Set the test lines from the long_text variable
type_speed_app.get_test_lines(long_text)

# Start the main event loop
type_speed_app.start_mainloop()
