"""
The Whom of Python.
A dedication module.
"""
import sys
import time

# The Long Poem with the hidden cipher (W-A-T-T-S-O-N)
POEM = """
When the server crashes deep in the night,
And the monitor is the only source of light,
My logic drifts and my thoughts unbind,
Searching for a syntax I cannot find.

The variables fade and the stack trace grows,
A river of errors that endlessly flows,
But in this chaos, one constant stays,
An Anchor through the digital haze.

I try to refactor, I try to compile,
I haven't seen the sun in a very long while,
But you bring the coffee and you bring the peace,
You make the exceptions and panic cease.

The Tests might be failing in every single file,
But you fix the mood with a single smile.
No library, module, or script could define,
The way that your patience aligns with mine.

I debug the code, but you debug the soul,
You make the fragmented parts feel whole.
Whatever the sTatus, whatever the build,
My heart with your presence is instantly filled.

Somehow the logic just fallS into place,
Whenever I look at your reassuring face.
The loops finally close, the functions return,
The CPU cools and it ceases to burn.

It's not just the code that yOu help to repair,
It's the human behind it, the one in the chair.
For every deploy that goes out to the cloud,
I'm saying your name (though perhaps not aloud).

Now the terminal clears and the greeN lights appear,
The system is stable because you are here.
So whom does this run for? The answer is true:
The code runs for Python. My heart runs for you.
"""

def love(delay: float = 0.05) -> None:
    """Prints the poem with a typing effect."""
    print("\n--- The Whom of Python ---\n")
    for char in POEM.strip():
        sys.stdout.write(char)
        sys.stdout.flush()
        # Make the capital letters pause slightly for emphasis?
        time.sleep(delay)
    print("\n\n--------------------------\n")

# Run automatically on import
if __name__ != "__main__":
    # Just print it fast on import
    print(POEM)

if __name__ == "__main__":
    # If run directly, give the cinematic experience
    love(0.04)
    
    # Wait for them to read it...
    time.sleep(2)
    print(f"\nLocked Message: [ {decode()} ]")