import copy
import os
try:
    import GPUtil #sometimes errors occurs on gpu testing
except:
    pass
import psutil
import ntpath
import platform
from llama_cpp import Llama
from Orange.data import Domain, StringVariable, Table


if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.AAIT.llm import prompt_management
    from Orange.widgets.orangecontrib.AAIT.utils import MetManagement
else:
    from orangecontrib.AAIT.llm import prompt_management
    from orangecontrib.AAIT.utils import MetManagement


def check_gpu(model_path, argself):
    """
    Checks if the GPU has enough VRAM to load a model.

    Args:
        model_path (str): Path to the model file.
        argself (OWWidget): OWQueryLLM object.

    Returns:
        bool: True if the model can be loaded on the GPU, False otherwise.
    """
    argself.error("")
    argself.warning("")
    argself.information("")
    argself.can_run = True
    argself.use_gpu = True
    return

    # attention bien faire la suite dans un try exept car gputil peut etre capricieux
    token_weight = 0.13
    if model_path is None:
        argself.use_gpu = False
        return
    if platform.system() != "Windows":
        argself.use_gpu = False
        return
    if not model_path.endswith(".gguf"):
        argself.use_gpu = False
        argself.can_run = False
        argself.error("Model is not compatible. It must be a .gguf format.")
        return
    # Calculate the model size in MB with a 1500 MB buffer
    model_size = os.path.getsize(model_path) / (1024 ** 3) * 1000
    model_size += token_weight * int(argself.n_ctx)
    print(f"Required memory: {model_size/1000:.2f}GB")
    # If there is no GPU, set use_gpu to False
    if len(GPUtil.getGPUs()) == 0:
        argself.use_gpu = False
        argself.information("Running on CPU. No GPU detected.")
        return
    # Else
    else:
        # Get the available VRAM on the first GPU
        gpu = GPUtil.getGPUs()[0]
        free_vram = gpu.memoryFree
    # If there is not enough VRAM on GPU
    if free_vram < model_size:
        # Set use_gpu to False
        argself.use_gpu = False
        # Check for available RAM
        available_ram = psutil.virtual_memory().available / 1024 / 1024
        if available_ram < model_size:
            argself.can_run = False
            argself.error(f"Cannot run. Both GPU and CPU are too small for this model (required: {model_size/1000:.2f}GB).")
            return
        else:
            argself.warning(f"Running on CPU. GPU seems to be too small for this model (available: {free_vram/1000:.2f}GB || required: {model_size/1000:.2f}GB).")
            return
    # If there is enough space on GPU
    else:
        try:
            # Load the model and test it
            # model = GPT4All(model_name=model_path, model_path=model_path, n_ctx=int(argself.n_ctx),
            #                 allow_download=False, device="cuda")
            # answer = model.generate("What if ?", max_tokens=3)
            # # If it works, set use_gpu to True
            argself.use_gpu = True
            argself.information("Running on GPU.")
            return
        # If importing Llama and reading the model doesn't work
        except Exception as e:
            # Set use_gpu to False
            argself.use_gpu = False
            argself.warning(f"GPU cannot be used. (detail: {e})")
            return


def load_model(model_path, use_gpu, n_ctx=10000):
    """
    Charge un modèle GGUF avec llama_cpp.Llama.

    - use_gpu=True : tente d'utiliser l'accélération (Metal/CUDA/Vulkan selon build)
      en mettant n_gpu_layers à -1 (= toutes les couches si possible).
    - use_gpu=False : CPU only (n_gpu_layers=0).
    """
    if not os.path.exists(model_path):
        print(f"Model could not be found: {model_path} does not exist")
        return

    try:
        # n_gpu_layers : -1 = toutes les couches si le binaire a un backend GPU (Metal/CUDA/Vulkan)
        n_gpu_layers = -1 if use_gpu else 0

        # n_threads : par défaut tous les cœurs logiques dispo moins 1 (pour avoir l'interface graphique qui ne freeze pas)
        n_threads = max(1, (os.cpu_count()-1 or 1))

        # NOTE : llama_cpp utilise n_ctx pour la taille de contexte
        model = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_threads=n_threads,
            n_gpu_layers=n_gpu_layers,
            # Quelques réglages sûrs
            use_mmap=True,
            use_mlock=False,
            embedding=False,
            verbose=False,
        )
        return model
    except Exception as e:
        print("Failed to load model with llama_cpp:", e)
        return


def generate_answers(table, model_path, use_gpu=False, n_ctx=4096, query_parameters=None, workflow_id="", progress_callback=None, argself=None):
    """
    Identique en signature/comportement, mais utilise llama_cpp sous le capot.
    """
    # Copie des données d'entrée
    data = copy.deepcopy(table)
    attr_dom = list(data.domain.attributes)
    metas_dom = list(data.domain.metas)
    class_dom = list(data.domain.class_vars)

    # Chargement modèle (llama_cpp)
    model = load_model(model_path=model_path, use_gpu=use_gpu, n_ctx=n_ctx)

    # Paramètres de génération par défaut
    if query_parameters is None:
        query_parameters = {"max_tokens": 4096, "temperature": 0.4, "top_p": 0.4, "top_k": 40, "repeat_penalty": 1.15}

    # Génération sur la colonne "prompt"
    try:
        rows = []
        for i, row in enumerate(data):
            features = list(data[i])
            metas = list(data.metas[i])
            prompt = row["prompt"].value

            system_prompt = row["system prompt"].value if "system prompt" in data.domain else ""
            assistant_prompt = row["assistant prompt"].value if "assistant prompt" in data.domain else ""

            # Appliquer ton template existant (inchangé)
            prompt = prompt_management.apply_prompt_template(
                model_path,
                user_prompt=prompt,
                assistant_prompt=assistant_prompt,
                system_prompt=system_prompt
            )

            answer = run_query(
                prompt,
                model=model,
                max_tokens=query_parameters["max_tokens"],
                temperature=query_parameters["temperature"],
                top_p=query_parameters["top_p"],
                top_k=query_parameters["top_k"],
                repeat_penalty=query_parameters["repeat_penalty"],
                workflow_id=workflow_id,
                argself=argself,
                progress_callback=progress_callback
            )

            if answer == "":
                answer = (
                    "Error: The answer could not be generated. The model architecture you tried to use is most "
                    f"likely not supported yet.\n\nModel name: {ntpath.basename(model_path)}"
                )

            metas += [answer]
            rows.append(features + metas)

            if progress_callback is not None:
                progress_value = float(100 * (i + 1) / len(data))
                progress_callback((progress_value, "\n\n\n\n"))

            if argself is not None and getattr(argself, "stop", False):
                break
    except ValueError as e:
        print("An error occurred when trying to generate an answer:", e)
        return

    # Ajouter la colonne "Answer" en metas
    answer_dom = [StringVariable("Answer")]

    domain = Domain(attributes=attr_dom, metas=metas_dom + answer_dom, class_vars=class_dom)
    out_data = Table.from_list(domain=domain, rows=rows)
    return out_data

class StopCallback:
    def __init__(self, stop_sequences, widget_thread=None):
        self.stop_sequences = stop_sequences
        self.recent_tokens = ""
        self.returning = True  # Store the last valid token before stopping
        self.widget_thread = widget_thread

    def __call__(self, token_id, token):
        # Stop in case thread is stopped
        if self.widget_thread:
            if self.widget_thread.stop:
                return False

        # Stop in case stop word has been met
        if not self.returning:
            return False
        self.recent_tokens += token

        # Check if any stop sequence appears
        for stop_seq in self.stop_sequences:
            if stop_seq in self.recent_tokens:
                self.returning = False  # Stop the generation, but allow the last token

        return True  # Continue generation

def write_tokens_to_file(token: str, workflow_id=""):
    chemin_dossier = MetManagement.get_api_local_folder(workflow_id=workflow_id)
    if os.path.exists(chemin_dossier):
        MetManagement.write_file_time(chemin_dossier + "time.txt")
        filepath = os.path.join(chemin_dossier, "chat_output.txt")
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(token)
            f.flush()


def run_query(prompt, model, max_tokens=4096, temperature=0, top_p=0, top_k=40, repeat_penalty=1.15,
              workflow_id="", argself=None, progress_callback=None):
    """
    Version llama_cpp avec streaming.
    On garde la même signature et le même contrat de retour.
    """


    # Séquences d'arrêt à filtrer du résultat final
    stop_sequences = ["<|endoftext|>", "### User", "<|im_end|>", "<|im_start|>", "<|im_end>", "<im_end|>", "<im_end>"]
    callback_instance = StopCallback(stop_sequences, argself)

    # Paramètres de sampling mappés vers llama_cpp
    gen_kwargs = dict(
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p if top_p else 1.0,   # top_p=0 désactive → on met 1.0
        top_k=top_k if top_k else 0,     # top_k=0 désactive
        repeat_penalty=repeat_penalty,
        stream=True,
    )

    answer = ""

    # IMPORTANT :
    # - On utilise create_completion (prompt-style) pour rester compatible avec ton templating actuel.
    # - Le générateur renvoie des chunks contenant choices[0].text.
    try:
        stream = model.create_completion(prompt=prompt, **gen_kwargs)

        for chunk in stream:
            # Récupérer le texte incrémental
            token = chunk["choices"][0].get("text", "")
            if not token:
                continue

            # Callback d'arrêt custom (on simule token_id=None)
            if not callback_instance(None, token):
                # On stoppe proprement le flux (consommation du générateur non nécessaire)
                answer += token  # on peut inclure le dernier token si souhaité
                break

            answer += token
            write_tokens_to_file(token, workflow_id)

            if progress_callback is not None:
                progress_callback((None, token))

            if argself is not None and getattr(argself, "stop", False):
                # Arrêt demandé de l'extérieur
                return answer

    except Exception as e:
        # En cas d'erreur pendant la génération, on retourne ce qu'on a + log
        print("Generation error (llama_cpp):", e)

    # Nettoyage des séquences d'arrêt
    for stop in stop_sequences:
        if stop:
            answer = answer.replace(stop, "")

    return answer


# def generate_conversation(table, model, model_path, conversation="", progress_callback=None, argself=None):
#     """
#     Generates a response using a language model and appends it to a conversation.
#
#     Parameters:
#     ----------
#     table (Orange.data.Table) Input data table. The first row should contain at least a "prompt" column, and optionally
#         "system prompt" and "assistant prompt" columns for context.
#
#     model (GPT4All) : Loaded language model instance, compatible with GPT4All or llama.cpp-style interfaces.
#
#     model_path (str) : Path or name of the model, used for selecting the appropriate prompt template.
#
#     conversation (str, optional) : Existing conversation string to append the new response to. Defaults to an empty string.
#
#     progress_callback (callable, optional) : Callback function for UI updates during generation. Called with progress percentage and message.
#
#     argself (object, optional) : Extra argument passed to `run_query`, typically the widget instance (used for context or settings).
#
#     Returns:
#     -------
#     Orange.data.Table
#         A new Orange Table containing the original input row with two new meta columns:
#         - "Answer": the model's generated response.
#         - "Conversation": the updated full conversation string.
#     """
#     if table is None:
#         return
#
#     # Copy of input data
#     data = copy.deepcopy(table)
#     attr_dom = list(data.domain.attributes)
#     metas_dom = list(data.domain.metas)
#     class_dom = list(data.domain.class_vars)
#
#     features = list(data[0])
#     metas = list(data.metas[0])
#
#     # Get data from the first row of the Data Table
#     system_prompt = data[0]["system prompt"].value if "system prompt" in data.domain else ""
#     assistant_prompt = data[0]["assistant prompt"].value if "assistant prompt" in data.domain else ""
#     user_prompt = data[0]["prompt"].value
#
#     # Build prompt based on the model name
#     prompt = prompt_management.apply_prompt_template(model_path, user_prompt=user_prompt, assistant_prompt=assistant_prompt, system_prompt=system_prompt)
#     answer = run_query(prompt, model=model, argself=argself, progress_callback=progress_callback)
#     conversation += "### Assistant :\n\n" + answer + "\n\n\n\n"
#
#     # Add spaces to the widget for following answers
#     progress_callback((100, "\n\n\n\n"))
#
#     # Generate new Domain to add to data
#     metas += [answer, conversation]
#     row = [features + metas]
#     answer_dom = [StringVariable("Answer"), StringVariable("Conversation")]
#
#     # Create and return table
#     domain = Domain(attributes=attr_dom, metas=metas_dom + answer_dom, class_vars=class_dom)
#     out_data = Table.from_list(domain=domain, rows=row)
#     return out_data
