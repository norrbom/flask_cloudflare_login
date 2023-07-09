from os import getenv


def app_config(dot_env):
    """
    Returns:
        returns a string showing application configuration, with an optional banner
    """
    output = f"\n{dot_env.get('APP_NAME')} started with this config:"
    dot_env["SECRET_KEY"] = getenv("SECRET_KEY")
    if dot_env.get("SECRET_KEY"):
        dot_env["SECRET_KEY"] = "*******************************"
    for key in dot_env:
        output += "\n" + key + "=" + dot_env[key]
    return output
