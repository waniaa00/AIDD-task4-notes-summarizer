import os
from dotenv import load_dotenv
from agents import Agent, RunConfig, AsyncOpenAI, Runner, OpenAIChatCompletionsModel

load_dotenv()
os.environ["OPENAI_API_KEY"] = "" #hehe
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

agent = Agent(
    name="Study Notes Agent",
    instructions="You are a helpful study assistant. You summarize PDFs into clear, student-friendly notes and generate quizzes based on the content.",
    model=model,
)

async def run_agent(prompt: str) -> str:
    """Run the agent with the given prompt and return the response."""
    from agents import Runner
    result = await Runner.run(agent, prompt)
    return result.final_output
