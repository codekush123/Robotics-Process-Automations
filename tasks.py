from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Excel.Files import Files
from RPA.PDF import PDF
@task
def project():
    """Insert the Artist Data and export it as a PDF"""
    browser.configure(
        slowmo=10,
    )
    open_website()
    log_in()
    download_excel_file()
    fill_form_with_excel_data()
    collect_results()
    export_as_pdf()
    

def open_website():
    """Navigates to the given URL"""
    browser.goto("https://fspacheco.github.io/rpa-challenge/music-collection.html")

def log_in():
   """Fills the login Form"""
   page= browser.page()
   page.fill("#username", "student")
   page.fill("#password", "rpa@hamk")
   page.click("button:text('login')")

def fill_and_submit_actor_form(music_collection):
    """Fill the data and click add to collection"""
    page=browser.page()
    page.fill("#artist", music_collection["Artist"])
    page.fill("#album", music_collection["Album"])
    page.fill("#year", str(music_collection["Release Year"]))
    page.select_option("#format", music_collection["Format"])
    page.select_option("#condition", music_collection["Condition"])
    page.click("#addToCollection")

def download_excel_file():
    "Download excel file from our url"
    http = HTTP()
    http.download(url="https://fspacheco.github.io/rpa-challenge/assets/music-collection-sample.xlsx", overwrite=True)
     
def fill_form_with_excel_data():
    """Read data from the excel and fill in the sales form"""
    excel = Files()
    excel.open_workbook("music-collection-sample.xlsx")
    worksheet = excel.read_worksheet_as_table("music-collection", header= True)
    excel.close_workbook()
    
    for row in worksheet:
        fill_and_submit_actor_form(row)

def collect_results():
    """Take a screenshot of the page"""
    page = browser.page()
    page.screenshot(path="output/music_collection_summary.png")
def export_as_pdf():
    """Export the data to pdf file"""
    page = browser.page()
    full_Music_Collection_Table = page.locator("#fullMusicCollectionTable").inner_html()
    
    pdf = PDF()
    pdf.html_to_pdf("<table>"+ full_Music_Collection_Table+ "</table>", "output/full_Music_Collection_Table.pdf")
