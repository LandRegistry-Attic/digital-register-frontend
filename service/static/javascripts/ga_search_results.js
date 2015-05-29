function ga_search_results(number_results, page_number) {
    search_term = document.getElementById('search_term').value
    if (number_results == 0) {
      result_description = "ZeroResults"
    } else {
      page_number = page_number
      result_description = "Page"+page_number
    }
    ga('send', 'event', 'Search', result_description, search_term);
}
