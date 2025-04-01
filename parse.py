from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import psutil

templateENG = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

templateHUN = (
    "Az a feladatod, hogy konkrét információkat nyerj ki a következő szöveges tartalomból: {dom_content}. "
    "Kövesd ezeket az utasításokat: \n\n"
    "1. **Információ kinyerés:** Csak azokat az információkat vedd ki, amelyek közvetlenül megegyeznek a megadott leírással: {parse_description}. "
    "2. **Nincs extra tartalom:** Válaszodban ne adj meg további szöveget, megjegyzést vagy magyarázatot. "
    "3. **Ha nincs válasz:** Ha egyetlen információ sem felel meg a leírásnak, adj vissza egy üres karakterláncot ('')."
    "4. **Céltudatos válasz:** A kimenetnek csak azokat az adatokat kell tartalmaznia, amelyeket kifejezetten kérek, más szöveg nélkül."
)

model = OllamaLLM(model="gemma3:1b")  # milyen llm válaszoljon

def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(templateENG)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke({"dom_content": chunk, "parse_description": parse_description})
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(response)

    return "\n".join(parsed_results)

def stop_ollama(process_name):
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if proc.info['name'] == process_name:
            print(f"Leállítom: {proc.info['name']} (PID: {proc.info['pid']})")
            psutil.Process(proc.info['pid']).terminate()
