"""
A sample module
"""

from yamlpp import ModuleEnvironment

def define_env(env: ModuleEnvironment):
    @env.export
    def greet(name: str) -> str:
        return f"Hello {name}"
    
    @env.filter
    def shout(value: str) -> str:
        return f"{value.upper()}!!!"
    
    env.variables["app_name"] = "YAMLpp"
