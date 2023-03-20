# -*- coding: utf-8 -*-
"""
Anki Add-on: No Screen Due

Hides all due numbers (learn, due, new) on the main screen and on the deck screen
"""
import itertools
from aqt import gui_hooks

def on_overview_will_render_content(overview, content):
    # Find the start and end indices of the new-count, learn-count, and review-count spans
    new_count_start = content.table.find("<span class=new-count>")
    new_count_end = content.table.find("</span>", new_count_start)
    learn_count_start = content.table.find("<span class=learn-count>")
    learn_count_end = content.table.find("</span>", learn_count_start)
    review_count_start = content.table.find("<span class=review-count>")
    review_count_end = content.table.find("</span>", review_count_start)

    # Replace the spans with the "hidden" span
    content.table = (content.table[:new_count_start] +
                     "<span class=new-count>~</span>" +
                     content.table[new_count_end+7:learn_count_start] +
                     "<span class=learn-count>~</span>" +
                     content.table[learn_count_end+7:review_count_start] +
                     "<span class=review-count>~</span>" +
                     content.table[review_count_end+7:])

def on_deck_browser_will_render_content(browser, content):
    # Find all substrings at once
    substrings = find_all_substrings(content.tree, [
        '<span class="new-count">',
        '<span class="learn-count">',
        '<span class="review-count">',
        '<span class="zero-count">'
    ], '</span>')

    # Replace all substrings with a placeholder
    placeholder = '<span class="zero-count">~</span>'
    content.tree = replace_substrings(content.tree, substrings, placeholder)

def find_all_substrings(main_str, start_substrings, end_substr):
    for start_substr in start_substrings:
        start_index = 0
        while True:
            start_index = main_str.find(start_substr, start_index)
            if start_index == -1:
                break
            end_index = main_str.find(end_substr, start_index)
            if end_index == -1:
                break
            yield main_str[start_index:end_index+len(end_substr)]
            start_index = end_index + 1

def replace_substrings(main_string, substring_generator, replace_with):
    # Use a generator expression to iterate over the substrings
    # and replace them one at a time, without loading them all into memory
    new_string = main_string
    for substring in substring_generator:
        new_string = new_string.replace(substring, replace_with)
    return new_string


gui_hooks.overview_will_render_content.append(on_overview_will_render_content)
gui_hooks.deck_browser_will_render_content.append(on_deck_browser_will_render_content)
