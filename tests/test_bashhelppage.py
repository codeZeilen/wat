from wat.pagesources import BashHelpPage

#
# Has Page
#


def test_has_page_for_builtin():
    assert BashHelpPage.has_page("echo")


#
# Get Page
#

def test_get_page_for_builtin():
    page = BashHelpPage.get_page("echo")
    assert page.page_name() == "echo"
    assert "Write arguments to the standard output." in page.description()

#
# Page Type
#


def page_type_for_builtin():
    page = BashHelpPage.get_page("echo")
    assert page.page_type() == "builtin"
