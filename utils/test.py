from kivy.utils import platform

print(f"Platform: {platform}") # See if this prints without error

import kivy.utils
print(dir(kivy.utils)) # Print all names in the module
# dp = kivy.utils.dp # Keep this line commented out for now