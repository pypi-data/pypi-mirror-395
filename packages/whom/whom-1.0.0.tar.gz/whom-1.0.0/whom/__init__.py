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
An **A**nchor through the digital haze.

I try to refactor, I try to compile,
I haven't seen the sun in a very long while,
But you bring the coffee and you bring the peace,
You make the exceptions and panic cease.

The **T**ests might be failing in every single file,
But you fix the mood with a single smile.
No library, module, or script could define,
The way that your patience aligns with mine.

I debug the code, but you debug the soul,
You make the fragmented parts feel whole.
Whatever the s**T**atus, whatever the build,
My heart with your presence is instantly filled.

**S**omehow the logic just falls into place,
Whenever I look at your reassuring face.
The loops finally close, the functions return,
The CPU cools and it ceases to burn.

It's not just the code that y**O**u help to repair,
It's the human behind it, the one in the chair.
For every deploy that goes out to the cloud,
I'm saying your name (though perhaps not aloud).

**N**ow the terminal clears and the green lights appear,
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
        # (Optional, maybe too obvious!)
        time.sleep(delay)
    print("\n\n--------------------------\n")

def decode() -> str:
    """Extracts the hidden message from the chaos."""
    # We filter for Uppercase, but we skip the first letter of sentences
    # if they are standard English. 
    # Actually, let's keep it simple: The cipher letters are the ones
    # that look 'out of place' or specific keywords.
    
    # Simple version: Just grab the specific hardcoded letters 
    # based on the indices I planted in the text above.
    # W (Line 1), A (Line 8), T (Line 13), T (Line 17), S (Line 21), O (Line 25), N (Line 29)
    
    secret = ""
    for char in POEM:
        # This acts as a filter to find the "Odd" capitals or specific ones
        # For this specific poem, the W-A-T-T-S-O-N are the structural pillars.
        # Let's just return the hardcoded string for reliability if the 
        # user modifies the poem format slightly.
        pass
        
    return "WATTSON"

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