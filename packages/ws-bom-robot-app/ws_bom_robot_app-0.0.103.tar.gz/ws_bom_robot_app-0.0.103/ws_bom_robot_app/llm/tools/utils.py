import random, os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from ws_bom_robot_app.llm.providers.llm_manager import LlmInterface
from ws_bom_robot_app.llm.utils.print import print_string

def __print_output(data: str) -> str:
  return print_string(data) if os.environ.get("AGENT_HANDLER_FORMATTED") == str(True) else f"{data} "

def getRandomWaitingMessage(waiting_messages: str, traduction: bool = True) -> str:
  if not waiting_messages: return ""
  messages = [msg.strip() for msg in waiting_messages.split(";") if msg.strip()]
  if not messages: return ""
  chosen_message = random.choice(messages) + "\n"
  if not traduction:
      return __print_output(chosen_message)
  return chosen_message

async def translate_text(llm: LlmInterface, language, text: str, callbacks: list) -> str:
  if language == "it":
      return __print_output(text)
  sys_message = """Il tuo compito è di tradurre il testo_da_tradurre nella seguente lingua: \n\n lingua: {language}\n\n testo_da_tradurre: {testo_da_tradurre} \n\nTraduci il testo_da_tradurre nella lingua {language} senza aggiungere altro:"""
  prompt = PromptTemplate.from_template(sys_message)
  chain = prompt | llm.get_llm()
  await chain.ainvoke({"language":language, "testo_da_tradurre": text}, {"callbacks": callbacks})

async def fetch_page(session, url):
    try:
        async with session.get(url, timeout=10, ssl=False) as response:
            if response.status == 200:
                text = await response.text()
                return {"url": url, "html": text}
            else:
                return {"url": url, "html": None}
    except Exception as e:
        return {"url": url, "html": None}

async def extract_content_with_trafilatura(html):
    """Estrae solo il testo principale usando trafilatura"""
    import trafilatura
    return trafilatura.extract(html)
