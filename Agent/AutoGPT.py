import json
from typing import List, Optional, Tuple

from langchain.memory.chat_memory import BaseChatMemory
from langchain.tools.render import render_text_description
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.memory import ConversationTokenBufferMemory, VectorStoreRetrieverMemory
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain.schema.output_parser import StrOutputParser
from langchain.tools.base import BaseTool
from langchain.vectorstores.base import VectorStoreRetriever
from langchain_core.memory import BaseMemory
from langchain_core.prompts import PromptTemplate
from pydantic import ValidationError

from Agent.Action import Action
from Utils.CallbackHandlers import *


class AutoGPT:
    """AgentGPT with Lanagchain"""

    @staticmethod
    def __chinese_friendly(string) -> str:
        lines = string.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('{') and line.endswith('}'):
                try:
                    lines[i] = json.dumps(json.loads(line), ensure_ascii=False)
                except:
                    pass
        return '\n'.join(lines)

    @staticmethod
    def __format_long_term_memory(task_description: str, memory: BaseChatMemory) -> str:
        return memory.load_memory_variables(
            {"prompt": task_description}
        )["history"]

    @staticmethod
    def __format_short_term_memory(memory: BaseChatMemory) -> str:
        messages = memory.chat_memory.messages
        string_messages = [messages[i].content for i in range(1, len(messages))]
        return "\n".join(string_messages)

    def __init__(
            self,
            llm: BaseChatModel,
            tools: List[BaseTool],
            work_dir: str = "./data",
            main_prompt_file: str = "./prompts/main/main.json",
            final_prompt_file: str = "./prompts/main/final_step.json",
            max_thought_steps: Optional[int] = 10,
            memery_retriever: Optional[VectorStoreRetriever] = None,
    ):
        self.llm = llm
        self.tools = tools
        self.work_dir = work_dir
        self.max_thought_steps = max_thought_steps
        self.memery_retriever = memery_retriever

        # OutputFixingParser
        self.output_parser = PydanticOutputParser(pydantic_object=Action)
        self.robust_parser = OutputFixingParser.from_llm(parser=self.output_parser, llm=self.llm)

        self.main_prompt_file = main_prompt_file
        self.final_prompt_file = final_prompt_file

        self.__init_prompt_templates()
        self.__init_chains()

        self.verbose_handler = ColoredPrintHandler(color=THOUGHT_COLOR)

    def __init_prompt_templates(self):
        self.main_prompt = PromptTemplate.from_file(
            self.main_prompt_file
        ).partial(
            work_dir=self.work_dir,
            tools=render_text_description(self.tools),
            format_instructions=self.__chinese_friendly(
                self.output_parser.get_format_instructions(),
            )
        )
        self.final_prompt = PromptTemplate.from_file(
            self.final_prompt_file
        )

    def __init_chains(self):
        self.main_chain = (self.main_prompt | self.llm | StrOutputParser())
        self.final_chain = (self.final_prompt | self.llm | StrOutputParser())

    def __find_tool(self, tool_name: str) -> Optional[BaseTool]:
        for tool in self.tools:
            if tool.name == tool_name:
                return tool
        return None

    def __step(self,
               task_description,
               short_term_memory,
               long_term_memory,
               verbose=False
               ) -> Tuple[Action, str]:

        """excute one step of thinking"""
        response = ""
        for s in self.main_chain.stream({
            "task_description": task_description,
            "short_term_memory": self.__format_short_term_memory(
                short_term_memory
            ),
            "long_term_memory": self.__format_long_term_memory(
                task_description,
                long_term_memory
            ) if long_term_memory is not None else "",
        }, config={
            "callbacks": [
                self.verbose_handler
            ] if verbose else []
        }):
            response += s

        action = self.robust_parser.parse(response)
        return action, response

    def __final_step(self, short_term_memory, task_description) -> str:
        """final step, generate output"""
        response = self.final_chain.invoke({
            "task_description": task_description,
            "short_term_memory": self.__format_short_term_memory(
                short_term_memory
            ),
        })
        return response

    def __exec_action(self, action: Action) -> str:
        # tools
        tool = self.__find_tool(action.name)
        if tool is None:
            observation = (
                f"Error: cannot find proper tool for '{action.name}'. "
                f"choose from tools or functions, make sure the outcome is aligned"
            )
        else:
            try:
                observation = tool.run(action.args)
            except ValidationError as e:
                observation = (
                    f"Validation Error in args: {str(e)}, args: {action.args}"
                )
            except Exception as e:
                observation = f"Error: {str(e)}, {type(e).__name__}, args: {action.args}"

        return observation

    def __init_short_term_memory(self) -> BaseChatMemory:
        short_term_memory = ConversationTokenBufferMemory(
            llm=self.llm,
            max_token_limit=4000,
        )
        short_term_memory.save_context(
            {"input": "\nInit"},
            {"output": "\nStart"}
        )
        return short_term_memory

    def __connect_long_term_memory(self) -> BaseMemory:
        if self.memery_retriever is not None:
            long_term_memory = VectorStoreRetrieverMemory(
                retriever=self.memery_retriever,
            )
        else:
            long_term_memory = None
        return long_term_memory

    @staticmethod
    def __update_short_term_memory(
            short_term_memory: BaseChatMemory,
            response: str,
            observation: str
    ):
        short_term_memory.save_context(
            {"input": response},
            {"output": "\nreturn:\n" + observation}
        )

    @staticmethod
    def __update_long_term_memory(
            long_term_memory: BaseMemory,
            task_description: str,
            final_reply: str
    ):
        if long_term_memory is not None:
            long_term_memory.save_context(
                {"input": task_description},
                {"output": final_reply}
            )

    @staticmethod
    def __show_observation(observation: str, verbose: bool):
        if verbose:
            color_print(f"----\n结果:\n{observation}", OBSERVATION_COLOR)

    def run(self, task_description, verbose=False) -> str:
        short_term_memory = self.__init_short_term_memory()
        long_term_memory = self.__connect_long_term_memory()

        thought_step_count = 0

        while thought_step_count < self.max_thought_steps:
            if verbose:
                color_print(f">>>>Round: {thought_step_count}<<<<", ROUND_COLOR)

            action, response = self.__step(
                task_description=task_description,
                short_term_memory=short_term_memory,
                long_term_memory=long_term_memory,
                verbose=verbose,
            )

            if action.name == "FINISH":
                break

            observation = self.__exec_action(action)
            self.__show_observation(observation, verbose)

            self.__update_short_term_memory(
                short_term_memory, response, observation
            )

            thought_step_count += 1

        if thought_step_count >= self.max_thought_steps:
            reply = "Sorry, mission failed"
        else:
            reply = self.__final_step(short_term_memory, task_description)

        self.__update_long_term_memory(long_term_memory, task_description, reply)

        return reply
