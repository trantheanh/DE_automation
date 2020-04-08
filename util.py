import DE_automation_core as automator
from tkinter import *
from tkinter import filedialog

my_tester = automator.Template(driver=automator.get_driver("chromedriver"), timeout=15)


def get_json_file_path(default_path):
   file_path = filedialog.askopenfilename(initialdir=default_path)

   return file_path


def get_url(ids, tester: automator.Template=my_tester):
    result = {}
    for i in range(len(ids)):
        sys.stdout.write("\rGetting urls of id  {}/{}: {}".format(i + 1, len(ids), ids[i]))
        result[ids[i]] = []

        tester.goto_url("https://www.drugbank.ca/drugs")
        tester.wait_util(
            target_xpath=automator.Template.get_xpath(
                tag_name="input",
                att_dict={
                    "type": "text",
                    "name": "query",
                    "id": "query",
                    "class": "search-query"
                }
            )
        )
        tester.enter_input(
            input_xpath=automator.Template.get_xpath(
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
        tester.press_button(
            btn_xpath=automator.Template.get_xpath(
                tag_name="input",
                att_dict={
                    "type": "text",
                    "name": "query",
                    "id": "query",
                    "class": "search-query"
                }
            )
        )
        tester.wait_util(
            target_xpath=automator.Template.get_xpath(
                tag_name="div",
                att_dict={
                    "class": "general-content"
                }
            )
        )
        tester.focus(
            target_xpath=automator.Template.get_xpath(
                tag_name="div",
                att_dict={
                    "class": "general-content"
                }
            )
        )

        elements = tester.current_focus.find_elements_by_xpath(
            automator.Template.get_xpath_sub(
                tag_name="a",
                att_dict={

                }
            )
        )

        searched_urls = [element.get_attribute("href") for element in elements if
                         "/drugs/" in element.get_attribute("href")]

        result[ids[i]] = searched_urls

    return result


def get_uniprot_ids(url, tester: automator.Template=my_tester):
    results = []

    tester.goto_url(url=url)

    tester.wait_util(
        target_xpath=automator.Template.get_xpath(
            tag_name="a",
            att_dict={
                "href": "#targets",
                "class": "btn bond-link targets"
            }
        )
    )

    tester.press_button(
        btn_xpath=automator.Template.get_xpath(
            tag_name="a",
            att_dict={
                "href": "#targets",
                "class": "btn bond-link targets"
            }
        )
    )

    tester.wait_util(
        target_xpath=automator.Template.get_xpath(
            tag_name="div",
            att_dict={
                "class": "bond-list-container targets"
            }
        )
    )

    tester.focus(
        target_xpath=automator.Template.get_xpath(
            tag_name="div",
            att_dict={
                "class": "bond-list-container targets"
            }
        )
    )

    tester.focus_to_child(target_xpath=automator.Template.get_xpath_sub(
        tag_name="div",
        att_dict={
            "class": "bond-list"
        }
    ))


    btn_index = -1

    while True:
        btn_index += 1
        is_out_of_tab = not tester.focus_by_index(target_index=btn_index)

        if is_out_of_tab:
            break

        tab_name = tester.get_text_from_current_sub_focus(
            target_xpath=automator.Template.get_xpath_sub(
                tag_name="strong",
                att_dict={

                }
            )
        )

        uniprot_ids = []

        ### Get single Uniprot_id ###
        tester.focus_by_index(target_index=btn_index)
        tester.subfocus_to_child(
            target_xpath=automator.Template.get_xpath_sub(
                tag_name="div",
                att_dict={
                    "class": "card-body"
                }
            )
        )
        tester.subfocus_to_child(
            target_xpath=automator.Template.get_xpath_sub(
                tag_name="div",
                att_dict={
                    "class": "row"
                }
            )
        )
        tester.subfocus_to_child(
            target_xpath=automator.Template.get_xpath_sub(
                tag_name="div",
                att_dict={
                    "class": "col-sm-12 col-lg-7"
                }
            )
        )
        text = tester.get_text_from_current_sub_focus(
            target_xpath=automator.Template.get_xpath_sub(
                tag_name="a",
                att_dict={
                    "target": "_blank",
                    "rel": "noopener",
                }
            )
        )

        if text:
            if len(text) == 6:
                uniprot_ids.append(text)
                results.append({tab_name: uniprot_ids})
                continue

        ### Get multi Uniprot ids from compoment
        tester.focus_by_index(target_index=btn_index)
        tester.subfocus_to_child(
            target_xpath=automator.Template.get_xpath_sub(
                tag_name="div",
                att_dict={
                    "class": "card-body"
                }
            )
        )
        tester.subfocus_to_child(
            target_xpath=automator.Template.get_xpath_sub(
                tag_name="div",
                att_dict={
                    "class": "col-12 col-sm-8"
                }
            )
        )
        texts = tester.get_texts_from_current_sub_focus(
            target_xpath=automator.Template.get_xpath_sub(
                tag_name="a",
                att_dict={
                    "target": "_blank",
                    "rel": "noopener",
                }
            )
        )

        if texts:
            uniprot_ids += [text for text in texts if len(text) == 6]

        results.append({tab_name: uniprot_ids})

    return results
