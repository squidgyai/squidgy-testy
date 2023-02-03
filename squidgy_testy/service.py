
def generate_prompt(
    prompt_file: str, 
    params: dict[str,str],
    additional_text: str = None
) -> str:
    with open(prompt_file) as f:
        prompt = f.read()

        if additional_text is not None:
            prompt += additional_text

        if params:
            for param in params:
                if params[param] is not None:
                    prompt = prompt.replace("{%s}" % param, params[param])
        return prompt
        
class PromptService:

    def invoke(
        self, 
        prompt: str,
        stop=['\n\n'], 
        settings: dict[str, object] = {}
    ) -> str:
        pass

    def embed(
        self, 
        texts: list[str]
    ) -> list[float]:
        pass