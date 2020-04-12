from automator.core import Tester as Tester
from tkinter import *
from tkinter import filedialog
from automator.category import Browser
import automator.action as action

my_tester = Tester(browser=Browser.Chrome, timeout=15)


def get_json_file_path(default_path):
   file_path = filedialog.askopenfilename(initialdir=default_path)

   return file_path


def get_url(ids, tester: Tester = my_tester):
    result = {}
    for i in range(len(ids)):
        sys.stdout.write("\rGetting urls of id  {}/{}: {}".format(i + 1, len(ids), ids[i]))
        result[ids[i]] = []

        tester.execute(
            action.goto_url,
            url="https://www.drugbank.ca/drugs"
        )
        tester.execute(
            action.wait_for,
            target_xpath=Tester.get_xpath(
                tag_name="input",
                att_dict={
                    "type": "text",
                    "name": "query",
                    "id": "query",
                    "class": "search-query"
                }
            )
        )
        tester.execute(
            action.enter_input,
            input_xpath=Tester.get_xpath(
                tag_name="input",
                att_dict={
                  "type": "text",
                  "name": "query",
                  "id": "query",
                  "class": "search-query"
                },
            ),
            value=ids[i]
        )
        tester.execute(
            action.click,
            target_xpath=Tester.get_xpath(
                tag_name="input",
                att_dict={
                    "type": "text",
                    "name": "query",
                    "id": "query",
                    "class": "search-query"
                }
            )
        )
        tester.execute(
            action.wait_for,
            target_xpath=Tester.get_xpath(
                tag_name="div",
                att_dict={
                    "class": "general-content"
                }
            )
        )
        tester.execute(
            action.focus,
            target_xpath=Tester.get_xpath(
                tag_name="div",
                att_dict={
                    "class": "general-content"
                }
            )
        )

        elements = tester.current_focus.find_elements_by_xpath(
            Tester.get_xpath(
                tag_name="a",
                att_dict={

                }
            )
        )

        searched_urls = [element.get_attribute("href") for element in elements if
                         "/drugs/" in element.get_attribute("href")]

        result[ids[i]] = searched_urls

        tester.reset_state()

    return result


def get_uniprot_ids(url, tester: Tester = my_tester):
    results = []

    tester.execute(
        action.goto_url,
        url=url
    )

    tester.execute(
        action.wait_for,
        target_xpath=Tester.get_xpath(
            tag_name="a",
            att_dict={
                "href": "#targets",
                "class": "btn bond-link targets"
            }
        )
    )

    tester.execute(
        action.click,
        target_xpath=Tester.get_xpath(
            tag_name="a",
            att_dict={
                "href": "#targets",
                "class": "btn bond-link targets"
            }
        )
    )

    tester.execute(
        action.wait_for,
        target_xpath=Tester.get_xpath(
            tag_name="div",
            att_dict={
                "class": "bond-list-container targets"
            }
        )
    )

    tester.execute(
        action.focus,
        target_xpath=Tester.get_xpath(
            tag_name="div",
            att_dict={
                "class": "bond-list-container targets"
            }
        )
    )

    tester.execute(
        action.focus,
        target_xpath=Tester.get_xpath(
            tag_name="div",
            att_dict={
                "class": "bond-list"
            }
        )
    )

    btn_index = -1
    tester.caching()

    while True:
        btn_index += 1

        is_out_of_tab = not tester.execute(action.focus_by_index, target_index=btn_index)

        if is_out_of_tab:
            break

        tab_name = tester.get(
            action.get_text_of_node,
            target_xpath=Tester.get_xpath(
                tag_name="strong",
                att_dict={

                }
            )
        )

        uniprot_ids = []

        ### Get single Uniprot_id ###
        tester.execute(
            action.focus,
            target_xpath=Tester.get_xpath(
                tag_name="div",
                att_dict={
                    "class": "card-body"
                }
            ),
        )

        tester.execute(
            action.focus,
            target_xpath=Tester.get_xpath(
                tag_name="div",
                att_dict={
                    "class": "row"
                }
            ),
        )

        tester.execute(
            action.focus,
            target_xpath=Tester.get_xpath(
                tag_name="div",
                att_dict={
                    "class": "col-sm-12 col-lg-7"
                }
            ),
        )

        text = tester.get(
            action.get_text_of_node,
            target_xpath=Tester.get_xpath(
                tag_name="a",
                att_dict={
                    "target": "_blank",
                    "rel": "noopener",
                }
            )
        )

        tester.previous_focus(need_remove=False)

        if text:
            if len(text) == 6:
                uniprot_ids.append(text)
                results.append({tab_name: uniprot_ids})
                continue

        ### Get multi Uniprot ids from compoment
        tester.execute(action.focus_by_index, target_index=btn_index)
        tester.execute(
            action.focus,
            target_xpath=Tester.get_xpath(
                tag_name="div",
                att_dict={
                    "class": "card-body"
                }
            )
        )
        tester.execute(
            action.focus,
            target_xpath=Tester.get_xpath(
                tag_name="div",
                att_dict={
                    "class": "col-12 col-sm-8"
                }
            )
        )
        texts = tester.get(
            action.get_texts_of_nodes,
            target_xpath=Tester.get_xpath(
                tag_name="a",
                att_dict={
                    "target": "_blank",
                    "rel": "noopener",
                }
            )
        )

        tester.previous_focus(need_remove=False)

        if texts:
            uniprot_ids += [text for text in texts if len(text) == 6]

        results.append({tab_name: uniprot_ids})

    tester.reset_state()

    return results


