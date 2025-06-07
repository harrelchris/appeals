// https://www.algolia.com/doc/api-reference/widgets/instantsearch/js/
const MEILI_HTTP_ADDR = "http://localhost:7700";
const MEILI_MASTER_KEY = "meilisearchmasterkey";

const search = instantsearch({
  indexName: "decisions",
  searchClient: instantMeiliSearch(
    MEILI_HTTP_ADDR, "meilisearchmasterkey"
  ).searchClient
  });

  search.addWidgets([
    instantsearch.widgets.searchBox({
      container: "#searchbox"
    }),
    instantsearch.widgets.configure({ hitsPerPage: 8 }),
    instantsearch.widgets.hits({
      container: "#hits",
      templates: {
      item: `
        <div>
          <div class="hit-name">
                {{#helpers.highlight}}{ "attribute": "id" }{{/helpers.highlight}}
          </div>
        </div>
      `
      }
    })
  ]);
  search.start();
