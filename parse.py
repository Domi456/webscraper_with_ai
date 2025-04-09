from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import psutil

templateENG = (
    "You are a helpful webscraper assistant. Answer the questions based on the content, scraped from a website." 
    "Give brief and concise answers. Do not ask for clarifications or additional task. "
    "Content: {dom_content}"
    "Questions: {parse_description}"
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
