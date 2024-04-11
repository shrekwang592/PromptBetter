import warnings

warnings.filterwarnings("ignore")

from langchain.tools import StructuredTool
from .FileQATool import ask_docment
from .WriterTool import write
from .EmailTool import send_email
from .ExcelTool import get_first_n_rows
from .FileTool import list_files_in_directory

document_qa_tool = StructuredTool.from_function(
    func=ask_docment,
    name="AskDocument",
    description="Based on the content of a Word or PDF document, answer a question. Consider the context information to ensure that the question fully articulates the definition of relevant concepts",
)

document_generation_tool = StructuredTool.from_function(
    func=write,
    name="GenerateDocument",
    description="Generate a formal document based on the requirements described.",
)

email_tool = StructuredTool.from_function(
    func=send_email,
    name="SendEmail",
    description="Send an email to the specified addresses. Ensure that the email format is xxx@xxx.xxx. Separate multiple email addresses with a semicolon (;).",
)

excel_inspection_tool = StructuredTool.from_function(
    func=get_first_n_rows,
    name="InspectExcel",
    description="Examine the contents and structure of the spreadsheet file, display its column names and the first n rows, where n defaults to 3.",
)

directory_inspection_tool = StructuredTool.from_function(
    func=list_files_in_directory,
    name="ListDirectory",
    description="Explore the contents and structure of the folder, display its file names and folder names.",
)

finish_placeholder = StructuredTool.from_function(
    func=lambda: None,
    name="FINISH",
    description="A placeholder used to signify the completion of a task"
)
