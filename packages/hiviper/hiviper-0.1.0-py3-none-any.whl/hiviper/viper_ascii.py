import sys
def say(text: str) -> str:
    bubble = f"""
    {'_' * (len(text) + 4)}
   <  {text}  >
    {'‾' * (len(text) + 4)}
    """

    viper = r"""
        __________
\/     /(*)   (*) \
 \____|__________/  \
        \_______      \
                `\     \                 \
                  |     |                  \
                 /      /                    \
                /     /                       \\
              /      /                         \ \
             /     /                            \  \
           /     /             _----_            \   \
          /     /           _-~      ~-_         |   |
         (      (        _-~    _--_    ~-_     _/   |
          \      ~-____-~    _-~    ~-_    ~-_-~    /
            ~-_           _-~          ~-_       _-~
               ~--______-~                ~-___-~
    """

    return bubble + viper

def cli():
    text=" ".join(sys.argv[1:]) or "Hello"
    print(say(text))